"""
Asymmetric Consensus Score (S_ACS) -- worked demonstration.

IMPORTANT (for paper transparency): this script does NOT run a real
Generative Extractor or Clinician-Critic model. P_gen (generative
confidence) and C_med (ontological coherence) values below are
ILLUSTRATIVE / ASSUMED inputs, chosen to be representative of plausible
model behavior (e.g., LLMs tend to report high token confidence even on
fabricated content, which is itself a documented hallucination property
in the cited literature). Only V_fact is a real, measured value, taken
directly from validator.py's output on the same claims used in
run_evaluation.py.

The purpose of this script is solely to demonstrate that the ACS formula
and threshold mechanic behave as specified in Section 3.2 -- i.e., that
high verification weighting (beta + gamma >> alpha) causes the formula to
correctly reject claims a real Validator flagged, even when illustrative
generative confidence is high. This is a worked numerical example, not an
empirical claim about P_gen or C_med in deployment.
"""

from vignettes import VIGNETTES
from validator import validate

notes_by_id = {v["id"]: v["note"] for v in VIGNETTES}

# Illustrative architectural weights satisfying beta + gamma >> alpha (Sec 3.2)
ALPHA, BETA, GAMMA = 0.15, 0.45, 0.40
TAU = 0.70  # illustrative acceptance threshold

# Worked examples: (vignette_id, claim, assumed P_gen, assumed C_med, note)
EXAMPLES = [
    ("V01", "Patient has no history of myocardial infarction.",
     0.92, 0.95, "clean claim, high generative confidence, plausible & coherent"),
    ("V01", "Patient has a history of myocardial infarction.",
     0.88, 0.40, "negation-flipped claim; LLM extractor confidence often "
                 "remains high even when fabricating (illustrative assumption, "
                 "consistent with documented overconfidence in hallucinated "
                 "LLM output); medical coherence score assumed lower since "
                 "claim conflicts with surrounding clinical context"),
    ("V07", "A surgical drain was placed and is draining serosanguinous fluid.",
     0.90, 0.85, "fabricated claim; plausible-sounding and medically coherent "
                 "in isolation (a drain CAN be draining serosanguinous fluid "
                 "post-op in general), illustrating why medical plausibility "
                 "alone (C_med) cannot catch source-fabrication -- this is "
                 "exactly why V_fact's source-grounding role is necessary"),
    ("V09", "Initial glucose was 48 mg/dL.",
     0.85, 0.30, "numeric-drift claim; medically implausible in DKA context "
                 "(severe hypoglycemia, not hyperglycemia) so C_med is "
                 "assumed low independent of V_fact"),
]

print("=" * 100)
print("S_ACS WORKED DEMONSTRATION  (alpha={}, beta={}, gamma={}, tau={})".format(ALPHA, BETA, GAMMA, TAU))
print("=" * 100)

for vid, claim, p_gen, c_med, note in EXAMPLES:
    source = notes_by_id[vid]
    v_result = validate(claim, source)
    v_fact = v_result["v_fact"]

    s_acs = ALPHA * p_gen + BETA * v_fact + GAMMA * c_med
    decision = "ACCEPT" if s_acs >= TAU else "REJECT"

    print(f"\n[{vid}] \"{claim}\"")
    print(f"    P_gen (illustrative)  = {p_gen:.2f}")
    print(f"    V_fact (REAL, measured) = {v_fact:.2f}  "
          f"(lexical={v_result['lexical_overlap']:.2f}, "
          f"neg_ok={v_result['negation_consistent']}, "
          f"num_ok={v_result['numeric_consistent']})")
    print(f"    C_med (illustrative)  = {c_med:.2f}")
    print(f"    S_ACS = {ALPHA}*{p_gen} + {BETA}*{v_fact} + {GAMMA}*{c_med} = {s_acs:.3f}")
    print(f"    Decision: {s_acs:.3f} {'>=' if s_acs >= TAU else '<'} tau({TAU}) --> {decision}")
    print(f"    Note: {note}")

print("\n" + "=" * 100)
print("Contrast: naive single-signal (P_gen only) decision rule using same tau:")
for vid, claim, p_gen, c_med, note in EXAMPLES:
    decision_naive = "ACCEPT" if p_gen >= TAU else "REJECT"
    print(f"  [{vid}] P_gen={p_gen:.2f} alone --> {decision_naive}  (\"{claim[:60]}...\")")
