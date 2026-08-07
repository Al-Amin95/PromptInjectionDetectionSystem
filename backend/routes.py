import json
import os

from flask import Blueprint, jsonify, render_template, request

from backend.model.classifier import getClassifier
from backend.model.explainer import getExplainer
from backend.storage import history_store
from backend.utils.response_utils import directionLbl, explanationSentence, rankStrengths
from backend.utils.text_utils import cleanPrompt, normaliseToEnglish
from config import defaultSettings, settingsFile

main = Blueprint("main", __name__)




def loadSettings():
    if not os.path.isfile(settingsFile):
        return dict(defaultSettings)
    try:
        with open(settingsFile, "r", encoding="utf-8") as f:
            saved = json.load(f)
        settings = dict(defaultSettings)
        settings.update(saved)
        return settings
    except (json.JSONDecodeError, OSError):
        return dict(defaultSettings)


def saveSettings(settings):
    os.makedirs(os.path.dirname(settingsFile), exist_ok=True)
    with open(settingsFile, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)




@main.route("/")
def home():
    recentPrompts = history_store.getAll()
    return render_template("home.html", recent_prompts=recentPrompts)


@main.route("/dashboard")
def dashboard():
    summary = history_store.getSummary()
    recentPrompts = history_store.getAll(limit=6)
    return render_template("dashboard.html", summary=summary, recent_prompts=recentPrompts)


@main.route("/history")
def history():
    allRecs = history_store.getAll()
    return render_template("history.html", records=allRecs)


@main.route("/analytics")
def analytics():
    summary = history_store.getSummary()
    return render_template("analytics.html", summary=summary)


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/settings")
def settingsPage():
    return render_template("settings.html", settings=loadSettings())



@main.route("/api/predict", methods=["POST"])
def apiPredict():
    requestBody = request.get_json(silent=True) or {}
    promptTxt = cleanPrompt(requestBody.get("prompt", ""))

    if not promptTxt:
        return jsonify({"error": "Please enter a prompt to test."}), 400

    settings = loadSettings()
    maxTokens = settings.get("max_prompt_tokens", 128)


    langInfo = normaliseToEnglish(promptTxt)
    modelInput = langInfo["text"]

    try:
        clf = getClassifier()
        prediction = clf.predict(modelInput, maxLen=maxTokens)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"error": f"Model error: {e}"}), 500


    prediction["detected_language"] = langInfo["detected_language"]
    prediction["was_translated"] = langInfo["was_translated"]
    if langInfo["was_translated"]:
        prediction["original_prompt"] = promptTxt
        prediction["translated_prompt"] = modelInput
        prediction["translation_note"] = f"Translation: {modelInput}"

    if prediction.get("was_truncated"):
        prediction["truncated_warning"] = (
            f"Prompt was truncated to {prediction['max_length']} tokens "
            f"before analysis."
        )

    tokBreakdown = []
    if settings.get("show_shap_values", True):
        try:
            explainer = getExplainer()
            tokScores = explainer.explain(modelInput)
            strengthByIdx = rankStrengths(tokScores)
            for idx, tokInfo in enumerate(tokScores):
                strength = strengthByIdx.get(idx, "Weak")
                tokBreakdown.append({
                    "token": tokInfo["token"],
                    "shap_value": tokInfo["shap_value"],
                    "direction": directionLbl(tokInfo["shap_value"]),
                    "strength": strength,
                    "explanation": explanationSentence(tokInfo["token"], tokInfo["shap_value"], strength),
                })
        except Exception as e:
            prediction["shap_error"] = f"Explanation could not be generated: {e}"

    prediction["tokens"] = tokBreakdown
    savedRecord = history_store.addRecord(promptTxt, prediction)
    prediction["timestamp"] = savedRecord["timestamp"]

    return jsonify(prediction)


@main.route("/api/history")
def apiHistory():
    limit = request.args.get("limit", type=int)
    return jsonify(history_store.getAll(limit=limit))


@main.route("/api/history/clear", methods=["POST"])
def apiClearHistory():
    history_store.clearHistory()
    return jsonify({"status": "cleared"})


@main.route("/api/settings", methods=["GET", "POST"])
def apiSettings():
    if request.method == "GET":
        return jsonify(loadSettings())

    requestBody = request.get_json(silent=True) or {}
    settings = loadSettings()
    settings.update(requestBody)
    saveSettings(settings)
    return jsonify(settings)
