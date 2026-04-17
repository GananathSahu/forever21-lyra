"""
================================================================
  FOREVER 21 LYRA — SESSION 6 AUDIT
  Comprehensive audit covering all sessions + lessons learned
  Date: 18 April 2026
  Expected: 75/75
================================================================
"""

import ast
import sys

PASS = []
FAIL = []
WARN = []

def ok(msg): PASS.append(msg); print(f"  \u2705 {msg}")
def fail(msg): FAIL.append(msg); print(f"  \u274c FAIL: {msg}")
def warn(msg): WARN.append(msg); print(f"  \u26a0\ufe0f  WARN: {msg}")

print("=" * 60)
print("  FOREVER 21 LYRA \u2014 SESSION 6 AUDIT (COMPREHENSIVE)")
print("=" * 60)

# Load files
try:
    with open("app.py", encoding="utf-8") as f:
        app = f.read()
        app_lines = app.splitlines()
    print(f"\n\u2705 app.py loaded ({len(app.encode())} bytes, {len(app_lines)} lines)")
except Exception as e:
    print(f"\u274c Cannot load app.py: {e}"); sys.exit(1)

try:
    with open("system_prompt.txt", encoding="utf-8") as f:
        sp = f.read()
        sp_lines = sp.splitlines()
    print(f"\u2705 system_prompt.txt loaded ({len(sp.encode())} bytes, {len(sp_lines)} lines)")
except Exception as e:
    print(f"\u274c Cannot load system_prompt.txt: {e}"); sys.exit(1)

# SECTION 1: PYTHON SYNTAX
print("\n\u2500\u2500 SECTION 1: PYTHON SYNTAX \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
try:
    ast.parse(app)
    ok("app.py syntax valid (AST parse)")
except SyntaxError as e:
    fail(f"app.py syntax valid \u2014 ERROR: {e}")

# SECTION 2: RICH FEATURES
print("\n\u2500\u2500 SECTION 2: RICH FEATURES (must be preserved) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
checks2 = [
    ("GALLERY_B64", "Gallery B64 images present"),
    ("GALLERY_ITEMS", "Gallery items defined"),
    ("wa.me/919853115511", "WhatsApp link present"),
    ("FESTIVAL_BANNER", "Festival banner present"),
    ("flashBanner", "Flashing banner animation"),
    ("admin_logged_in", "Admin dashboard present"),
    ("save_lead_to_sheet", "Google Sheets lead save"),
    ("f21_logo_new", "Logo loading present"),
    ("chip_question", "Quick chips present"),
    ("Special Discounts", "Discount info present"),
    ("instagram.com", "Social links present"),
    ("maps.app.goo.gl", "Maps link present"),
    ("gemini-2.5-flash", "Gemini 2.5 Flash engine"),
    ("gspread", "gspread import present"),
    ("st.columns", "Column layout present"),
]
for term, msg in checks2:
    ok(msg) if term in app else fail(msg)

# SECTION 3: SESSION 4 CHANGES
print("\n\u2500\u2500 SECTION 3: SESSION 4 CHANGES \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
checks3 = [
    ("def is_valid_indian_mobile", "Phone validation function exists"),
    ("is_valid_indian_mobile(lead_phone)", "Phone validation called before saving"),
    ("^[6-9]", "Phone regex pattern (6-9 digits)"),
    ("Always Young, Always Beautiful", "Tagline in nav area"),
    ("Dandruff Treatment", "Dandruff Treatment in services"),
    ("Eyelash Extension", "Eyelash Extension in services"),
    ("Mole Removal", "Mole Removal in services"),
    ("Earlobe Repair", "Earlobe Repair in services"),
    ("Eye & Lash", "Eye & Lash category"),
    ("Skin & Advanced", "Skin & Advanced category"),
    ("LEAD_CAPTURED", "LEAD_CAPTURED tag parsing"),
]
for term, msg in checks3:
    ok(msg) if term in app else fail(msg)

# SECTION 4: SESSION 5 APP CHANGES
print("\n\u2500\u2500 SECTION 4: SESSION 5 APP CHANGES \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
checks4_app = [
    ("nav_v2_done", "2-button nav (Chat + Gallery)"),
    ("nav_admin_bottom", "Admin button at bottom of left panel"),
    ("tagline_below_logo", "Tagline below logo"),
    ("patch_v91", "Expanded tagline styling in chat"),
    ("scroll-arrow", "Flashing arrow CSS present"),
    ("arrow_rerun", "Two-phase arrow rerun"),
    ("patch_layout2", "Header first, festival in right column"),
    ("patch_compact2", "Left panel compacted"),
    ("mobile_columns", "Mobile column order CSS"),
    ("disclaimer_conditional", "Disclaimer conditional on messages"),
]
for term, msg in checks4_app:
    ok(msg) if term in app else fail(msg)

# SECTION 5: SYSTEM PROMPT — VERSION AND STRUCTURE
print("\n\u2500\u2500 SECTION 5: SYSTEM PROMPT \u2014 VERSION & STRUCTURE \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
checks5_version = [
    ("System Prompt Version: 6.0", "System prompt version 6.0"),
    ("MUST ALWAYS be written in English", "English-only tagline rule"),
    ("NEVER translate the tagline", "Tagline never translated rule"),
    ("ODIA CONFIRMATION", "Odia confirmation rule"),
    ("NEVER quote any price", "No price rule"),
    ("maps.app.goo.gl/B7oszYnEmBxMxLVe8", "Maps link correct"),
    ("9 AM to 9 PM", "Working hours 9AM-9PM"),
    ('LEAD_CAPTURED:{"name"', "LEAD_CAPTURED format"),
    ("valid Indian mobile", "Phone validation in prompt"),
    ("Start with 6, 7, 8, or 9", "Starts with 6/7/8/9 rule"),
    ("off-topic", "Off-topic rule"),
    ("bridal", "Bridal flow"),
    ("10% discount", "Discounts in prompt"),
]
for term, msg in checks5_version:
    ok(msg) if term in sp else fail(msg)

# SECTION 6: SYSTEM PROMPT — SACRED SECTIONS (LESSONS LEARNED)
print("\n\u2500\u2500 SECTION 6: SACRED SECTIONS (NEVER BREAK) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
sacred_checks = [
    ("GOLDEN PHRASE", "Golden Phrase present in system prompt"),
    ("LEAD CAPTURE FLOW", "Lead capture flow section present"),
    ("Every client at Forever 21 is unique", "Golden phrase text correct"),
    ("May I have your name and phone number", "Name and phone ask present"),
    ("STEP 1 - WARM INTEREST", "Step 1 warm interest present"),
    ("STEP 2 - CONSULTATION PIVOT", "Step 2 consultation pivot present"),
    ("STEP 3 - ASK FOR NAME AND PHONE", "Step 3 ask for contact present"),
    ("STEP 4 - WARM CLOSE", "Step 4 warm close present"),
    ("proactive_lead_capture", "Proactive lead capture marker"),
    ("EVERY conversation", "Every conversation rule"),
]
for term, msg in sacred_checks:
    ok(msg) if term in sp else fail(msg)

# SECTION 7: SESSION 5 SYSTEM PROMPT ADDITIONS
print("\n\u2500\u2500 SECTION 7: SESSION 5 SYSTEM PROMPT ADDITIONS \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
checks7 = [
    ("audience_rule", "Audience rule marker"),
    ("primarily serves", "Ladies studio rule"),
    ("adult men", "Adult men clarification"),
    ("trusted friend", "Warm tone guidance"),
    ("Dandruff Treatment", "Dandruff Treatment in prompt"),
    ("Eyelash Extension", "Eyelash Extension in prompt"),
    ("Mole Removal", "Mole Removal in prompt"),
    ("Earlobe Repair", "Earlobe Repair in prompt"),
]
for term, msg in checks7:
    ok(msg) if term in sp else fail(msg)

# SECTION 8: FILE SIZE SANITY
print("\n\u2500\u2500 SECTION 8: FILE SIZE SANITY \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500")
app_size = len(app.encode())
sp_size = len(sp.encode())
ok("app.py is rich (>400KB with gallery)") if app_size > 400000 else fail("app.py too small \u2014 gallery may be missing")
ok("system_prompt.txt is substantial (>18KB)") if sp_size > 18000 else fail("system_prompt.txt too small \u2014 content may be missing")
ok("system_prompt.txt not bloated (<50KB)") if sp_size < 50000 else warn("system_prompt.txt very large \u2014 check for duplication")

# RESULTS
total = len(PASS) + len(FAIL)
print("\n" + "=" * 60)
print(f"  TOTAL : {total}")
print(f"  \u2705 PASSED  : {len(PASS)}")
print(f"  \u274c FAILED  : {len(FAIL)}")
print(f"  \u26a0\ufe0f  WARNINGS: {len(WARN)}")
print("=" * 60)
if not FAIL:
    print("  \U0001f389 ALL CRITICAL CHECKS PASSED \u2014 SAFE TO PROCEED")
else:
    print("  \U0001f6a8 FAILURES DETECTED \u2014 DO NOT DEPLOY")
    for f in FAIL:
        print(f"     \u274c {f}")
if WARN:
    for w in WARN:
        print(f"     \u26a0\ufe0f  {w}")
print("=" * 60)
