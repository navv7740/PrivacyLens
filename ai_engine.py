import os
import json
from groq import Groq

MODEL = "openai/gpt-oss-120b"


def get_client():
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if not key:
        raise ValueError("GROQ_API_KEY is not configured.")
    return Groq(api_key=key)


def run_privacy_agent(text, local_findings):
    client = get_client()

    prompt = f"""
Identify sensitive information in this text.

Categories: PERSON, ADDRESS, PHONE, EMAIL, DOB, ID_NUMBER.

Existing findings:
{json.dumps(local_findings)}

Return only a valid JSON object.
Entity text must be copied exactly from the input.
Do not invent information.

Format:
{{
  "entities": [],
  "risk_level": "High",
  "risk_summary": "Brief explanation",
  "recommendations": ["Advice 1", "Advice 2", "Advice 3"]
}}

TEXT:
{text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_completion_tokens=3000,
        response_format={"type": "json_object"}
    )

    result = json.loads(response.choices[0].message.content)
    findings = []

    for item in result.get("entities", []):
        value = item.get("text", "")
        label = item.get("label", "")

        if not isinstance(value, str) or not value:
            continue

        if label not in (
            "PERSON", "ADDRESS", "PHONE",
            "EMAIL", "DOB", "ID_NUMBER",
            "VEHICLE_NUMBER"
        ):
            continue

        start = 0
        while True:
            index = text.find(value, start)
            if index == -1:
                break

            findings.append({
                "text": value,
                "label": label,
                "start": index,
                "end": index + len(value)
            })
            start = index + len(value)

    return {
        "findings": findings,
        "risk_level": result.get("risk_level", "Unknown"),
        "risk_summary": result.get("risk_summary", ""),
        "recommendations": result.get("recommendations", [])
    }


def verify_redaction(redacted_text):
    client = get_client()

    prompt = f"""
Check whether this redacted text still contains personal information.
Find actual values such as:
- Personal names
- Residential or office addresses
- Phone numbers
- Email addresses
- Actual dates of birth
- Identification numbers

Do NOT flag generic labels or headings such as:
"Date of Birth", "Phone Number", "Address", "Email",
"Plaintiff", or "Defendant","VEHICLE_NUMBER".

Ignore redaction placeholders like [PERSON], [ADDRESS],
[PHONE], [EMAIL], [DOB], [ID_NUMBER].

Return only valid JSON:
{{
  "safe": true,
  "remaining_entities": [],
  "message": "Short verification result"
}}

TEXT:
{redacted_text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_completion_tokens=500,
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)
