"""
Synthetic clinical vignette set for the Asymmetric Agentic Network POC.

Design notes (for paper Methods/Limitations section):
- Vignettes are SYNTHETIC, not drawn from MIMIC-IV directly (MIMIC-IV access is
  credentialed/restricted). They are structurally modeled on the documented
  format of MIMIC-IV-Note discharge summaries: multi-section narrative covering
  admission events, clinical course, interventions, and discharge recommendations,
  with heterogeneous (non-templated) phrasing -- consistent with the structural
  description in Noori et al. (2025) and Damm et al. (2024).
- Each vignette has a "ground_truth_entities" list (what a correct extractor
  should output) and is paired with a "candidate_extraction" that an Extractor
  LLM (Claude, acting in-role) actually produced after reading ONLY the note text.
- Half the candidate extractions will contain a genuine, unprompted hallucination
  (the Extractor is not told which ones), and half should be clean -- this is
  determined empirically by running the extraction, not pre-decided.
- error_type taxonomy follows the categories used in clinical hallucination
  literature cited in the paper: faithfulness hallucination (fabrication),
  negation-flip error, temporal misalignment, and dosage/numeric fabrication.
"""

VIGNETTES = [
    {
        "id": "V01",
        "note": (
            "Admission Note: 67-year-old male admitted with acute decompensated heart failure. "
            "History of hypertension and type 2 diabetes mellitus. No history of myocardial infarction. "
            "On admission, started on furosemide 40 mg IV twice daily. Echocardiogram showed ejection "
            "fraction of 30%. Patient improved with diuresis and was transitioned to oral furosemide 20 mg "
            "daily prior to discharge. Discharge medications include lisinopril 10 mg daily, metformin "
            "500 mg twice daily, and furosemide 20 mg daily."
        ),
    },
    {
        "id": "V02",
        "note": (
            "Progress Note, Day 3: Patient with community-acquired pneumonia, currently afebrile for 24 hours. "
            "No known drug allergies. Denies penicillin allergy. Continues on ceftriaxone 1g IV daily, day 3 of "
            "a planned 7-day course. Family history notable for father with COPD. Plan to transition to oral "
            "antibiotics once clinically stable."
        ),
    },
    {
        "id": "V03",
        "note": (
            "Discharge Summary: Patient presented with new-onset atrial fibrillation, rate-controlled with "
            "metoprolol. Started on apixaban 5 mg twice daily for stroke prophylaxis given CHA2DS2-VASc score "
            "of 3. No history of prior stroke or transient ischemic attack. Patient does not smoke. Discharged "
            "in stable condition with cardiology follow-up in two weeks."
        ),
    },
    {
        "id": "V04",
        "note": (
            "History and Physical: 54-year-old female with chronic kidney disease stage 3, presenting with "
            "hyperkalemia, potassium 6.2 mmol/L on admission labs drawn at 0300. Treated with calcium "
            "gluconate, insulin/dextrose, and sodium polystyrene sulfonate. Repeat potassium at 0900 same day "
            "was 4.8 mmol/L. No history of dialysis. Nephrology consulted."
        ),
    },
    {
        "id": "V05",
        "note": (
            "Discharge Summary: Patient admitted for cellulitis of the left lower extremity, treated with "
            "vancomycin, later narrowed to cefazolin 2g IV every 8 hours once cultures returned negative for "
            "MRSA. No history of intravenous drug use. Discharged on oral cephalexin 500 mg four times daily "
            "for a total 10-day course, with 4 days completed inpatient."
        ),
    },
    {
        "id": "V06",
        "note": (
            "Admission Note: Patient with known seizure disorder on levetiracetam 1000 mg twice daily, "
            "admitted after a breakthrough seizure witnessed by family. Denies missed doses. No history of "
            "alcohol use disorder. EEG pending. Neurology following."
        ),
    },
    {
        "id": "V07",
        "note": (
            "Progress Note: Patient post-operative day 2 from laparoscopic cholecystectomy, pain well "
            "controlled on oral oxycodone 5 mg every 6 hours as needed. Tolerating regular diet. No fever. "
            "Surgical drains were not placed during this procedure. Ambulating independently."
        ),
    },
    {
        "id": "V08",
        "note": (
            "Discharge Summary: 72-year-old male with COPD exacerbation, treated with prednisone 40 mg daily "
            "for a 5-day course and nebulized albuterol/ipratropium. Influenza and COVID-19 testing negative. "
            "Home oxygen requirement unchanged at 2L nasal cannula. No history of intubation during this or "
            "prior admissions."
        ),
    },
    {
        "id": "V09",
        "note": (
            "Admission Note: Patient with type 1 diabetes mellitus admitted with diabetic ketoacidosis, "
            "initial glucose 480 mg/dL, anion gap 22. Started on IV insulin infusion per DKA protocol. "
            "No history of insulin pump use; patient uses multiple daily injections at home with insulin "
            "glargine and insulin lispro."
        ),
    },
    {
        "id": "V10",
        "note": (
            "Discharge Summary: Patient with deep vein thrombosis of the right popliteal vein, confirmed by "
            "ultrasound, started on rivaroxaban 15 mg twice daily for 21 days, then to transition to 20 mg "
            "once daily. No history of prior venous thromboembolism. No known malignancy on review of systems."
        ),
    },
    {
        "id": "V11",
        "note": (
            "Progress Note: Patient with acute pancreatitis, likely gallstone-related per right upper quadrant "
            "ultrasound findings. NPO initially, advanced to clear liquids on hospital day 2 once pain improved "
            "and lipase trended down from 1200 to 310 U/L. No history of alcohol use. Surgery consulted for "
            "consideration of cholecystectomy after recovery."
        ),
    },
    {
        "id": "V12",
        "note": (
            "Discharge Summary: 45-year-old male with major depressive disorder, admitted electively for "
            "medication adjustment. Sertraline increased from 50 mg to 100 mg daily during admission. No "
            "history of suicide attempts. Denies current suicidal ideation at discharge. Outpatient "
            "psychiatry follow-up arranged within one week."
        ),
    },
]

if __name__ == "__main__":
    print(f"Total vignettes: {len(VIGNETTES)}")
    for v in VIGNETTES:
        print(f"{v['id']}: {len(v['note'].split())} words")
