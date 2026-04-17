"""
================================================================
  FOREVER 21 LYRA — SESSION 5 AUDIT
  Supersedes audit_session4.py
  Checks all Session 4 + Session 5 changes
  Date: 18 April 2026
================================================================
"""

import ast
import sys

PASS = []
FAIL = []

def ok(msg): PASS.append(msg); print(f"  ✅ {msg}")
def fail(msg): FAIL.append(msg); print(f"  ❌ FAIL: {msg}")

print("=" * 60)
print("  FOREVER 21 LYRA — SESSION 5 AUDIT")
print("=" * 60)

# ── Load files ────────────────────────────────────────────────
try:
    with open("app.py", encoding="utf-8") as f:
        app = f.read()
        app_lines = app.splitlines()
    print(f"\n✅ app.py loaded ({len(app.encode())} bytes, {len(app_lines)} lines)")
except Exception as e:
    print(f"❌ Cannot load app.py: {e}"); sys.exit(1)

try:
    with open("system_prompt.txt", encoding="utf-8") as f:
        sp = f.read()
        sp_lines = sp.splitlines()
    print(f"✅ system_prompt.txt loaded ({len(sp.encode())} bytes, {len(sp_lines)} lines)")
except Exception as e:
    print(f"❌ Cannot load system_prompt.txt: {e}"); sys.exit(1)

# ── SECTION 1: PYTHON SYNTAX ──────────────────────────────────
print("\n── SECTION 1: PYTHON SYNTAX ──────────────────────────────")
try:
    ast.parse(app)
    ok("app.py syntax valid (AST parse)")
except SyntaxError as e:
    fail(f"app.py syntax valid — ERROR: {e}")

# ── SECTION 2: RICH FEATURES ──────────────────────────────────
print("\n── SECTION 2: RICH FEATURES (must be preserved) ─────────")
checks2 = [
    ("GALLERY_B64", "Gallery B64 images present (GALLERY_B64)"),
    ("GALLERY_ITEMS", "Gallery items defined (GALLERY_ITEMS)"),
    ("wa.me/919853115511", "WhatsApp link present"),
    ("FESTIVAL_BANNER", "Festival banner present"),
    ("flashBanner", "Flashing banner animation"),
    ("admin_logged_in", "Admin dashboard present"),
    ("save_lead_to_sheet", "Google Sheets lead save"),
    ("f21_logo_new", "Logo loading (f21_logo_new)"),
    ("chip_question", "Quick chips present"),
    ("Special Discounts", "Discount info present"),
    ("instagram.com", "Social links present"),
    ("maps.app.goo.gl", "Maps link present"),
    ("gemini-2.5-flash", "Gemini 2.5 Flash engine"),
    ("gspread", "gspread / Google Sheets import"),
    ("st.columns", "Two column layout"),
]
for term, msg in checks2:
    ok(msg) if term in app else fail(msg)

# ── SECTION 3: SESSION 4 CHANGES ─────────────────────────────
print("\n── SECTION 3: SESSION 4 CHANGES ─────────────────────────")
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

# ── SECTION 4: SYSTEM PROMPT ──────────────────────────────────
print("\n── SECTION 4: SYSTEM PROMPT ──────────────────────────────")
checks4 = [
    ("System Prompt Version: 6.0", "Version 5.9"),
    ("MUST ALWAYS be written in English", "English-only tagline rule"),
    ("NEVER translate the tagline", "Tagline never translated rule"),
    ("Always Young, Always Beautiful.**", "Hindi greeting uses English tagline"),
    ("Always Young, Always Beautiful.**", "Odia greeting uses English tagline"),
    ("ODIA CONFIRMATION", "Odia confirmation rule section"),
    ("ଆପଣଙ୍କ ନମ୍ବର", "Odia script confirmation example"),
    ("valid Indian mobile", "Phone validation in prompt"),
    ("Start with 6, 7, 8, or 9", "Starts with 6/7/8/9 rule"),
    ("Dandruff Treatment", "Dandruff Treatment in prompt"),
    ("Eyelash Extension", "Eyelash Extension in prompt"),
    ("Mole Removal", "Mole Removal in prompt"),
    ("Earlobe Repair", "Earlobe Repair in prompt"),
    ("NEVER quote any price", "No price rule"),
    ("maps.app.goo.gl/B7oszYnEmBxMxLVe8", "Maps link correct"),
    ("9 AM to 9 PM", "Working hours 9AM-9PM"),
    ('LEAD_CAPTURED:{"name"', "LEAD_CAPTURED format in prompt"),
    ("bridal", "Bridal flow in prompt"),
    ("10% discount", "Discounts in prompt"),
    ("off-topic", "Off-topic rule in prompt"),
]
for term, msg in checks4:
    ok(msg) if term in sp else fail(msg)

# ── SECTION 5: SESSION 5 CHANGES ─────────────────────────────
print("\n── SECTION 5: SESSION 5 CHANGES ─────────────────────────")

# App changes
checks5_app = [
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
for term, msg in checks5_app:
    ok(msg) if term in app else fail(msg)

# System prompt Session 5 changes
checks5_sp = [
    ("audience_rule", "Audience rule in system prompt"),
    ("primarily serves", "Ladies studio rule"),
    ("proactive_lead_capture", "Proactive lead capture rule"),
    ("EVERY conversation", "Every conversation lead capture"),
    ("trusted friend", "Warm tone guidance"),
    ("adult men", "Adult men clarification rule"),
]
for term, msg in checks5_sp:
    ok(msg) if term in sp else fail(msg)

# ── SECTION 6: FILE SIZE SANITY ───────────────────────────────
print("\n── SECTION 6: FILE SIZE SANITY ───────────────────────────")
app_size = len(app.encode())
sp_size = len(sp.encode())
ok("app.py is rich (>400KB with gallery)") if app_size > 400000 else fail("app.py too small — gallery may be missing")
ok("system_prompt.txt is complete (>15KB)") if sp_size > 15000 else fail("system_prompt.txt too small")

# ── RESULTS ───────────────────────────────────────────────────
total = len(PASS) + len(FAIL)
print("\n" + "=" * 60)
print(f"  TOTAL : {total}")
print(f"  ✅ PASSED  : {len(PASS)}")
print(f"  ❌ FAILED  : {len(FAIL)}")
print("=" * 60)
if not FAIL:
    print("  🎉 ALL CRITICAL CHECKS PASSED — SAFE TO PROCEED")
else:
    print("  🚨 FAILURES DETECTED — DO NOT DEPLOY")
    for f in FAIL:
        print(f"     ❌ {f}")
print("=" * 60)
