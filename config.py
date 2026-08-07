
import os

baseDir = os.path.dirname(os.path.abspath(__file__))

mdlDir = os.path.join(baseDir, "models")

dataDir = os.path.join(baseDir, "data")
histFile = os.path.join(dataDir, "history.json")

histKeep = 100

defaultMaxLen = 128
defaultThresh = 0.5

settingsFile = os.path.join(dataDir, "settings.json")

defaultSettings = {
    "confidence_threshold": 80,
    "max_prompt_tokens": 128,
    "show_shap_values": True,
    "show_probabilities": True,
}
