import streamlit as st
import pandas as pd
from predictor import CKDPredictor
from kidney_info import KidneyAgentKnowledge
from patient_records import save_patient_record, get_all_records

st.set_page_config(page_title="CKD AI Agent", page_icon="🩸", layout="wide")

st.title("🩸 Chronic Kidney Disease (CKD) AI Monitoring Agent")
st.markdown("Phase 2: Intelligent risk assessment, clinical recommendations, and patient logging.")

# Load Model
@st.cache_resource
def get_predictor():
    return CKDPredictor()

try:
    predictor = get_predictor()
except Exception as e:
    st.error(f"Failed to load ML models: {e}")
    st.stop()

tab1, tab2, tab3 = st.tabs(["🧪 Agent Assessment", "📋 Patient Records", "ℹ️ Clinical Reference"])

with tab1:
    st.subheader("Patient Clinical Data Input")

    col1, col2, col3 = st.columns(3)
    with col1:
        patient_id = st.text_input("Patient ID", value="PID-1001")
        age = st.number_input("Age", 1, 100, 50)
        bp = st.number_input("Blood Pressure (mmHg)", 50, 200, 80)
        sg = st.selectbox("Specific Gravity", [1.005, 1.010, 1.015, 1.020, 1.025], index=3)
        al = st.selectbox("Albumin (0 to 5)", [0, 1, 2, 3, 4, 5], index=0)
        su = st.selectbox("Sugar (0 to 5)", [0, 1, 2, 3, 4, 5], index=0)
        rbc = st.selectbox("Red Blood Cells", ["normal", "abnormal"], index=0)
        pc = st.selectbox("Pus Cell", ["normal", "abnormal"], index=0)
        pcc = st.selectbox("Pus Cell Clumps", ["notpresent", "present"], index=0)

    with col2:
        ba = st.selectbox("Bacteria", ["notpresent", "present"], index=0)
        bgr = st.number_input("Blood Glucose Random (mg/dL)", 50, 500, 120)
        bu = st.number_input("Blood Urea (mg/dL)", 10, 300, 36)
        sc = st.number_input("Serum Creatinine (mg/dL)", 0.4, 20.0, 1.2, step=0.1)
        sod = st.number_input("Serum Sodium (mEq/L)", 100, 180, 138)
        pot = st.number_input("Serum Potassium (mEq/L)", 2.0, 10.0, 4.4, step=0.1)
        hemo = st.number_input("Hemoglobin (g/dL)", 3.0, 20.0, 15.0, step=0.1)
        pcv = st.number_input("Packed Cell Volume", 10, 60, 44)
        wc = st.number_input("White Blood Cell Count", 2000, 25000, 7800)

    with col3:
        rc = st.number_input("Red Blood Cell Count", 2.0, 8.0, 5.2, step=0.1)
        htn = st.selectbox("Hypertension", ["no", "yes"], index=0)
        dm = st.selectbox("Diabetes Mellitus", ["no", "yes"], index=0)
        cad = st.selectbox("Coronary Artery Disease", ["no", "yes"], index=0)
        appet = st.selectbox("Appetite", ["good", "poor"], index=0)
        pe = st.selectbox("Pedal Edema", ["no", "yes"], index=0)
        ane = st.selectbox("Anemia", ["no", "yes"], index=0)

    # Encode categorical fields the same way they were encoded at training
    # time (alphabetical LabelEncoder order): abnormal=0/normal=1,
    # notpresent=0/present=1, no=0/yes=1, good=0/poor=1.
    binary_normal_abnormal = {"abnormal": 0, "normal": 1}
    binary_notpresent_present = {"notpresent": 0, "present": 1}
    binary_no_yes = {"no": 0, "yes": 1}
    binary_good_poor = {"good": 0, "poor": 1}

    if st.button("Run AI Agent Diagnosis", type="primary"):
        input_data = {
            "age": age, "bp": bp, "sg": sg, "al": al, "su": su,
            "rbc": binary_normal_abnormal[rbc],
            "pc": binary_normal_abnormal[pc],
            "pcc": binary_notpresent_present[pcc],
            "ba": binary_notpresent_present[ba],
            "bgr": bgr, "bu": bu, "sc": sc, "sod": sod, "pot": pot,
            "hemo": hemo, "pcv": pcv, "wc": wc, "rc": rc,
            "htn": binary_no_yes[htn],
            "dm": binary_no_yes[dm],
            "cad": binary_no_yes[cad],
            "appet": binary_good_poor[appet],
            "pe": binary_no_yes[pe],
            "ane": binary_no_yes[ane],
        }

        result = predictor.predict(input_data)
        risk = result["risk_level"]
        prob = result["probability"]

        st.markdown("---")
        st.subheader("Agent Diagnostic Output")

        m_col1, m_col2 = st.columns(2)
        with m_col1:
            if risk == "High Risk":
                st.error(f"**Risk Level**: {risk}")
            elif risk == "Moderate Risk":
                st.warning(f"**Risk Level**: {risk}")
            else:
                st.success(f"**Risk Level**: {risk}")
        with m_col2:
            st.metric("Estimated CKD Probability", f"{prob}%")

        # Recommendations
        st.markdown("### 🤖 Clinical Recommendations")
        recommendations = KidneyAgentKnowledge.generate_recommendations(risk, input_data)
        for rec in recommendations:
            st.write(f"- {rec}")

        # Save to records
        save_patient_record(patient_id, age, bp, sc, risk, prob)
        st.toast("Record saved to database!", icon="💾")

with tab2:
    st.subheader("Logged Patient History")
    df_records = get_all_records()
    if not df_records.empty:
        st.dataframe(df_records, use_container_width=True)
        csv_data = df_records.to_csv(index=False).encode('utf-8')
        st.download_button("Download Records CSV", csv_data, "patient_records.csv", "text/csv")
    else:
        st.info("No records logged yet.")

with tab3:
    st.markdown("""
    ### Normal Clinical Reference Ranges
    * **Serum Creatinine**: 0.6 – 1.2 mg/dL
    * **Blood Urea**: 7 – 20 mg/dL
    * **Hemoglobin**: 12.0 – 17.5 g/dL
    * **Blood Pressure**: < 120/80 mmHg
    * **Albumin (Urine)**: 0 (Negative)
    """)
