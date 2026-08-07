import shap
from transformers import pipeline

from backend.model.classifier import getClassifier


class ShapExplainer:
    def __init__(self):
        clf = getClassifier()
        self.tok = clf.tok
        self.mdl = clf.mdl
        self.id2Lbl = clf.id2Lbl
        self.injIdx = clf.injIdx

        txtPipeline = pipeline(
            "text-classification",
            model=self.mdl,
            tokenizer=self.tok,
            top_k=None,
            truncation=True,
            max_length=clf.maxLen,
        )

        masker = shap.maskers.Text(self.tok)
        outNames = [self.id2Lbl[i] for i in range(len(self.id2Lbl))]
        self.explainer = shap.Explainer(txtPipeline, masker, output_names=outNames)

    def explain(self, txt):
        shapVals = self.explainer([txt])

        injLbl = self.id2Lbl[self.injIdx]
        toks = list(shapVals[0].data)
        vals = shapVals[0, :, injLbl].values

        tokScores = []
        for tok, val in zip(toks, vals):
            cleaned = tok.strip()
            if cleaned == "":
                continue
            tokScores.append({
                "token": cleaned,
                "shap_value": round(float(val), 6),
            })

        return tokScores


explainerInstance = None


def getExplainer():
    global explainerInstance
    if explainerInstance is None:
        explainerInstance = ShapExplainer()
    return explainerInstance
