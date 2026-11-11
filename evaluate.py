import json
import pandas as pd
from detector import detect_pii, merge_findings
from ai_engine import run_privacy_agent

df = pd.read_csv("data/privacylens_pii_dataset.csv")

tp = fp = fn = 0
successful = 0
failed = 0

for _, row in df.iterrows():
    text = row["text"]
    expected = json.loads(row["entities_json"])

    local = detect_pii(text)

    try:
        report = run_privacy_agent(text, local)
        ai = report.get("findings", [])
        successful += 1
    except Exception as e:
        print(f"AI failed on sample {row['sample_id']}: {e}")
        ai = []
        failed += 1

    predicted = merge_findings(text, local, ai)

    expected_set = {
        (x["start"], x["end"], x["label"])
        for x in expected
    }

    predicted_set = {
        (x["start"], x["end"], x["label"])
        for x in predicted
    }

    tp += len(expected_set & predicted_set)
    fp += len(predicted_set - expected_set)
    fn += len(expected_set - predicted_set)

precision = tp / (tp + fp) if tp + fp else 0
recall = tp / (tp + fn) if tp + fn else 0
f1 = (
    2 * precision * recall / (precision + recall)
    if precision + recall else 0
)

print("\nPrivacyLens AI Evaluation")
print("-------------------------")
print("Total samples:", len(df))
print("AI successful:", successful)
print("AI failed:", failed)
print("True Positives:", tp)
print("False Positives:", fp)
print("False Negatives:", fn)
print(f"Precision: {precision:.2%}")
print(f"Recall:    {recall:.2%}")
print(f"F1 Score:  {f1:.2%}")
