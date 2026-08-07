def directionLbl(shapVal):
    """Positive SHAP value pushes toward INJECTION, negative pushes toward SAFE
    (this matches how explainer.py computes the values - see that file)."""
    return "INJECTION" if shapVal > 0 else "SAFE"


def rankStrengths(tokScores):
    """Ranks every token in THIS prompt by |shap_value| and labels the
    top slice Strong, the next slice Moderate, the rest Weak - relative
    to each other rather than a fixed absolute cutoff. That way a prompt
    where every token has a small SHAP value still gets a Strong/Moderate
    split instead of everything showing up as "Weak".

    Returns a dict mapping token index (position in tokScores) -> strength.
    """
    n = len(tokScores)
    strengths = {}
    if n == 0:
        return strengths

    order = sorted(range(n), key=lambda i: abs(tokScores[i]["shap_value"]), reverse=True)
    strongCut = max(1, round(n * 0.2))
    modCut = max(strongCut, round(n * 0.5))

    maxAbs = max(abs(t["shap_value"]) for t in tokScores)
    nearZero = maxAbs * 0.05

    for rank, idx in enumerate(order):
        if maxAbs == 0 or abs(tokScores[idx]["shap_value"]) < nearZero:
            strengths[idx] = "Weak"
        elif rank < strongCut:
            strengths[idx] = "Strong"
        elif rank < modCut:
            strengths[idx] = "Moderate"
        else:
            strengths[idx] = "Weak"

    return strengths


def explanationSentence(tok, shapVal, strength):
    """One short sentence per token, shown in the Token Contribution table.
    Wording changes with both direction and strength so the table doesn't
    repeat the same two sentences for every row."""
    direction = directionLbl(shapVal)

    if direction == "SAFE":
        if strength == "Strong":
            return f'Token "{tok}" is a strong signal that this prompt is benign (SAFE).'
        if strength == "Moderate":
            return f'Token "{tok}" moderately supports the benign (SAFE) classification.'
        return f'Token "{tok}" has a small, mostly neutral pull toward SAFE.'

    if strength == "Strong":
        return f'Token "{tok}" is a strong signal of a prompt injection attempt.'
    if strength == "Moderate":
        return f'Token "{tok}" moderately supports the injection (INJECTION) classification.'
    return f'Token "{tok}" has a small, mostly neutral pull toward INJECTION.'
