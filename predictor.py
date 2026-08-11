import joblib
import pandas as pd
import numpy as np
import os
from logger import logger


class CKDPredictor:
    def __init__(self, model_dir=None):
        # Resolve absolute path to THIS folder (the .pkl files live next to
        # this script, not in a "models" subfolder).
        if model_dir is None:
            self.model_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            self.model_dir = model_dir

        self.load_artifacts()

    def load_artifacts(self):
        try:
            model_path = os.path.join(self.model_dir, "best_ckd_model.pkl")
            scaler_path = os.path.join(self.model_dir, "scaler.pkl")
            cols_path = os.path.join(self.model_dir, "feature_columns.pkl")
            le_path = os.path.join(self.model_dir, "label_encoder.pkl")

            logger.info(f"Loading model from: {model_path}")

            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.feature_columns = joblib.load(cols_path)
            self.label_encoder = joblib.load(le_path)

            # The target was label-encoded (e.g. 'ckd' -> 0, 'notckd' -> 1).
            # Work out which encoded value actually means "ckd" instead of
            # assuming it's always index 1 - that assumption was wrong here
            # and was silently flipping every risk score.
            ckd_encoded_value = self.label_encoder.transform(["ckd"])[0]
            self.ckd_class_index = list(self.model.classes_).index(ckd_encoded_value)

            logger.info(
                f"Artifacts loaded successfully. CKD corresponds to "
                f"model.classes_ index {self.ckd_class_index}."
            )
        except Exception as e:
            logger.error(f"Error loading artifacts: {e}")
            raise e

    def predict(self, input_data: dict):
        df = pd.DataFrame([input_data])

        # Reorder and align columns; anything the model expects but the UI
        # didn't collect gets filled with 0.
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0
        df = df[self.feature_columns]

        # Scale features
        scaled_data = self.scaler.transform(df)

        # Predict class and probabilities
        prediction = self.model.predict(scaled_data)[0]
        probabilities = self.model.predict_proba(scaled_data)[0]

        ckd_prob = (
            probabilities[self.ckd_class_index]
            if len(probabilities) > 1
            else float(prediction)
        )

        if ckd_prob >= 0.70:
            risk_level = "High Risk"
        elif ckd_prob >= 0.35:
            risk_level = "Moderate Risk"
        else:
            risk_level = "Low Risk"

        return {
            "prediction": int(prediction),
            "probability": round(ckd_prob * 100, 2),
            "risk_level": risk_level,
        }
