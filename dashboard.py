import pandas as pd
import streamlit as st
import plotly.express as px

from src.main import load_logs_from_csv
from src.incident_engine import analyze_incident
from src.xai_explainer import explain_incident

st.set_page_config(page_title="AutoRCA Pro Max", layout="wide")
st.title("🚨 AutoRCA Pro Max")
st.caption("Explainable ML-assisted Production Root Cause Analysis")

logs = load_logs_from_csv("data/sample_logs.csv")
result = analyze_incident(logs)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Logs", result["total_logs"])
c2.metric("Dominant Category", result["dominant_category"])
c3.metric("Affected Service", result["most_affected_service"])
c4.metric("Likely Root Cause", result["likely_root_cause"])

left, right = st.columns(2)

with left:
    st.subheader("Failure Categories")
    df_cat = pd.DataFrame(
        result["category_counts"].items(), columns=["Category", "Count"]
    )
    st.plotly_chart(px.bar(df_cat, x="Category", y="Count"), use_container_width=True)

with right:
    st.subheader("Affected Services")
    df_srv = pd.DataFrame(
        result["service_counts"].items(), columns=["Service", "Errors"]
    )
    st.plotly_chart(px.bar(df_srv, x="Service", y="Errors"), use_container_width=True)

st.subheader("Root Cause Ranking")
st.dataframe(pd.DataFrame(result["root_cause_candidates"]), use_container_width=True)

st.subheader("Explainable RCA")
for text in explain_incident(result):
    st.write("• " + text)

st.subheader("Anomalous / Important Logs")
log_df = pd.DataFrame(result["logs"])
st.dataframe(
    log_df[["timestamp", "service", "category", "message", "anomaly_score", "is_anomaly"]],
    use_container_width=True,
)

st.info(
    "Scores are ranking signals, not calibrated probabilities. "
    "For real production use, connect validated logs, traces, metrics and service topology."
)
