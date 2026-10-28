#!/usr/bin/env python3
"""Validation tests for the Freebies directory.

Run:  python3 tests/validate.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILURES = []


def check(condition, message):
    if condition:
        print(f"PASS: {message}")
    else:
        print(f"FAIL: {message}")
        FAILURES.append(message)


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main():
    tools_path = ROOT / "tools.json"
    index_path = ROOT / "index.html"
    readme_path = ROOT / "README.md"
    license_path = ROOT / "LICENSE"

    check(tools_path.exists(), "tools.json exists")
    check(index_path.exists(), "index.html exists")
    check(readme_path.exists(), "README.md exists")
    check(license_path.exists(), "LICENSE exists")

    data = load_json(tools_path)

    check(isinstance(data.get("tools"), list), "tools is a list")
    check(len(data["tools"]) > 0, "tools list is not empty")

    categories = {c["key"] for c in data.get("categories", [])}
    check(len(categories) == 4, f"exactly 4 categories ({sorted(categories)})")

    required = ("name", "category", "cost", "platform", "steps", "officialLink")
    from collections import Counter
    cat_counts = Counter()

    for tool in data["tools"]:
        tid = tool.get("id", "<missing id>")
        for field in required:
            check(field in tool and str(tool[field]).strip(), f"{tid}: has {field}")
        check(tool.get("category") in categories, f"{tid}: category is valid")
        check(tool.get("officialLink", "").startswith("https://"), f"{tid}: link is https")
        check(not re.search(r"(ref=|affiliate|utm_|partner=|tracking=)", tool.get("officialLink", ""), re.I),
              f"{tid}: no affiliate/referral params")
        cat_counts[tool["category"]] += 1

    check(len(cat_counts) == 4, "all four categories have at least one tool")

    # Embedded JSON in index.html matches tools.json
    page = index_path.read_text(encoding="utf-8")
    m = re.search(r'<script id="freebies-data" type="application/json">\n(.*?)\n</script>', page, re.S)
    check(bool(m), "index.html embeds freebies-data JSON")
    if m:
        embedded = json.loads(m.group(1))
        check(embedded == data, "embedded data equals tools.json")

    # Client-side search logic sanity check
    def matches(tool, term, cat_key):
        if cat_key and tool["category"] != cat_key:
            return False
        if not term:
            return True
        haystack = " ".join([
            tool["name"], tool["description"], tool["cost"],
            tool["platform"], tool["officialLink"], " ".join(tool["steps"]),
        ])
        return term.lower() in haystack.lower()

    term_matches = [t for t in data["tools"] if matches(t, "invoice", "")]
    check(len(term_matches) == 5, f"keyword search 'invoice' returns 5 (got {len(term_matches)})")
    cat_matches = [t for t in data["tools"] if matches(t, "", "contracts")]
    check(len(cat_matches) == 5, f"category 'contracts' returns 5 (got {len(cat_matches)})")
    empty = [t for t in data["tools"] if matches(t, "zzznomatch", "")]
    check(len(empty) == 0, "non-matching search returns zero")

    # LICENSE exact copyright line
    license_text = license_path.read_text(encoding="utf-8")
    copyright_lines = [line for line in license_text.splitlines() if line.startswith("Copyright")]
    check(copyright_lines == ["Copyright (c) 2026 Asdale Dynamics, LLC"],
          f"LICENSE copyright line exact: {copyright_lines}")

    # README credits Asdale Dynamics, LLC
    readme_text = readme_path.read_text(encoding="utf-8")
    check("Asdale Dynamics, LLC" in readme_text, "README credits Asdale Dynamics, LLC")
    check("MIT License" in readme_text or "license" in readme_text.lower(), "README mentions license")

    # No secrets/personal data patterns anywhere in tracked text files
    secret_patterns = [r"sk-[A-Za-z0-9]{20,}", r"AKIA[0-9A-Z]{16}", r"password\s*=\s*\S+", r"api.?key\s*=\s*\S+"]
    for path in [tools_path, index_path, readme_path, license_path, ROOT / "css" / "style.css", ROOT / "js" / "app.js"]:
        text = path.read_text(encoding="utf-8")
        for pat in secret_patterns:
            check(not re.search(pat, text, re.I), f"{path.name}: no secret pattern {pat}")

    print()
    if FAILURES:
        print(f"{len(FAILURES)} test(s) FAILED")
        sys.exit(1)
    print("All tests passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
