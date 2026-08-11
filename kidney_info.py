class KidneyAgentKnowledge:
    @staticmethod
    def generate_recommendations(risk_level: str, metrics: dict) -> list:
        recommendations = []
        
        # Risk-based advice
        if risk_level == "High Risk":
            recommendations.append("🚨 **Immediate Action Required**: Schedule an urgent consultation with a Nephrologist.")
            recommendations.append("🔬 **Diagnostic Tests**: Confirm with Serum Creatinine, eGFR, Blood Urea Nitrogen (BUN), and 24-hr Urine Protein test.")
            recommendations.append("💊 **Medication Advice**: Avoid NSAIDs (e.g., Ibuprofen, Naproxen) and nephrotoxic medications without doctor approval.")
        elif risk_level == "Moderate Risk":
            recommendations.append("⚠️ **Follow-up Needed**: Consult a general physician or renal specialist within 1-2 weeks.")
            recommendations.append("📊 **Monitoring**: Retest kidney function parameters (eGFR & Albumin) in 30 days.")
            recommendations.append("🥗 **Dietary Adjustments**: Consider a low-sodium, controlled-protein diet.")
        else:
            recommendations.append("✅ **Low Risk Detected**: Maintain routine annual wellness checkups.")
            recommendations.append("💧 **Hydration**: Drink 2–2.5 liters of water daily unless restricted by a clinician.")

        # Specific Biomarker Trigger Rules
        if metrics.get("sc", 0) > 1.2:
            recommendations.append("⚠️ **Elevated Serum Creatinine**: Indicates potential decline in glomerular filtration rate.")
        if metrics.get("bp", 0) >= 140:
            recommendations.append("🩸 **Hypertension Alert**: Blood pressure ≥140 mmHg strictly accelerates kidney damage. Maintain BP < 130/80 mmHg.")
        if metrics.get("al", 0) > 0:
            recommendations.append("🧪 **Proteinuria Warning**: Protein in urine detected (Albumin > 0). Follow up with a Quantitative Urine Albumin-to-Creatinine Ratio (UACR).")
        if metrics.get("hemo", 15) < 11:
            recommendations.append("🩸 **Anemia Screening**: Low hemoglobin observed. Evaluate for renal anemia or iron deficiency.")

        return recommendations