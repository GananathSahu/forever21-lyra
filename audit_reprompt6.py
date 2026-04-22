"""
================================================================
  FOREVER 21 LYRA — REPROMPT_Session6.txt AUDIT
  Verifies reprompt file is accurate and complete
  Date: 22 April 2026
================================================================
"""

import sys
import subprocess

PASS = []
FAIL = []
WARN = []

def ok(msg): PASS.append(msg); print(f"  \u2705 {msg}")
def fail(msg): FAIL.append(msg); print(f"  \u274c FAIL: {msg}")
def warn(msg): WARN.append(msg); print(f"  \u26a0\ufe0f  WARN: {msg}")

print("=" * 60)
print("  FOREVER 21 LYRA \u2014 REPROMPT SESSION 6 AUDIT")
print("=" * 60)

# Load REPROMPT file
try:
    with open("REPROMPT_Session6.txt", encoding="utf-8") as f:
        rp = f.read()
    print(f"\n\u2705 REPROMPT_Session6.txt loaded ({len(rp.encode())} bytes, {len(rp.splitlines())} lines)")
except Exception as e:
    print(f"\u274c Cannot load REPROMPT_Session6.txt: {e}")
    sys.exit(1)

# Load app.py and system_prompt.txt for cross-checking
try:
    with open("app.py", encoding="utf-8") as f:
        app = f.read()
    with open("system_prompt.txt", encoding="utf-8") as f:
        sp = f.read()
except Exception as e:
    print(f"\u274c Cannot load app files: {e}")
    sys.exit(1)

# Get actual git HEAD
try:
    result = subprocess.run(["git", "log", "--oneline", "-1"],
                          capture_output=True, text=True)
    actual_head = result.stdout.strip().split()[0] if result.stdout else "unknown"
    print(f"\u2705 Git HEAD: {actual_head}")
except:
    actual_head = "unknown"
    warn("Could not get git HEAD")

print()

# SECTION 1: CRITICAL IDENTIFIERS
print("\u2500\u2500 SECTION 1: CRITICAL IDENTIFIERS \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
ok("App URL present") if "forever21-lyra.streamlit.app" in rp else fail("App URL missing")
ok("GitHub URL present") if "github.com/GananathSahu/forever21-lyra" in rp else fail("GitHub URL missing")
ok("Phone number present") if "98531 15511" in rp else fail("Phone number missing")
ok("Studio address present") if "Kalinga Vihar" in rp else fail("Studio address missing")
ok("Owner name present") if "Bini" in rp else fail("Owner name missing")

# SECTION 2: VERSION ACCURACY
print("\n\u2500\u2500 SECTION 2: VERSION ACCURACY \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")

# Check git HEAD accuracy
if actual_head in rp:
    ok(f"Git HEAD {actual_head} matches reprompt")
else:
    fail(f"Git HEAD {actual_head} NOT in reprompt — reprompt is outdated")

# Check app version
if "v10.6" in rp:
    ok("App version v10.6 present")
else:
    fail("App version v10.6 missing — reprompt outdated")

# Check system prompt version
if "v6.2" in rp or "6.2" in rp:
    ok("System prompt v6.2 referenced")
else:
    fail("System prompt v6.2 not referenced — reprompt outdated")

# Check audit count
if "72" in rp:
    ok("Audit count 72 present")
else:
    fail("Audit count 72 missing")

# Check audit script name
if "audit_session6" in rp:
    ok("audit_session6.py referenced")
else:
    fail("audit_session6.py not referenced")

# SECTION 3: SACRED SECTIONS DOCUMENTED
print("\n\u2500\u2500 SECTION 3: SACRED SECTIONS DOCUMENTED \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
ok("Golden Phrase documented") if "Every client at Forever 21 is unique" in rp else fail("Golden Phrase missing from reprompt")
ok("4-step lead capture documented") if "STEP 1" in rp and "STEP 2" in rp else fail("4-step flow missing")
ok("Sacred sections listed") if "NEVER touch" in rp or "NEVER TOUCH" in rp else fail("Sacred sections warning missing")
ok("LEAD CAPTURE FLOW sacred") if "LEAD CAPTURE FLOW" in rp else fail("LEAD CAPTURE FLOW not listed as sacred")
ok("TRILINGUAL MASTERY sacred") if "TRILINGUAL" in rp else fail("TRILINGUAL not listed as sacred")

# SECTION 4: LESSONS LEARNED DOCUMENTED
print("\n\u2500\u2500 SECTION 4: LESSONS LEARNED \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
ok("Never rewrite lesson") if "NEVER REWRITE" in rp or "Never rewrite" in rp else fail("Never rewrite lesson missing")
ok("Behavioural audit lesson") if "behaviour" in rp.lower() or "behavioral" in rp.lower() else fail("Behavioural audit lesson missing")
ok("Mobile test lesson") if "mobile" in rp.lower() else fail("Mobile test lesson missing")
ok("Patch verification lesson") if "patch" in rp.lower() else fail("Patch verification lesson missing")

# SECTION 5: SESSION START PROTOCOL
print("\n\u2500\u2500 SECTION 5: SESSION START PROTOCOL \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
ok("Audit command documented") if "audit_session6.py" in rp else fail("Audit command missing")
ok("Git log command documented") if "git log" in rp else fail("Git log command missing")
ok("Manual test documented") if "manually test" in rp.lower() or "manual test" in rp.lower() else fail("Manual test step missing")
ok("Recovery command documented") if "git checkout" in rp else fail("Recovery command missing")
ok("Directory path documented") if "Google Drive" in rp else fail("Directory path missing")

# SECTION 6: TECHNICAL ACCURACY
print("\n\u2500\u2500 SECTION 6: TECHNICAL ACCURACY \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
ok("Gemini engine documented") if "gemini" in rp.lower() else fail("Gemini engine missing")
ok("Google Sheets documented") if "Google Sheets" in rp else fail("Google Sheets missing")
ok("Streamlit documented") if "Streamlit" in rp else fail("Streamlit missing")
ok("IST timezone fix documented") if "IST" in rp else fail("IST timezone fix not documented")
ok("Secrets file warning") if "secrets" in rp.lower() else fail("Secrets file warning missing")

# SECTION 7: SESSION 6 AGENDA
print("\n\u2500\u2500 SECTION 7: SESSION 6 AGENDA \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
ok("Mobile UX in agenda") if "mobile" in rp.lower() else fail("Mobile UX missing from agenda")
ok("Gallery in agenda") if "Gallery" in rp else fail("Gallery missing from agenda")
ok("Timeout in agenda") if "timeout" in rp.lower() or "connection" in rp.lower() else fail("Timeout missing from agenda")

# RESULTS
total = len(PASS) + len(FAIL)
print("\n" + "=" * 60)
print(f"  TOTAL : {total}")
print(f"  \u2705 PASSED  : {len(PASS)}")
print(f"  \u274c FAILED  : {len(FAIL)}")
print(f"  \u26a0\ufe0f  WARNINGS: {len(WARN)}")
print("=" * 60)
if not FAIL:
    print("  \U0001f389 REPROMPT IS ACCURATE \u2014 SAFE TO USE")
else:
    print("  \U0001f6a8 REPROMPT NEEDS UPDATING \u2014 DO NOT USE AS-IS")
    for f in FAIL:
        print(f"     \u274c {f}")
if WARN:
    for w in WARN:
        print(f"     \u26a0\ufe0f  {w}")
print("=" * 60)
