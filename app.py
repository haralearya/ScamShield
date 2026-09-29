import streamlit as st
from modules.analyzers import analyze_text, analyze_url
from modules.qr_scanner import scan_qr

st.set_page_config(
    page_title="ScamShield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.main {background: #f7f9fc;}
.block-container {padding-top: 2rem;}
.hero {
    padding: 28px;
    border-radius: 18px;
    background: linear-gradient(135deg,#0f172a,#1e3a8a);
    color: white;
    margin-bottom: 24px;
}
.hero h1 {font-size: 42px; margin-bottom: 5px;}
.hero p {font-size: 17px; opacity: .9;}
.card {
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    background: white;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

def show_result(result):
    score = result["score"]
    level = result["level"]
    reasons = result["reasons"]

    if level == "LOW":
        st.success(f"🟢 LOW RISK — Score: {score}/100")
    elif level == "MEDIUM":
        st.warning(f"🟠 MEDIUM RISK — Score: {score}/100")
    else:
        st.error(f"🔴 HIGH RISK — Score: {score}/100")

    st.progress(score / 100)

    st.subheader("Why was it flagged?")
    if reasons:
        for r in reasons:
            st.write("• " + r)
    else:
        st.write("No major suspicious indicators were detected.")

    st.info(result["advice"])

    st.session_state.history.insert(0, {
        "Type": result["type"],
        "Risk": level,
        "Score": score
    })
    st.session_state.history = st.session_state.history[:10]

st.markdown("""
<div class="hero">
<h1>🛡️ ScamShield</h1>
<p>Scam, phishing, suspicious URL and QR-code risk analyzer</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🛡️ ScamShield")
    st.write("Choose what you want to analyze.")
    mode = st.radio(
        "Analyzer",
        ["📱 SMS / Message", "📧 Email", "🔗 URL", "📷 QR Code", "📊 Scan History", "ℹ️ About"]
    )
    st.divider()
    st.caption("Educational cybersecurity project. Results are indicators, not a guarantee.")

if mode == "📱 SMS / Message":
    st.header("📱 SMS / Message Scam Detector")
    st.write("Paste an SMS, WhatsApp-style message, or other text.")
    text = st.text_area(
        "Message",
        height=220,
        placeholder="Example: Your bank account will be blocked today. Send your OTP to verify..."
    )
    if st.button("🔍 Analyze Message", type="primary"):
        if not text.strip():
            st.warning("Please enter a message first.")
        else:
            show_result(analyze_text(text, "SMS / Message"))

elif mode == "📧 Email":
    st.header("📧 Email Scam Detector")
    st.write("Paste the email subject and body.")
    email = st.text_area(
        "Email",
        height=260,
        placeholder="Subject: Urgent KYC verification required\n\nDear customer, your account..."
    )
    if st.button("🔍 Analyze Email", type="primary"):
        if not email.strip():
            st.warning("Please enter an email first.")
        else:
            show_result(analyze_text(email, "Email"))

elif mode == "🔗 URL":
    st.header("🔗 Suspicious URL Checker")
    url = st.text_input(
        "Website URL",
        placeholder="https://example.com/login"
    )
    if st.button("🔍 Analyze URL", type="primary"):
        if not url.strip():
            st.warning("Please enter a URL first.")
        else:
            result = analyze_url(url)
            show_result(result)

elif mode == "📷 QR Code":
    st.header("📷 QR Code Scanner")
    st.write("Upload an image containing a QR code. ScamShield will decode it and analyze the extracted content.")
    image = st.file_uploader("Upload QR image", type=["png", "jpg", "jpeg", "webp"])
    if image:
        st.image(image, caption="Uploaded QR image", width=300)
        if st.button("🔍 Scan QR Code", type="primary"):
            result = scan_qr(image)
            if not result["decoded"]:
                st.error("❌ No readable QR code was detected in this image.")
            else:
                st.success("✅ QR code detected.")
                st.code(result["data"])
                if result["is_url"]:
                    show_result(analyze_url(result["data"], "QR Code"))
                else:
                    show_result(analyze_text(result["data"], "QR Code"))

elif mode == "📊 Scan History":
    st.header("📊 Recent Scan History")
    if not st.session_state.history:
        st.info("No scans yet. Your results will appear here during this session.")
    else:
        st.dataframe(st.session_state.history, use_container_width=True)
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()

elif mode == "ℹ️ About":
    st.header("ℹ️ About ScamShield")
    st.markdown("""
**ScamShield** is a student cybersecurity project designed to identify common warning signs in:

- SMS and messages
- Emails
- Website URLs
- QR-code contents

### How it works
ScamShield uses a transparent **rule-based risk engine**. It checks for indicators such as OTP/PIN requests, urgent language, suspicious URL structures, shortened links, fake prize claims and other common scam patterns.

### Risk levels
- 🟢 **0–29:** Low risk indicators
- 🟠 **30–59:** Medium risk indicators
- 🔴 **60–100:** High risk indicators

### Important
A result is an indicator, not proof that a message or website is safe or fraudulent. Never share OTPs, UPI PINs, passwords or card security codes with someone who asks for them.
""")
    st.success("Project ready for GitHub 🚀")
