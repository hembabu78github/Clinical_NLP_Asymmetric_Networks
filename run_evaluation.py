"""
Run the Deterministic Validator against the full Synthetic Perturbation
Evaluation dataset (claims.py / vignettes.py) and report real metrics.

No numbers in this script's output are pre-decided -- this is the actual
evaluation run referenced in the paper's results.
"""

from vignettes import VIGNETTES
from claims import CLAIMS
from validator import validate

notes_by_id = {v["id"]: v["note"] for v in VIGNETTES}

rows = []
for vid, claim_list in CLAIMS.items():
    source = notes_by_id[vid]
    for c in claim_list:
        result = validate(c["claim"], source)
        predicted_label = "clean" if result["v_fact"] == 1.0 else "perturbed"
        rows.append({
            "vignette": vid,
            "claim": c["claim"],
            "true_label": c["label"],
            "perturbation_type": c.get("perturbation_type", "-"),
            "predicted_label": predicted_label,
            "lexical_overlap": result["lexical_overlap"],
            "negation_consistent": result["negation_consistent"],
            "numeric_consistent": result["numeric_consistent"],
            "correct": predicted_label == c["label"],
        })

# ---- Aggregate metrics ----
tp = sum(1 for r in rows if r["true_label"] == "perturbed" and r["predicted_label"] == "perturbed")
fn = sum(1 for r in rows if r["true_label"] == "perturbed" and r["predicted_label"] == "clean")
tn = sum(1 for r in rows if r["true_label"] == "clean" and r["predicted_label"] == "clean")
fp = sum(1 for r in rows if r["true_label"] == "clean" and r["predicted_label"] == "perturbed")

total = len(rows)
accuracy = (tp + tn) / total
precision = tp / (tp + fp) if (tp + fp) > 0 else float("nan")
recall = tp / (tp + fn) if (tp + fn) > 0 else float("nan")
f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else float("nan")
specificity = tn / (tn + fp) if (tn + fp) > 0 else float("nan")

print("=" * 70)
print("SYNTHETIC PERTURBATION EVALUATION -- Validator Performance")
print("=" * 70)
print(f"Total claims evaluated: {total}  (clean={tp+fn+0 if False else sum(1 for r in rows if r['true_label']=='clean')}, perturbed={sum(1 for r in rows if r['true_label']=='perturbed')})")
print(f"Confusion matrix:")
print(f"  TP (perturbed correctly flagged): {tp}")
print(f"  FN (perturbed missed, false negative): {fn}")
print(f"  TN (clean correctly passed):      {tn}")
print(f"  FP (clean incorrectly flagged):   {fp}")
print()
print(f"Accuracy:    {accuracy:.3f}")
print(f"Precision:   {precision:.3f}  (of claims flagged as perturbed, fraction truly perturbed)")
print(f"Recall:      {recall:.3f}  (of truly perturbed claims, fraction caught)")
print(f"Specificity: {specificity:.3f}  (of truly clean claims, fraction correctly passed)")
print(f"F1 score:    {f1:.3f}")
print()

# ---- Breakdown by perturbation type ----
print("-" * 70)
print("Recall by perturbation type (i.e., detection rate per error category):")
ptypes = sorted(set(r["perturbation_type"] for r in rows if r["perturbation_type"] != "-"))
for pt in ptypes:
    sub = [r for r in rows if r["perturbation_type"] == pt]
    caught = sum(1 for r in sub if r["predicted_label"] == "perturbed")
    print(f"  {pt:18s}: {caught}/{len(sub)} caught")

print()
print("-" * 70)
print("Misclassified rows (errors made by the rule-based Validator):")
errors = [r for r in rows if not r["correct"]]
if not errors:
    print("  (none)")
else:
    for r in errors:
        print(f"  [{r['vignette']}] true={r['true_label']:9s} pred={r['predicted_label']:9s} "
              f"type={r['perturbation_type']:14s} lex={r['lexical_overlap']:.2f} "
              f"neg_ok={r['negation_consistent']} num_ok={r['numeric_consistent']}  "
              f"claim=\"{r['claim']}\"")
