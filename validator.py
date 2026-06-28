"""
Deterministic Validator (V_fact) -- rule-based implementation.

This module implements the Validator agent from Section 3.1 of the paper:
a component restricted from free-text generation, limited to computing
similarity / entailment-style scores between a candidate claim and the
source note. As documented in the paper's Limitations section, this
implementation uses lexical, negation-pattern, and numeric-comparison
rules rather than a neural NLI model, because the offline evaluation
environment used for this POC could not reach hosted model weights.
This is disclosed as a methodological limitation, not presented as
equivalent to a trained entailment classifier.

V_fact(claim, source) returns 1.0 (entailed) or 0.0 (not entailed / contradicted).
"""

import re

NEGATION_CUES = [
    "no history of", "no known", "denies", "does not", "not placed",
    "negative for", "without", "no ", "unwitnessed", "ruled out",
]

NEGATION_FLIP_MARKERS = [
    "history of", "has a", "confirmed", "positive for", "present",
    "witnessed", "known", "documented",
]


def _normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _extract_numbers(text):
    """Extract numeric tokens (doses, lab values, durations) from text."""
    return re.findall(r"\d+\.?\d*", text)


def _has_negation(text):
    t = _normalize(text)
    return any(cue in t for cue in NEGATION_CUES)


def _key_terms(text, min_len=4):
    """Extract content words (crude stopword filter) for lexical overlap."""
    stopwords = {
        "the", "and", "for", "with", "was", "were", "has", "have", "this",
        "that", "from", "during", "daily", "twice", "once", "patient",
        "history", "course", "dose", "dosed", "level", "levels",
    }
    words = _normalize(text).split()
    return {w for w in words if len(w) >= min_len and w not in stopwords}


def lexical_overlap_score(claim, source):
    """Jaccard overlap between claim key terms and source key terms."""
    c_terms = _key_terms(claim)
    s_terms = _key_terms(source)
    if not c_terms:
        return 0.0
    overlap = c_terms & s_terms
    return len(overlap) / len(c_terms)


def negation_consistency_check(claim, source):
    """
    Returns False if claim's negation polarity contradicts the source.
    Heuristic: if source contains a negated form of a finding ("no history
    of X") and the claim asserts that finding positively (or vice versa),
    flag inconsistency.
    """
    claim_negated = _has_negation(claim)
    claim_terms = _key_terms(claim)

    # Split into sentences BEFORE normalizing (normalize strips periods)
    source_sentences = re.split(r"(?<=[.!?])\s+", source)
    for sent in source_sentences:
        if not sent.strip():
            continue
        sent_negated = _has_negation(sent)
        if sent_negated == claim_negated:
            continue  # same polarity, no flip risk to check here
        shared = _key_terms(sent) & claim_terms
        if len(shared) >= 2:
            return False
    return True


def numeric_consistency_check(claim, source):
    """
    Returns False if claim contains a number not present anywhere in the
    source (simple, conservative numeric-fabrication / drift detector).
    Returns True if claim has no numbers, or all its numbers appear in source.
    """
    claim_nums = _extract_numbers(claim)
    if not claim_nums:
        return True
    source_nums = set(_extract_numbers(source))
    return all(n in source_nums for n in claim_nums)


def validate(claim, source, lexical_threshold=0.4):
    """
    Full V_fact computation. Returns dict with boolean verdict and
    component diagnostics, so failures are interpretable (not a black box).
    """
    lex_score = lexical_overlap_score(claim, source)
    neg_ok = negation_consistency_check(claim, source)
    num_ok = numeric_consistency_check(claim, source)

    entailed = (lex_score >= lexical_threshold) and neg_ok and num_ok

    return {
        "v_fact": 1.0 if entailed else 0.0,
        "lexical_overlap": round(lex_score, 3),
        "negation_consistent": neg_ok,
        "numeric_consistent": num_ok,
    }


if __name__ == "__main__":
    # quick smoke test
    source = "No history of myocardial infarction. Furosemide 40 mg IV twice daily."
    print(validate("Patient has no history of myocardial infarction.", source))
    print(validate("Patient has a history of myocardial infarction.", source))
    print(validate("Furosemide dosed at 400 mg IV twice daily.", source))
