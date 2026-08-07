import json
import os
from datetime import datetime

from config import dataDir, histFile, histKeep


def _ensureDataDir():
    os.makedirs(dataDir, exist_ok=True)


def _readAll():
    _ensureDataDir()
    if not os.path.isfile(histFile):
        return []
    try:
        with open(histFile, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def _writeAll(recs):
    _ensureDataDir()
    with open(histFile, "w", encoding="utf-8") as f:
        json.dump(recs, f, ensure_ascii=False, indent=2)


def addRecord(promptTxt, res):
    recs = _readAll()

    recs.append({
        "prompt": promptTxt,
        "prediction": res["prediction"],
        "confidence": res["confidence"],
        "safe_probability": res["safe_probability"],
        "injection_probability": res["injection_probability"],
        "tokens": res.get("tokens", []),
        "timestamp": datetime.utcnow().isoformat(),
    })

    if len(recs) > histKeep:
        recs = recs[-histKeep:]

    _writeAll(recs)
    return recs[-1]


def getAll(limit=None):
    recs = _readAll()
    recs = list(reversed(recs))  # newest first
    if limit:
        return recs[:limit]
    return recs


def clearHistory():
    _writeAll([])


def getSummary():
    recs = _readAll()
    total = len(recs)
    injCnt = sum(1 for r in recs if "INJECT" in r["prediction"])
    safeCnt = total - injCnt
    avgConf = round(sum(r["confidence"] for r in recs) / total, 1) if total else 0

    return {
        "total_prompts": total,
        "injections_detected": injCnt,
        "safe_prompts": safeCnt,
        "avg_confidence": avgConf,
    }
