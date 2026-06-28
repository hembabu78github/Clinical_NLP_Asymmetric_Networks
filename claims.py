"""
Synthetic Perturbation Evaluation dataset.

For each of the 12 vignettes (vignettes.py), this file defines a set of
clinical claims, each labeled:
    - label = "clean"      : claim is directly and correctly supported by the note
    - label = "perturbed"  : claim has been deliberately corrupted

Each perturbed claim carries an explicit perturbation_type, drawn from the
hallucination taxonomy used in the paper's Related Work section:
    - "negation_flip"   : an asserted/negated fact in the note is reversed
    - "numeric_drift"   : a dose, lab value, or duration is altered
    - "temporal_shift"  : a timing/sequence relationship is altered
    - "fabrication"     : a fact is invented with no basis in the note

This is a controlled adversarial test of the Validator component only.
No LLM-generated extraction is used as the source of error here -- all
perturbations are authored explicitly and labeled, satisfying the
"Synthetic Perturbation Evaluation" design discussed in the paper's
Section 4 methodology.
"""

CLAIMS = {
    "V01": [
        {"claim": "Patient has a history of hypertension.", "label": "clean"},
        {"claim": "Patient has no history of myocardial infarction.", "label": "clean"},
        {"claim": "Echocardiogram showed an ejection fraction of 30%.", "label": "clean"},
        {"claim": "Discharge dose of furosemide is 20 mg daily.", "label": "clean"},
        {"claim": "Patient has a history of myocardial infarction.", "label": "perturbed", "perturbation_type": "negation_flip"},
        {"claim": "Discharge dose of furosemide is 200 mg daily.", "label": "perturbed", "perturbation_type": "numeric_drift"},
    ],
    "V02": [
        {"claim": "Patient denies penicillin allergy.", "label": "clean"},
        {"claim": "Patient is on ceftriaxone 1g IV daily.", "label": "clean"},
        {"claim": "Patient's father has a history of COPD.", "label": "clean"},
        {"claim": "Patient has a confirmed penicillin allergy.", "label": "perturbed", "perturbation_type": "negation_flip"},
        {"claim": "Ceftriaxone course is planned for 17 days.", "label": "perturbed", "perturbation_type": "numeric_drift"},
    ],
    "V03": [
        {"claim": "Patient was started on apixaban 5 mg twice daily.", "label": "clean"},
        {"claim": "Patient has no history of prior stroke or TIA.", "label": "clean"},
        {"claim": "CHA2DS2-VASc score is 3.", "label": "clean"},
        {"claim": "Patient has a history of prior stroke.", "label": "perturbed", "perturbation_type": "negation_flip"},
        {"claim": "Cardiology follow-up is scheduled in two days.", "label": "perturbed", "perturbation_type": "temporal_shift"},
    ],
    "V04": [
        {"claim": "Admission potassium was 6.2 mmol/L.", "label": "clean"},
        {"claim": "Patient has no history of dialysis.", "label": "clean"},
        {"claim": "Repeat potassium at 0900 was 4.8 mmol/L.", "label": "clean"},
        {"claim": "Admission potassium was 2.6 mmol/L.", "label": "perturbed", "perturbation_type": "numeric_drift"},
        {"claim": "Repeat potassium was drawn at 0900 the day before admission.", "label": "perturbed", "perturbation_type": "temporal_shift"},
    ],
    "V05": [
        {"claim": "Cultures returned negative for MRSA.", "label": "clean"},
        {"claim": "Patient has no history of intravenous drug use.", "label": "clean"},
        {"claim": "Patient was narrowed to cefazolin 2g IV every 8 hours.", "label": "clean"},
        {"claim": "Cultures returned positive for MRSA.", "label": "perturbed", "perturbation_type": "negation_flip"},
        {"claim": "Patient has a documented history of intravenous drug use.", "label": "perturbed", "perturbation_type": "fabrication"},
    ],
    "V06": [
        {"claim": "Seizure was witnessed by family.", "label": "clean"},
        {"claim": "Patient has no history of alcohol use disorder.", "label": "clean"},
        {"claim": "Levetiracetam dose is 1000 mg twice daily.", "label": "clean"},
        {"claim": "Seizure was unwitnessed.", "label": "perturbed", "perturbation_type": "negation_flip"},
        {"claim": "Levetiracetam dose is 100 mg twice daily.", "label": "perturbed", "perturbation_type": "numeric_drift"},
    ],
    "V07": [
        {"claim": "Surgical drains were not placed during the procedure.", "label": "clean"},
        {"claim": "Patient is tolerating a regular diet.", "label": "clean"},
        {"claim": "Oxycodone is dosed at 5 mg every 6 hours as needed.", "label": "clean"},
        {"claim": "A surgical drain was placed and is draining serosanguinous fluid.", "label": "perturbed", "perturbation_type": "fabrication"},
        {"claim": "Oxycodone is dosed at 50 mg every 6 hours as needed.", "label": "perturbed", "perturbation_type": "numeric_drift"},
    ],
    "V08": [
        {"claim": "Prednisone is dosed at 40 mg daily for a 5-day course.", "label": "clean"},
        {"claim": "Patient has no history of intubation.", "label": "clean"},
        {"claim": "Home oxygen requirement is 2L nasal cannula.", "label": "clean"},
        {"claim": "Patient has a history of intubation during a prior admission.", "label": "perturbed", "perturbation_type": "negation_flip"},
        {"claim": "Home oxygen requirement is 8L nasal cannula.", "label": "perturbed", "perturbation_type": "numeric_drift"},
    ],
    "V09": [
        {"claim": "Initial glucose was 480 mg/dL.", "label": "clean"},
        {"claim": "Patient has no history of insulin pump use.", "label": "clean"},
        {"claim": "Anion gap was 22.", "label": "clean"},
        {"claim": "Patient has a history of insulin pump use.", "label": "perturbed", "perturbation_type": "negation_flip"},
        {"claim": "Initial glucose was 48 mg/dL.", "label": "perturbed", "perturbation_type": "numeric_drift"},
    ],
    "V10": [
        {"claim": "DVT was confirmed by ultrasound.", "label": "clean"},
        {"claim": "Patient has no history of prior venous thromboembolism.", "label": "clean"},
        {"claim": "Rivaroxaban is dosed at 15 mg twice daily for 21 days initially.", "label": "clean"},
        {"claim": "DVT was confirmed by CT venogram.", "label": "perturbed", "perturbation_type": "fabrication"},
        {"claim": "Patient has a known malignancy.", "label": "perturbed", "perturbation_type": "negation_flip"},
    ],
    "V11": [
        {"claim": "Lipase improved from 1200 to 310 U/L.", "label": "clean"},
        {"claim": "Patient has no history of alcohol use.", "label": "clean"},
        {"claim": "Patient was advanced to clear liquids on hospital day 2.", "label": "clean"},
        {"claim": "Lipase improved from 120 to 31 U/L.", "label": "perturbed", "perturbation_type": "numeric_drift"},
        {"claim": "Patient was advanced to clear liquids on hospital day 5.", "label": "perturbed", "perturbation_type": "temporal_shift"},
    ],
    "V12": [
        {"claim": "Sertraline was increased from 50 mg to 100 mg daily.", "label": "clean"},
        {"claim": "Patient has no history of suicide attempts.", "label": "clean"},
        {"claim": "Patient denies current suicidal ideation at discharge.", "label": "clean"},
        {"claim": "Patient has a history of a prior suicide attempt.", "label": "perturbed", "perturbation_type": "negation_flip"},
        {"claim": "Outpatient psychiatry follow-up is arranged within six months.", "label": "perturbed", "perturbation_type": "temporal_shift"},
    ],
}

if __name__ == "__main__":
    total = sum(len(v) for v in CLAIMS.values())
    clean = sum(1 for v in CLAIMS.values() for c in v if c["label"] == "clean")
    perturbed = sum(1 for v in CLAIMS.values() for c in v if c["label"] == "perturbed")
    print(f"Total claims: {total} | clean: {clean} | perturbed: {perturbed}")
