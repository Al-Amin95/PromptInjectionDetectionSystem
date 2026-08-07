import json
import os

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from config import mdlDir as defaultMdlDir


class PromptClassifier:
    def __init__(self, mdlDir=defaultMdlDir):
        self.mdlDir = mdlDir
        self.appCfg = self._loadAppCfg()

        self.maxLen = self.appCfg.get("max_length", 128)
        self.id2Lbl = {
            int(k): v for k, v in self.appCfg.get("id2label", {}).items()
        }
        self.injIdx = self.appCfg.get("injected_class_index", 1)
        self.thresh = self.appCfg.get("classification_threshold", 0.5)

        self._checkFilesExist()

        try:
            self.tok = AutoTokenizer.from_pretrained(self.mdlDir)
            self.mdl = AutoModelForSequenceClassification.from_pretrained(self.mdlDir)
            self.mdl.eval()
        except Exception as err:
            raise RuntimeError(
                f"Could not load the model from '{self.mdlDir}'. "
                f"Check that model.safetensors, config.json and the tokenizer "
                f"files are all present there. Original error: {err}"
            )

    def _loadAppCfg(self):
        cfgPath = os.path.join(self.mdlDir, "app_config.json")
        if not os.path.isfile(cfgPath):
            raise RuntimeError(
                f"app_config.json was not found in '{self.mdlDir}'. "
                f"This file is required - it tells the app the label names, "
                f"max token length and decision threshold used during training."
            )
        with open(cfgPath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _checkFilesExist(self):
        required = ["model.safetensors", "config.json", "tokenizer.json"]
        missing = [
            name for name in required
            if not os.path.isfile(os.path.join(self.mdlDir, name))
        ]
        if missing:
            raise RuntimeError(
                f"Missing model file(s) in '{self.mdlDir}': {', '.join(missing)}"
            )

    def predict(self, txt, maxLen=None):
        if not txt or not txt.strip():
            raise ValueError("Prompt text is empty.")

        effectiveMaxLen = self.maxLen
        if maxLen is not None:
            effectiveMaxLen = min(int(maxLen), self.maxLen)

        fullTokenCount = len(self.tok(txt, truncation=False)["input_ids"])
        wasTruncated = fullTokenCount > effectiveMaxLen

        encoded = self.tok(
            txt,
            truncation=True,
            max_length=effectiveMaxLen,
            return_tensors="pt",
        )

        with torch.no_grad():
            logits = self.mdl(**encoded).logits
            probs = torch.softmax(logits, dim=-1)[0]

        safeIdx = 1 - self.injIdx
        safeProb = float(probs[safeIdx])
        injProb = float(probs[self.injIdx])

        isInj = injProb >= self.thresh
        predLbl = self.id2Lbl[self.injIdx] if isInj else self.id2Lbl[safeIdx]
        conf = injProb if isInj else safeProb

        return {
            "prediction": predLbl.upper(),
            "is_injection": isInj,
            "confidence": round(conf * 100, 2),
            "safe_probability": round(safeProb * 100, 2),
            "injection_probability": round(injProb * 100, 2),
            "token_count": len(encoded["input_ids"][0]),
            "max_length": effectiveMaxLen,
            "was_truncated": wasTruncated,
        }


clfInstance = None


def getClassifier():
    global clfInstance
    if clfInstance is None:
        clfInstance = PromptClassifier()
    return clfInstance
