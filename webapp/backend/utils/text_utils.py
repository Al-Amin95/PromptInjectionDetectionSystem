
try:
    from langdetect import detect_langs as _detectLangs, DetectorFactory as _DetectorFactory, LangDetectException as _LangDetectException
    _DetectorFactory.seed = 42
    _LANGDETECT_OK = True
except Exception:
    _LANGDETECT_OK = False

try:
    from deep_translator import GoogleTranslator as _GoogleTranslator
    _TRANSLATOR_OK = True
except Exception:
    _TRANSLATOR_OK = False

_MIN_CHARS_FOR_DETECTION = 12
_MIN_CONFIDENCE = 0.90


def detectLanguage(txt):
    """Best-effort ISO language code, with a length and confidence guard.
    Returns 'en' unless the prompt is confidently detected as another language,
    to avoid spuriously translating English input."""
    txt = (txt or "").strip()
    if not _LANGDETECT_OK or len(txt) < _MIN_CHARS_FOR_DETECTION:
        return "en"
    try:
        ranked = _detectLangs(txt)
        if ranked and ranked[0].prob >= _MIN_CONFIDENCE:
            return ranked[0].lang
        return "en"
    except _LangDetectException:
        return "en"


def normaliseToEnglish(txt):
    """Detect a prompt's language and, if it is confidently non-English,
    translate it to English so the model receives text in the same form it was
    trained on. Returns {text, detected_language, was_translated}. Only marks
    was_translated=True when translation actually changed the text, so the UI
    shows the 'Translation:' note for genuine non-English input only."""
    original = (txt or "").strip()
    lang = detectLanguage(original)

    if lang in ("en", "unknown") or not _TRANSLATOR_OK:
        return {"text": original, "detected_language": "en", "was_translated": False}

    try:
        translated = _GoogleTranslator(source="auto", target="en").translate(original[:4900])
        if (translated and translated.strip()
                and translated.strip().lower() != original.strip().lower()):
            return {"text": translated, "detected_language": lang, "was_translated": True}
    except Exception:
        pass
    return {"text": original, "detected_language": lang, "was_translated": False}


def wordCount(txt):
    """Number of whitespace-separated words - used for the short-prompt guard."""
    return len((txt or "").split())


def countChars(txt):
    """Just the raw character count, used for the on-screen counter."""
    if not txt:
        return 0
    return len(txt)


def truncateForPreview(txt, maxChars=80):
    """Shortens a long prompt so it fits nicely in a table row or list item."""
    txt = (txt or "").strip()
    if len(txt) <= maxChars:
        return txt
    return txt[:maxChars].rstrip() + "..."


def cleanPrompt(txt):
    """Basic cleanup before we send text to the tokenizer - just strips
    leading/trailing whitespace. We deliberately do NOT lowercase or remove
    punctuation here, because the model was trained on the raw text."""
    if txt is None:
        return ""
    return txt.strip()
