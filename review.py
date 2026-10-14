import json
import sys

import anthropic

client = anthropic.Anthropic()        # uses your ANTHROPIC_API_KEY
MODEL = "claude-sonnet-5-5"

spec = open("spec.md").read()
code = open("discount.py").read()
notes = open("writer_notes.md").read()
rules = open("CLAUDE.md").read()

# 1) SELF-REVIEW: the writer reviews its own code. It still sees its own reasoning.
self_review = client.messages.create(
    model=MODEL,
    max_tokens=600,
    messages=[
        {"role": "user", "content": "Write discount.py from this spec:\n" + spec},
        {"role": "assistant", "content": notes + "\n" + code},
        {"role": "user", "content": "Quickly review your code. Any problems?"},
    ],
)
print("=== SELF-REVIEW ===")
print(self_review.content[0].text)

# 2) INDEPENDENT REVIEW: a fresh call. Only the spec, the rules and the code. JSON out.
schema = {
    "type": "object",
    "properties": {
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "severity": {"type": "string", "enum": ["important", "nit"]},
                    "issue": {"type": "string"},
                },
                "required": ["severity", "issue"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["findings"],
    "additionalProperties": False,
}
review = client.messages.create(
    model=MODEL,
    max_tokens=1500,
    system="You are an independent code reviewer. You did not write this code.\n" + rules,
    messages=[{"role": "user", "content": "SPEC:\n" + spec + "\n\nCODE:\n" + code}],
    output_config={"format": {"type": "json_schema", "schema": schema}},
)
findings = json.loads(review.content[0].text)["findings"]

print("\n=== INDEPENDENT REVIEW ===")
for f in findings:
    print(f"[{f['severity']}] {f['issue']}")

# 3) GATE: fail (exit code 1) if there is any important finding
important = [f for f in findings if f["severity"] == "important"]
print("\nRESULT:", "BLOCK the merge" if important else "OK to merge")
sys.exit(1 if important else 0)
