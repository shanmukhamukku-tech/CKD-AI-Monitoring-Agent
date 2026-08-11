import pandas as pd
import os
from datetime import datetime
from logger import logger

CSV_FILE = "patient_records.csv"

EXPECTED_COLUMNS = ["Timestamp", "Patient_ID", "Age", "BP", "Creatinine", "Risk_Level", "CKD_Probability_%"]

def initialize_records_csv():
    needs_init = True
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        try:
            with open(CSV_FILE, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
            needs_init = first_line != ",".join(EXPECTED_COLUMNS)
        except Exception:
            needs_init = True

    if needs_init:
        # File is missing, empty, or missing its header (e.g. was created
        # before this check existed) - rebuild it with a proper header,
        # keeping any existing rows if they look like data rows.
        existing_rows = []
        if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
            try:
                with open(CSV_FILE, "r", encoding="utf-8") as f:
                    existing_rows = [line for line in f.read().splitlines() if line.strip()]
            except Exception:
                existing_rows = []

        with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
            f.write(",".join(EXPECTED_COLUMNS) + "\n")
            for line in existing_rows:
                f.write(line + "\n")
        logger.info("Initialized/repaired patient_records.csv header")

def save_patient_record(patient_id, age, bp, creatinine, risk_level, prob):
    initialize_records_csv()
    new_record = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Patient_ID": patient_id,
        "Age": age,
        "BP": bp,
        "Creatinine": creatinine,
        "Risk_Level": risk_level,
        "CKD_Probability_%": prob
    }
    df = pd.DataFrame([new_record])
    df.to_csv(CSV_FILE, mode='a', header=False, index=False)
    logger.info(f"Saved record for Patient ID: {patient_id}")

def get_all_records():
    initialize_records_csv()
    return pd.read_csv(CSV_FILE)