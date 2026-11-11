import streamlit as st
import pandas as pd
from ai_engine import run_privacy_agent, verify_redaction
from detector import detect_pii, merge_findings, redact_text

st.set_page_config(page_title="PrivacyLens", page_icon="🔒", layout="wide")

st.title("PrivacyLens")
st.caption("AI-powered sensitive information detection and redaction")
st.info("Local detection runs in Python. AI analysis sends text to Groq when enabled.")

uploaded = st.file_uploader("Upload a TXT file", type=["txt"])
manual_text = st.text_area("Or paste text here", height=160)

text = manual_text
if uploaded and not manual_text:
    text = uploaded.getvalue().decode("utf-8", errors="replace")

use_ai = st.checkbox("Enable AI Privacy Agent (sends text to Groq)", value=True)

if st.button("🔍 Scan for Privacy Risks", type="primary"):
    if not text.strip():
        st.warning("Enter some text first.")
    else:
        with st.spinner("PrivacyLens agent is analyzing your text..."):
            local = detect_pii(text)
            ai_report = None
            ai = []

            if use_ai:
                try:
                    ai_report = run_privacy_agent(text, local)
                    ai = ai_report.get("findings", [])
                except Exception as e:
                    st.error(f"AI Agent Error: {e}")
                    st.warning("Showing local detection results.")

            findings = merge_findings(text, local, ai)
            redacted = redact_text(text, findings)
            verification = None

            if ai_report:
                try:
                    verification = verify_redaction(redacted)
                except Exception as e:
                    st.warning(f"Verification unavailable: {e}")

        st.session_state["results"] = {
            "findings": findings,
            "redacted": redacted,
            "ai_report": ai_report,
            "verification": verification
        }

if "results" in st.session_state:
    results = st.session_state["results"]
    findings = results["findings"]
    ai_report = results.get("ai_report")

    st.divider()

    if ai_report:
        st.subheader("🤖 AI Privacy Agent Report")
        st.metric("Overall Privacy Risk", ai_report.get("risk_level", "Unknown"))
        st.write(ai_report.get("risk_summary", ""))

        st.markdown("**Privacy Recommendations**")
        for recommendation in ai_report.get("recommendations", []):
            st.write("•", recommendation)

    col1, col2 = st.columns(2)
    col1.metric("Sensitive fields detected", len(findings))
    col2.metric("PII categories", len(set(x["label"] for x in findings)))

    st.subheader("Detection Results")

    if findings:
        st.dataframe(
            pd.DataFrame(findings)[["text", "label"]],
            hide_index=True,
            use_container_width=True
        )
    else:
        st.success("No supported PII patterns detected.")

    st.subheader("Redacted Text")
    st.code(results["redacted"], language=None)
    

    verification = results.get("verification")

    if verification:
       st.subheader("AI Redaction Verification")

       if verification.get("safe"):
           st.success("No remaining PII detected by the AI verifier.")
       else:
            st.warning("Potential sensitive information remains.")

       st.write(verification.get("message", ""))

       if verification.get("remaining_entities"):
        st.write(verification["remaining_entities"])

    st.download_button(
    "⬇ Download Redacted Text",
    data=results["redacted"],
    file_name="redacted.txt",
    mime="text/plain",
    key="download_redacted"
)

 
st.caption("Prototype only: undetected PII may remain. Review output before sharing.")
