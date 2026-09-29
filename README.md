# 🛡️ ScamShield

**Scam, phishing, suspicious URL and QR-code risk analyzer built with Python and Streamlit.**

ScamShield is a student cybersecurity project that analyzes common warning signs in SMS/messages, emails, URLs and QR-code contents.

## ✨ Features

- 📱 SMS / message scam detection
- 📧 Email scam detection
- 🔗 Suspicious URL analysis
- 📷 QR-code scanning and analysis
- 📊 Risk score from 0–100
- 🟢 Low / 🟠 Medium / 🔴 High risk levels
- 🧠 Explainable rule-based detection
- 📋 Recent scan history
- 🎨 Clean Streamlit interface
- 💻 Runs locally

## 🛠️ Technology

- Python
- Streamlit
- OpenCV
- NumPy
- Pillow
- Pandas
- Regular expressions
- URL parsing

## 🚀 How to Run

### 1. Install Python

Use Python 3.11, 3.12 or 3.13.

### 2. Open the project folder

Open Command Prompt / PowerShell inside the `ScamShield` folder.

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate it on Windows

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

Your browser should open the ScamShield application.

## 📁 Project Structure

```text
ScamShield/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── modules/
    ├── __init__.py
    ├── analyzers.py
    └── qr_scanner.py
```

## 🔍 How Detection Works

ScamShield currently uses transparent rule-based indicators.

Examples include:

- OTP / PIN / password requests
- Urgent or threatening language
- Prize and lottery claims
- Financial/KYC language
- Suspicious URL structures
- URL shorteners
- IP-address URLs
- Excessively long URLs
- Suspicious URL terms
- QR codes containing suspicious links

The score is an indicator, not proof that content is malicious or safe.

## ⚠️ Disclaimer

This project is for **educational and awareness purposes**. It does not guarantee that a message, URL, QR code or email is safe or fraudulent.

Never share OTPs, UPI PINs, passwords, CVV or other authentication secrets with someone who asks for them.

## 🔮 Future Improvements

Possible future versions can add:

- Machine-learning based classification
- Multilingual scam detection
- Screenshot analysis
- Browser extension
- Database of reported scam domains
- User accounts and scan history database
- Voice-call transcript analysis
- Hindi and Marathi support

## 👩‍💻 Author

Add your name and GitHub profile here.
