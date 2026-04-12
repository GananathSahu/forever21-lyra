"""
Forever 21 Beauty Studio — Lyra Full Diagnostic Audit
Run this BEFORE any changes to app.py
Usage: python audit.py
"""

import sys
import os
import json

ROOT = os.path.dirname(os.path.abspath(__file__))
SECRETS_PATH = os.path.join(ROOT, ".streamlit", "secrets.toml")
CONFIG_PATH  = os.path.join(ROOT, ".streamlit", "config.toml")
APP_PATH     = os.path.join(ROOT, "app.py")
PROMPT_PATH  = os.path.join(ROOT, "..", "02_system_prompt", "system_prompt.txt")

PASS = "  [PASS]"
FAIL = "  [FAIL]"
INFO = "  [INFO]"

results = []

def check(label, passed, detail=""):
    status = PASS if passed else FAIL
    line = f"{status} {label}"
    if detail:
        line += f"\n         {detail}"
    results.append((passed, line))
    print(line)

print()
print("=" * 60)
print("  FOREVER 21 LYRA — FULL DIAGNOSTIC AUDIT")
print("=" * 60)

# ── 1. FILE EXISTS CHECKS ─────────────────────────────────────
print("\n[1] FILE STRUCTURE")

check("app.py exists",            os.path.exists(APP_PATH))
check("secrets.toml exists",      os.path.exists(SECRETS_PATH))
check("config.toml exists",       os.path.exists(CONFIG_PATH))
check("system_prompt.txt exists", os.path.exists(PROMPT_PATH),
      f"Looking at: {PROMPT_PATH}")

# ── 2. SECRETS.TOML CONTENT ───────────────────────────────────
print("\n[2] SECRETS.TOML")

try:
    import toml
    secrets = toml.load(SECRETS_PATH)

    api_key = secrets.get("GOOGLE_API_KEY", "")
    check("GOOGLE_API_KEY present",       bool(api_key))
    check("GOOGLE_API_KEY not placeholder",
          api_key not in ("", "AIza-REPLACE_ME", "YOUR_NEW_KEY_HERE"),
          f"Key starts with: {api_key[:12]}..." if api_key else "MISSING")

    sheet_id = secrets.get("GOOGLE_SHEET_ID", "")
    check("GOOGLE_SHEET_ID present",       bool(sheet_id))
    check("GOOGLE_SHEET_ID not placeholder",
          sheet_id not in ("", "REPLACE_ME"),
          f"Sheet ID: {sheet_id[:10]}..." if sheet_id else "MISSING")

    gcp = secrets.get("gcp_service_account", {})
    check("gcp_service_account present",   bool(gcp))
    check("gcp client_email present",
          bool(gcp.get("client_email", "")),
          gcp.get("client_email", "MISSING"))
    check("gcp private_key present",
          "REPLACE_ME" not in gcp.get("private_key", "REPLACE_ME"),
          "Key length: " + str(len(gcp.get("private_key", ""))) + " chars")

except Exception as e:
    check("secrets.toml readable", False, str(e))

# ── 3. CONFIG.TOML SYNTAX ─────────────────────────────────────
print("\n[3] CONFIG.TOML")

try:
    import toml
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        raw = f.read()
    toml.loads(raw)
    check("config.toml syntax valid", True)
    check("config.toml has [theme]",  "[theme]" in raw)
    check("config.toml has [server]", "[server]" in raw)
except Exception as e:
    check("config.toml syntax valid", False, str(e))

# ── 4. PYTHON PACKAGES ────────────────────────────────────────
print("\n[4] PYTHON PACKAGES")

packages = {
    "streamlit":      "streamlit",
    "google.genai":   "google.genai",
    "gspread":        "gspread",
    "google.oauth2":  "google.oauth2.service_account",
    "toml":           "toml",
}

for name, module in packages.items():
    try:
        __import__(module)
        import importlib.metadata
        try:
            ver = importlib.metadata.version(name.split(".")[0])
        except Exception:
            ver = "unknown version"
        check(f"{name} installed", True, ver)
    except ImportError as e:
        check(f"{name} installed", False, str(e))

# ── 5. GEMINI API LIVE TEST ───────────────────────────────────
print("\n[5] GEMINI API LIVE TEST")

try:
    import toml
    from google import genai
    from google.genai import types

    secrets = toml.load(SECRETS_PATH)
    api_key = secrets.get("GOOGLE_API_KEY", "")

    if not api_key or api_key in ("AIza-REPLACE_ME", "YOUR_NEW_KEY_HERE"):
        check("Gemini API key usable", False, "Key is placeholder — update secrets.toml")
    else:
        client = genai.Client(api_key=api_key)

        # List available models
        models = [m.name for m in client.models.list()]
        gemini_models = [m for m in models if "gemini" in m.lower()]
        check("Models listed successfully", True,
              f"{len(gemini_models)} Gemini models available")

        # Find best model to use
        preferred = [
            "models/gemini-2.0-flash-001",
            "models/gemini-2.0-flash",
            "models/gemini-2.5-flash",
            "models/gemini-2.0-flash-001",
            "models/gemini-2.5-pro",
        ]
        chosen = next((m for m in preferred if m in models), None)
        if not chosen and gemini_models:
            chosen = gemini_models[0]

        check("Suitable model found", bool(chosen), chosen or "None found")

        if chosen:
            # Live call test
            try:
                response = client.models.generate_content(
                    model=chosen,
                    contents="Reply with exactly: AUDIT_OK",
                    config=types.GenerateContentConfig(
                        temperature=0.1,
                        max_output_tokens=20,
                    ),
                )
                reply = response.text.strip() if response.text else ""
                check("Live API call succeeded", bool(reply), f"Response: '{reply}'")
                print(f"\n  {INFO} Best model to use in app.py: {chosen}")
            except Exception as e:
                check("Live API call succeeded", False, str(e))

except Exception as e:
    check("Gemini API test", False, str(e))

# ── 6. GOOGLE SHEETS TEST ────────────────────────────────────
print("\n[6] GOOGLE SHEETS CONNECTION")

try:
    import toml
    import gspread
    from google.oauth2.service_account import Credentials

    secrets = toml.load(SECRETS_PATH)
    gcp     = secrets.get("gcp_service_account", {})
    sheet_id = secrets.get("GOOGLE_SHEET_ID", "")

    if not gcp or "REPLACE_ME" in gcp.get("private_key", "REPLACE_ME"):
        check("Sheets credentials usable", False, "GCP credentials are placeholders")
    elif not sheet_id or sheet_id == "REPLACE_ME":
        check("Sheet ID usable", False, "GOOGLE_SHEET_ID is placeholder")
    else:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds  = Credentials.from_service_account_info(gcp, scopes=scopes)
        gc     = gspread.authorize(creds)
        sheet  = gc.open_by_key(sheet_id)
        ws     = sheet.worksheet("Leads")
        rows   = len(ws.get_all_values())
        check("Google Sheets connected", True,
              f"Sheet: '{sheet.title}' | Leads tab rows: {rows}")

except Exception as e:
    check("Google Sheets connected", False, str(e))

# ── 7. APP.PY MODEL NAME CHECK ───────────────────────────────
print("\n[7] APP.PY CONTENT CHECK")

try:
    with open(APP_PATH, "r", encoding="utf-8") as f:
        app_code = f.read()

    check("Uses google.genai (new SDK)",
          "from google import genai" in app_code)
    check("No deprecated google.generativeai",
          "google.generativeai" not in app_code)
    check("GOOGLE_API_KEY in st.secrets",
          'st.secrets["GOOGLE_API_KEY"]' in app_code)
    check("system_instruction used",
          "system_instruction" in app_code)

    import re
    model_matches = re.findall(r'model=["\']([^"\']+)["\']', app_code)
    for m in model_matches:
        if "gemini" in m:
            check(f"Model in app.py: {m}", True)

except Exception as e:
    check("app.py readable", False, str(e))

# ── SUMMARY ──────────────────────────────────────────────────
print()
print("=" * 60)
total  = len(results)
passed = sum(1 for ok, _ in results if ok)
failed = total - passed

print(f"  RESULT: {passed}/{total} checks passed")
if failed == 0:
    print("  STATUS: ALL GOOD — safe to run app.py")
else:
    print(f"  STATUS: {failed} issue(s) need fixing before running app")
print("=" * 60)
print()
