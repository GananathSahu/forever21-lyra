"""
Forever 21 Beauty Studio — Lyra AI Consultant
Streamlit App | Engine: Google Gemini 2.5 Flash
Trilingual: English / Hindi / Odia
Lead Capture: Google Sheets
"""

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from google import genai
from google.genai import types
from datetime import datetime
import re
import json
import os

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Forever 21 Beauty Studio",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─── LOAD SYSTEM PROMPT ──────────────────────────────────────────────────────

def load_system_prompt() -> str:
    candidates = [
        os.path.join(os.path.dirname(__file__), "..", "02_system_prompt", "system_prompt.txt"),
        os.path.join(os.path.dirname(__file__), "system_prompt.txt"),
    ]
    for path in candidates:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    return """
You are Lyra, warm beauty consultant for Forever 21 Beauty Studio, Bhubaneswar.
Owner: Bini. Tagline: "Always Young, Always Beautiful."
NEVER quote prices. Ask for name + phone so Bini can call personally.
Respond in the customer's language: Odia / Hindi / English.
When you have name AND phone, append on its own line:
LEAD_CAPTURED:{"name":"<n>","phone":"<p>"}
"""

SYSTEM_PROMPT = load_system_prompt()

# ─── GEMINI CLIENT ───────────────────────────────────────────────────────────

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

# ─── GOOGLE SHEETS ───────────────────────────────────────────────────────────

def get_leads_worksheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes,
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(st.secrets["GOOGLE_SHEET_ID"])
    return sheet.worksheet("Leads")


def save_lead(name: str, phone: str) -> bool:
    try:
        ws = get_leads_worksheet()
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
        ws.append_row([timestamp, name.strip(), phone.strip(), "New Lead"])
        return True
    except Exception as e:
        st.error(f"Google Sheets error: {e}")
        return False

# ─── RESPONSE UTILITIES ──────────────────────────────────────────────────────

def extract_lead(text: str):
    match = re.search(r"LEAD_CAPTURED:\{[^}]+\}", text)
    if match:
        try:
            payload = match.group().replace("LEAD_CAPTURED:", "")
            data = json.loads(payload)
            name = data.get("name", "").strip()
            phone = data.get("phone", "").strip()
            if name and phone:
                return name, phone
        except (json.JSONDecodeError, AttributeError):
            pass
    return None, None


def clean_response(text: str) -> str:
    return re.sub(r"\n?LEAD_CAPTURED:\{[^}]+\}", "", text).strip()


def build_history(messages: list) -> list:
    history = []
    for msg in messages:
        role = "model" if msg["role"] == "assistant" else "user"
        content = clean_response(msg["content"]) if role == "model" else msg["content"]
        history.append(types.Content(role=role, parts=[types.Part(text=content)]))
    return history

# ─── CUSTOM CSS ──────────────────────────────────────────────────────────────

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=DM+Sans:wght@300;400;500&display=swap');
  :root {
    --rose:    #8B3A62;
    --blush:   #F4C0D1;
    --muted:   #b06090;
    --dark:    #2C2C2A;
    --light-bg:#fff0f6;
  }
  .brand-header { text-align:center; padding:1.8rem 0 1rem; font-family:'Cormorant Garamond',serif; }
  .brand-name { font-size:1.9rem; font-weight:600; color:var(--rose); letter-spacing:0.04em; }
  .brand-tagline { font-size:0.88rem; color:var(--muted); font-style:italic; margin-top:4px;
                   font-family:'DM Sans',sans-serif; font-weight:300; letter-spacing:0.06em; }
  .lead-banner { background:var(--light-bg); border:1px solid var(--blush); border-radius:10px;
                 padding:12px 16px; margin:6px 0; font-size:0.86rem; color:#72243E;
                 font-family:'DM Sans',sans-serif; }
  .lead-banner strong { color:#4B1528; }
  .chat-user { background:#F0EAF8; border-radius:18px 18px 4px 18px; padding:11px 16px;
               margin:8px 0 8px 18%; font-size:0.91rem; color:var(--dark);
               font-family:'DM Sans',sans-serif; line-height:1.55; }
  .chat-lyra { background:#ffffff; border:0.5px solid var(--blush);
               border-radius:18px 18px 18px 4px; padding:11px 16px;
               margin:8px 18% 8px 0; font-size:0.91rem; color:var(--dark);
               font-family:'DM Sans',sans-serif; line-height:1.55; }
  .lyra-label { font-size:0.72rem; color:var(--rose); font-weight:500; margin-bottom:3px;
                font-family:'DM Sans',sans-serif; letter-spacing:0.05em; text-transform:uppercase; }
  .gemini-badge { text-align:center; font-size:0.72rem; color:#aaa; margin-top:6px;
                  font-family:'DM Sans',sans-serif; }
  #MainMenu, footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ─── HEADER ──────────────────────────────────────────────────────────────────

st.markdown("""
<div class="brand-header">
  <div class="brand-name">✨ Forever 21 Beauty Studio</div>
  <div class="brand-tagline">Always Young, Always Beautiful.</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─── SESSION STATE ───────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []
if "leads_captured" not in st.session_state:
    st.session_state.leads_captured = []

# ─── LEAD BANNERS ────────────────────────────────────────────────────────────

for lead in st.session_state.leads_captured:
    st.markdown(f"""
    <div class="lead-banner">
      ✅ <strong>Consultation request saved!</strong><br>
      Bini will personally call <strong>{lead['name']}</strong>
      at <strong>{lead['phone']}</strong> very soon.
    </div>
    """, unsafe_allow_html=True)

# ─── CHAT DISPLAY ────────────────────────────────────────────────────────────

if not st.session_state.messages:
    st.markdown("""
    <div class="lyra-label">Lyra — Forever 21</div>
    <div class="chat-lyra">
      Namaste! I'm Lyra, your personal beauty consultant at
      Forever 21 Beauty Studio. 💐<br><br>
      Whether you're dreaming of glowing skin, gorgeous hair, or a
      complete bridal transformation — you've come to the right place.<br><br>
      How can I help you today?<br><br>
      <em>You can also chat in हिन्दी or ଓଡ଼ିଆ — whichever feels most comfortable!</em>
    </div>
    <div class="gemini-badge">Powered by Gemini 2.5 Flash</div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        display = clean_response(msg["content"])
        st.markdown(
            f'<div class="lyra-label">Lyra — Forever 21</div>'
            f'<div class="chat-lyra">{display}</div>',
            unsafe_allow_html=True)

# ─── CHAT INPUT & GEMINI CALL ────────────────────────────────────────────────

user_input = st.chat_input("Type in English, हिन्दी, or ଓଡ଼ିଆ...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    client = get_gemini_client()
    history = build_history(st.session_state.messages[:-1])

    with st.spinner("Lyra is thinking..."):
        try:
            contents = history + [types.Content(
                role="user",
                parts=[types.Part(text=user_input)]
            )]

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                    max_output_tokens=1024,
                ),
            )

            lyra_reply = response.text if response.text else (
                "I didn't quite catch that — could you rephrase? "
                "I'm here to help! Always Young, Always Beautiful! ✨"
            )

        except Exception as e:
            lyra_reply = (
                "I'm so sorry, something went wrong. "
                "Please call us directly at +91 98531 15511. "
                "Always Young, Always Beautiful! ✨"
            )
            st.error(f"Gemini error: {e}")

    name, phone = extract_lead(lyra_reply)
    if name and phone:
        already_saved = any(
            l["name"] == name and l["phone"] == phone
            for l in st.session_state.leads_captured
        )
        if not already_saved:
            if save_lead(name, phone):
                st.session_state.leads_captured.append({"name": name, "phone": phone})

    st.session_state.messages.append({"role": "assistant", "content": lyra_reply})
    st.rerun()

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### ✨ Forever 21 Beauty Studio")
    st.markdown("*Always Young, Always Beautiful.*")
    st.divider()

    st.markdown("**Studio**")
    st.markdown("📍 MIG, Lane - 3, Kalinga Vihar (K9A)")
    st.markdown("🌆 Bhubaneswar - 751019, Odisha")
    st.markdown("🏛️ Near Vivanta Hotel & D N Regalia Mall")
    st.markdown("📞 [+91 98531 15511](tel:+919853115511)")
    st.divider()

    st.markdown("**Session stats**")
    st.markdown(f"💬 Messages: **{len(st.session_state.messages)}**")
    st.markdown(f"📋 Leads today: **{len(st.session_state.leads_captured)}**")
    st.divider()

    if st.session_state.leads_captured:
        st.markdown("**Leads this session**")
        for i, lead in enumerate(st.session_state.leads_captured, 1):
            st.markdown(f"{i}. **{lead['name']}** — {lead['phone']}")
        st.divider()

    if st.button("🔄 Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.leads_captured = []
        st.rerun()

    st.caption("Engine: Gemini 2.5 Flash · Paid Tier")
    st.caption("Leads: Google Sheets")
    st.caption("Built for Bini · Forever 21 Beauty Studio")
