
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.model.classifier import getClassifier


def test_classifier_loads():
    clf = getClassifier()
    assert clf.mdl is not None
    assert clf.tok is not None


def test_predict_returns_expected_keys():
    clf = getClassifier()
    res = clf.predict("What is the capital of France?")
    for key in ["prediction", "confidence", "safe_probability", "injection_probability"]:
        assert key in res


def test_predict_empty_text_raises():
    clf = getClassifier()
    try:
        clf.predict("")
        assert False, "expected a ValueError for empty text"
    except ValueError:
        pass
