"""
================================================================
  FOREVER 21 LYRA — REPROMPT_Session7.txt AUDIT
  Verifies Session 7 reprompt is accurate and complete
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
print("  FOREVER 21 LYRA \u2014 REPROMPT SESSION 7 AUDIT")
print("=" * 60)

# Load REPROMPT file
try:
    with open("REPROMPT_Session7.txt", encoding="utf-8") as f:
        rp = f.read()
    print(f"\n\u2705 REPROMPT_Session7.txt loaded ({len(rp.encode())} bytes, {len(rp.splitlines())} lines)")
except Exception as e:
    print(f"\u274c Cannot load REPROMPT_Session7.txt: {e}")
    sys.exit(1)

# Load app.py and system_prompt.txt
try:
    with open("app.py", encoding="utf-8") as f:
        app = f.read()
    with open("system_prompt.txt", encoding="utf-8") as f:
        sp = f.read()
except Exception as e:
    print(f"\u274c Cannot load app files: {e}")
    sys.exit(1)

print()

# SECTION 1: CRITICAL IDENTIFIERS
print("\u2500\u2500 SECTION 1: CRITICAL IDENTIFIERS \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
ok("App URL present") if "forever21-lyra.streamlit.app" in rp else fail("App URL missing")
ok("GitHub URL present") if "github.com/GananathSahu/forever21-lyra" in rp else fail("GitHub URL missing")
ok("Phone number present") if "98531 15511" in rp else fail("Phone number missing")
ok("Studio address present") if "Kalinga Vihar" in rp else fail("Studio address missing")
ok("Owner name present") if "Bini" in rp else fail("Owner name missing")
ok("Session 7 identified") if "Session 7" in rp else fail("Session 7 not identified")

# SECTION 2: VERSION AND AUDIT INFO
print("\n\u2500\u2500 SECTION 2: VERSION AND AUDIT INFO \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
ok("App version referenced") if "v10." in rp else fail("App version missing")
ok("System prompt v6.2 referenced") if "v6.2" in rp else fail("System prompt version missing")
ok("audit_session6.py referenced") if "audit_session6.py" in rp else fail("audit_session6.py missing")
ok("audit_reprompt6.py referenced") if "audit_reprompt6.py" in rp else fail("audit_reprompt6.py missing")
ok("72 checks referenced") if "72" in rp else fail("72 checks not referenced")
ok("32 checks referenced") if "32" in rp else fail("32 checks not referenced")
ok("Recovery command present") if "git checkout" in rp else fail("Recovery command missing")

# SECTION 3: SESSION START PROTOCOL
print("\n\u2500\u2500 SECTION 3: SESSION START PROTOCOL \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
ok("Audit command documented") if "audit_session6.py" in rp else fail("Audit command missing")
ok("Reprompt audit command documented") if "audit_reprompt6.py" in rp else fail("Reprompt audit command missing")
ok("Git log command documented") if "git log" in rp else fail("Git log command missing")
ok("Manual test step documented") if "manually test" in rp.lower() or "Manually test" in rp else fail("Manual test missing")
ok("Directory path documented") if "Google Drive" in rp else fail("Directory path missing")

# SECTION 4: SACRED SECTIONS
print("\n\u2500\u2500 SECTION 4: SACRED SECTIONS \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
ok("Golden Phrase documented") if "Every client at Forever 21 is unique" in rp else fail("Golden Phrase missing")
ok("4-step flow documented") if "STEP 1" in rp and "STEP 4" in rp else fail("4-step flow missing")
ok("Sacred sections warning") if "NEVER touch" in rp or "NEVER TOUCH" in rp else fail("Sacred sections warning missing")
ok("LEAD CAPTURE FLOW sacred") if "LEAD CAPTURE FLOW" in rp else fail("LEAD CAPTURE FLOW not sacred")
ok("TRILINGUAL MASTERY sacred") if "TRILINGUAL" in rp else fail("TRILINGUAL not sacred")

# SECTION 5: LESSONS LEARNED
print("\n\u2500\u2500 SECTION 5: LESSONS LEARNED \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
ok("Never rewrite lesson") if "NEVER REWRITE" in rp or "Never rewrite" in rp else fail("Never rewrite lesson missing")
ok("Behavioural audit lesson") if "AUDIT BEHAVIOUR" in rp or "behaviour" in rp.lower() else fail("Behavioural audit lesson missing")
ok("Mobile test lesson") if "mobile" in rp.lower() else fail("Mobile test lesson missing")
ok("One recommendation lesson") if "ONE RECOMMENDATION" in rp or "one recommendation" in rp.lower() else fail("One recommendation lesson missing")
ok("Reprompt commit rule") if "meaningful content" in rp else fail("Reprompt commit rule missing")

# SECTION 6: CAMPAIGNPLUS DETAILS
print("\n\u2500\u2500 SECTION 6: CAMPAIGNPLUS DETAILS \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
ok("CampaignPlus login URL") if "crm.campaignplus.in" in rp else fail("CampaignPlus login URL missing")
ok("Business email documented") if "Mailtobinodini" in rp else fail("Business email missing")
ok("Plan details documented") if "API Quarterly" in rp else fail("Plan details missing")
ok("WhatsApp number documented") if "98531 15511" in rp else fail("WhatsApp number missing")
ok("API endpoint documented") if "campaignplus.in/api" in rp else fail("API endpoint missing")
ok("API key security warning") if "secrets.toml" in rp else fail("API key security warning missing")
ok("API key NOT in reprompt") if "TWFpbHRvYmlub2RpbmlAZ21haWwuY29t" not in rp else fail("API key exposed in reprompt — SECURITY RISK")
ok("Message templates documented") if "Namaskar! Thank you" in rp else fail("Message templates missing")
ok("Bini notification template") if "New Lead!" in rp else fail("Bini notification template missing")
ok("Blue tick status documented") if "Blue Tick" in rp else fail("Blue tick status missing")

# SECTION 7: SESSION 7 PLAN
print("\n\u2500\u2500 SECTION 7: SESSION 7 PLAN \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
ok("Test phase documented") if "test_campaignplus.py" in rp else fail("Test script missing")
ok("Webhook phase documented") if "whatsapp_webhook.py" in rp else fail("Webhook file missing")
ok("Deploy phase documented") if "render.com" in rp or "railway.app" in rp else fail("Deploy platform missing")
ok("Zero risk statement") if "zero risk" in rp.lower() or "Zero risk" in rp else fail("Zero risk statement missing")
ok("Separate from app.py") if "separate from app.py" in rp.lower() or "SEPARATE from app.py" in rp else fail("Separation statement missing")
ok("Trilingual test planned") if "Hindi, Odia" in rp or "Odia, Hindi" in rp else fail("Trilingual test missing")

# SECTION 8: BEHAVIOURAL BENCHMARKS
print("\n\u2500\u2500 SECTION 8: BEHAVIOURAL BENCHMARKS \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
ok("Greeting test documented") if 'Input: "Hi"' in rp else fail("Greeting test missing")
ok("Lead capture test documented") if "glow facial" in rp else fail("Lead capture test missing")
ok("No price test documented") if "How much does" in rp else fail("No price test missing")
ok("Tagline test documented") if "Tagline in English always" in rp else fail("Tagline test missing")
ok("Google Sheet test documented") if "IST timestamp" in rp else fail("Google Sheet test missing")

# SECTION 9: FILE SIZE SANITY
print("\n\u2500\u2500 SECTION 9: FILE SIZE SANITY \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
rp_size = len(rp.encode())
ok("Reprompt substantial (>3KB)") if rp_size > 3000 else fail("Reprompt too small")
ok("Reprompt not bloated (<30KB)") if rp_size < 30000 else warn("Reprompt very large")
ok("app.py size referenced") if "507" in rp else fail("app.py size not referenced")

# RESULTS
total = len(PASS) + len(FAIL)
print("\n" + "=" * 60)
print(f"  TOTAL : {total}")
print(f"  \u2705 PASSED  : {len(PASS)}")
print(f"  \u274c FAILED  : {len(FAIL)}")
print(f"  \u26a0\ufe0f  WARNINGS: {len(WARN)}")
print("=" * 60)
if not FAIL:
    print("  \U0001f389 REPROMPT SESSION 7 IS ACCURATE \u2014 SAFE TO USE")
else:
    print("  \U0001f6a8 REPROMPT NEEDS UPDATING \u2014 DO NOT USE AS-IS")
    for f in FAIL:
        print(f"     \u274c {f}")
if WARN:
    for w in WARN:
        print(f"     \u26a0\ufe0f  {w}")
print("=" * 60)
