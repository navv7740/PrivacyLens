import re

PATTERNS = {
    "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "PHONE": r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)",
    "DOB": r"(?i)\b(?:DOB|date of birth|born on|birthday)(?:\s+is)?\s*[:\-]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{4}-\d{2}-\d{2})",
    "ID_NUMBER": r"\b(?:EMP[- ]?\d{4}[- ]?\d{3}|\d{4}[- ]\d{4}[- ]\d{4})\b",
    "ADDRESS": r"(?is)(?:delivery address|pickup address|residing at|office at|correspondence address is)\s*:?\s*(.+?\b\d{6}\b)",
    "TOLL_FREE": r"\b1800[\s-]?\d{3}[\s-]?\d{4}\b",
    "VEHICLE_NUMBER": r"\b[A-Z]{2}[- ]?\d{1,2}[- ]?[A-Z]{1,3}[- ]?\d{1,4}\b",}

def detect_pii(text):
    findings = []

    for label, pattern in PATTERNS.items():
        for match in re.finditer(pattern, text):
            start, end = match.span(1) if label in ("DOB",
             "ADDRESS") else match.span()
            if label == "ADDRESS":
                while end > start and text[end - 1] in " ,.;":
                    end -= 1    


            findings.append({
                "text": text[start:end],
                "label": label,
                "start": start,
                "end": end
            })

    return sorted(findings, key=lambda x: x["start"])


def merge_findings(text, *groups):
    candidates = []

    for group in groups:
        for item in group:
            start = item.get("start")
            end = item.get("end")

            if (
                isinstance(start, int)
                and isinstance(end, int)
                and 0 <= start < end <= len(text)
            ):
                candidates.append(item)

    candidates.sort(
        key=lambda x: (x["start"], -(x["end"] - x["start"]))
    )

    result = []

    for item in candidates:
        if all(
            item["end"] <= old["start"]
            or item["start"] >= old["end"]
            for old in result
        ):
            result.append(item)

    return sorted(result, key=lambda x: x["start"])


def redact_text(text, findings):
    output = text

    for item in sorted(findings, key=lambda x: x["start"], reverse=True):
        output = (
            output[:item["start"]]
            + f'[{item["label"]}]'
            + output[item["end"]:]
        )

    return output
