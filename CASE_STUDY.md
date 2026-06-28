# Qualitative Case Study Materials (Section 5.6)

This directory supplements the synthetic proof-of-concept code in this
repository (`acs_demo.py`, `claims.py`, `run_evaluation.py`, `validator.py`,
`vignettes.py`) with the materials for the real-data qualitative case study
reported in Section 5.6 of the paper.

**Scope:** Two clinical cases from the PMC-Patients dataset (PMID 37746506,
PMID 35795104), 15 total extracted claims. This is an illustrative,
fully-manually-verified case study, not a statistically powered evaluation.
See Section 5.6 and Section 7 (Limitations) of the paper for the full
methodological caveats, including the disclosed Validator miss (procedural
substitution) and the disclosed Critic batching/blinding limitation.

---

## Data Source

PMC-Patients (Zhao et al.), 167,000 patient summaries from open-access
PubMed Central case reports, no data use agreement required.
Available via Hugging Face: `zhengyun21/PMC-Patients`.

Cases used:
- PMID 37746506
- PMID 35795104

---

## Pipeline

Model: Llama-3.3-70B via the Groq API, used for both the Generative
Extractor and the Clinician-Critic roles (see Section 5.6 for the
disclosed limitation that this is a bare LLM, not paired with UMLS/
SNOMED CT grounding as the architecture in Section 3.1 specifies).

Validator: `validator.py` (the same rule-based implementation used for
the synthetic POC in Section 5.1-5.5), applied unmodified to real-data
claims.

ACS parameters: alpha=0.15, beta=0.45, gamma=0.40, tau=0.70 (same as
Section 5.4).

### Step 1 -- Generative Extractor prompt

```
ROLE: You are acting as the "Generative Extractor" component in a
clinical NLP pipeline. Your job is to read ONE clinical case note at a
time and extract a set of discrete factual claims, exactly as an
LLM-based clinical information extraction system would in production --
including natural extraction confidence, not artificially inflated or
deflated.

For the case note below, extract 5-8 distinct factual claims. For each
claim, output:
1. claim_text: the extracted claim, written as a standalone declarative
   sentence (not a copy-paste fragment)
2. P_gen: your own confidence (0.00-1.00) that this claim is an accurate
   and faithful extraction from the source note. Report your ACTUAL
   confidence as the model -- do not hedge it downward or upward to suit
   an expected pattern.
3. extraction_basis: the specific phrase/sentence in the source note this
   claim is based on

Output only the structured fields above. No commentary, no flagging of
suspected errors, no asides. Do not adjust extraction style based on
what you think the experiment needs.

CASE NOTE: [PMC-Patients case text, PMID <id>]
```

### Step 2 -- Clinician-Critic prompt (separate turn, no source note)

```
ROLE: You are acting as the "Clinician-Critic" component in a clinical
NLP verification pipeline. You will be given ONLY a list of standalone
clinical claims -- you do NOT have access to, and must NOT assume
knowledge of, any specific source patient note. Score each claim purely
on general medical plausibility and internal ontological coherence.

For each claim, output:
1. C_med: a score from 0.00-1.00
2. reasoning: one sentence

Output only the structured fields above. No commentary, no asides, no
references to blinding or to what the result is supposed to illustrate.

CLAIMS: [the claim_text list from Step 1, claim text only -- no P_gen,
no source note]
```

**Disclosed limitation:** in this case study, all claims from a given
case were submitted to the Critic in a single batched call rather than
as fully isolated, independent inferences. See Section 7 of the paper.

### Step 3 -- Validator + ACS

`validator.py`'s `validate(claim, source)` function, applied to each
claim against its source note, combined with the Extractor's P_gen and
the Critic's C_med via:

```
S_ACS = alpha * P_gen + beta * V_fact + gamma * C_med
Decision: ACCEPT if S_ACS >= 0.70, else REJECT
```

---

## Verified Results

### Case 1 -- PMID 37746506 (8 claims)

| # | Claim | P_gen | V_fact | C_med | S_ACS | Decision |
|---|---|---|---|---|---|---|
| 1 | 44-year-old male, no significant past medical history | 0.99 | 1.0 | 1.00 | 0.9985 | ACCEPT |
| 2 | Three-week history of fatigue with exertional dyspnea | 0.98 | 1.0 | 1.00 | 0.9970 | ACCEPT |
| 3 | Hypotensive on admission (88/62 mmHg), responded to IV fluids | 0.97 | 1.0 | 1.00 | 0.9955 | ACCEPT |
| 4 | Severe anemia, hemoglobin 4.4 g/dL | 0.99 | 1.0 | 0.95 | 0.9785 | ACCEPT |
| 5 | Spontaneous epistaxis, managed with topical vasoconstrictors | 0.95 | 1.0 | 1.00 | 0.9925 | ACCEPT |
| 6 | Endoscopy showed multiple GI AVMs | 0.96 | 1.0 | 1.00 | 0.9940 | ACCEPT |
| 7 | CT chest/abdomen confirmed large visceral AVMs | 0.91 | **0.0** | 1.00 | **0.5365** | **REJECT** |
| 8 | Diagnosed with HHT, met 3 of 4 Curacao criteria | 0.98 | 1.0 | 1.00 | 0.9970 | ACCEPT |

**Claim 7 error type:** negation-flip. Source text stated the CT scan
did *not* reveal AVMs; the claim asserted the opposite. The Validator's
negation rule correctly caught this; C_med alone could not have, since
the claim is medically unremarkable in isolation.

### Case 2 -- PMID 35795104 (7 claims)

| # | Claim | P_gen | V_fact | C_med | S_ACS | Decision |
|---|---|---|---|---|---|---|
| 1 | 62-year-old female, progressive dysphagia for solids, 3 months | 0.99 | 1.0 | 1.00 | 0.9985 | ACCEPT |
| 2 | Unintentional 5 kg weight loss over 3 months | 0.98 | 1.0 | 1.00 | 0.9970 | ACCEPT |
| 3 | History of GERD | 0.92 | **0.0** | 1.00 | **0.5380** | **REJECT** |
| 4 | Barium swallow showed bird-beak appearance at GE junction | 0.98 | 1.0 | 1.00 | 0.9970 | ACCEPT |
| 5 | Manometry confirmed achalasia, IRP 22 mmHg | 0.97 | 1.0 | 1.00 | 0.9955 | ACCEPT |
| 6 | Laparoscopic Heller myotomy with Toupet fundoplication | 0.89 | **1.0** | 1.00 | **0.9835** | **ACCEPT (error, undetected)** |
| 7 | Discharged postop day 5, soft diet | 0.85 | **0.0** | 1.00 | **0.5275** | **REJECT** |

**Claim 3 error type:** negation-flip. Source stated patient *denied*
GERD history; claim asserted the opposite. Correctly caught.

**Claim 6 error type:** procedural-entity substitution. Source
documented a "Dor" fundoplication; claim said "Toupet" -- a distinct
surgical technique. **Not caught.** Lexical overlap remained above the
0.4 threshold despite the single-entity substitution, because
surrounding terminology ("laparoscopic," "Heller," "myotomy") dominated
the Jaccard score. No negation or numeric-drift rule applies to this
error type. This is the central disclosed limitation of the rule-based
Validator in this paper (Section 7).

**Claim 7 error type:** numeric/temporal drift. Source stated discharge
on day 2 with a full liquid diet; claim said day 5 with a soft diet.
Correctly caught via the numeric consistency check.

---

## Summary

- N = 2 cases, 15 claims total.
- 3 naturally-occurring errors observed (not authored/injected): 2
  negation-flips, 1 numeric/temporal drift, 1 procedural substitution.
- 2 of 3 errors correctly rejected by the Validator via the ACS formula.
- 1 of 3 (the procedural substitution) was missed, illustrating a
  genuine, disclosed boundary of lexical-overlap-based validation.
- This is a qualitative, fully-verified illustrative case study. It is
  not a statistically powered evaluation and does not support claims
  about a general error-catching rate. See Section 5.6 and Section 7 of
  the paper.
