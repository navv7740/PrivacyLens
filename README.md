# PrivacyLens
### AI-Powered PII Detection and Privacy Protection

PrivacyLens is a privacy-focused application that detects Personally Identifiable Information (PII) in text and helps users redact sensitive information using a combination of rule-based detection and Generative AI.

It uses an agentic AI workflow to analyze privacy risks, identify sensitive entities, redact them, and verify the redacted output.

## Features

- **PII Detection:** Detects names, phone numbers, email addresses, dates of birth, addresses, identification numbers, and other sensitive information.
- **Rule-Based Detection:** Uses Python regular expressions for local detection.
- **AI Privacy Agent:** Uses Groq-hosted LLMs for contextual PII detection and privacy risk assessment.
- **Automated Redaction:** Replaces detected sensitive information with labels such as `[PHONE]`, `[EMAIL]`, and `[ADDRESS]`.
- **Redaction Verification:** Uses AI to check whether sensitive information remains in the redacted text.
- **Privacy Recommendations:** Provides suggestions based on the detected privacy risks.
- **Download Results:** Allows users to download the redacted text.

## Tech Stack

- Python
- Streamlit
- Groq API
- Generative AI
- Regular Expressions
- Pandas

## Project Structure

```text
PrivacyLens/
│
├── app.py
├── ai_engine.py
├── detector.py
├── evaluate.py
├── requirements.txt
├── .gitignore
│
└── data/
    └── privacylens_pii_dataset.csv
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/navv7740/PrivacyLens.git
```

### 2. Navigate to the project directory

```bash
cd PrivacyLens
```

### 3. Create a virtual environment

```bash
py -m venv .venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the Groq API key

Get an API key from [Groq Console](https://console.groq.com/keys).

Set it in your PowerShell terminal:

```powershell
$env:GROQ_API_KEY = "your_groq_api_key"
```

Replace `your_groq_api_key` with your actual API key.

**Important:** Never upload your API key to GitHub or share it publicly.

### 7. Run PrivacyLens

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## Usage

1. Open PrivacyLens in your browser.
2. Paste text or upload a `.txt` file.
3. Enable the AI Privacy Agent for contextual analysis.
4. Scan the text to identify sensitive information.
5. Review detected PII and the privacy risk assessment.
6. Download the redacted output.
7. Check the AI verification results.

## Privacy Note

- Rule-based detection runs locally.
- When the AI Privacy Agent is enabled, input text is sent to the Groq API for analysis.
- Avoid using real personal or confidential information when testing.
- AI verification may produce false positives or false negatives and does not guarantee complete removal of all sensitive information.

## Author

Developed as a project exploring Generative AI, Agentic AI, and automated privacy protection.

**GitHub:** [@navv7740](https://github.com/navv7740)
