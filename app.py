# VERSION: 4.1 — Single HTML block for left panel, fixes overflow
import streamlit as st
import re
import base64
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from google import genai
from google.genai import types

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Forever 21 Beauty Studio – Lyra",
    page_icon="💄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;700&display=swap');

html, body, [class*="css"] { font-family: 'Lato', sans-serif; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container { padding-top: 0.5rem !important; padding-bottom: 1rem !important; }

/* ── FESTIVAL BANNER ── */
.festival-banner {
    background: linear-gradient(90deg, #880e4f, #c2185b, #880e4f);
    color: white;
    text-align: center;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 0.8rem;
    letter-spacing: 0.3px;
    box-shadow: 0 2px 8px rgba(136,14,79,0.35);
    animation: pulse-banner 3s ease-in-out infinite;
}
@keyframes pulse-banner { 0%,100%{opacity:1;} 50%{opacity:0.82;} }

/* ── HEADER ── */
.lyra-header {
    background: linear-gradient(135deg, #8B3A62 0%, #C2185B 50%, #8B3A62 100%);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 14px;
    margin-bottom: 0.8rem;
    text-align: center;
    box-shadow: 0 4px 18px rgba(139,58,98,0.35);
}
.lyra-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    margin: 0 0 0.1rem 0;
}
.lyra-header p { font-size: 0.82rem; margin: 0; opacity: 0.88; }

/* ── WELCOME BOX ── */
.welcome-box {
    background: linear-gradient(135deg, #fff9fb 0%, #fce4ec 100%);
    border-left: 4px solid #C2185B;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.8rem;
    font-size: 0.87rem;
    line-height: 1.65;
    color: #3a3a3a;
}
.welcome-title {
    font-family: 'Playfair Display', serif;
    font-size: 0.97rem;
    font-weight: 600;
    color: #8B3A62;
    margin-bottom: 0.35rem;
}
.lang-chip {
    display: inline-block;
    background: #8B3A62;
    color: white;
    border-radius: 20px;
    padding: 0.15rem 0.55rem;
    font-size: 0.73rem;
    font-weight: 600;
    margin: 0.3rem 0.2rem 0 0;
}

/* ── INFO PANEL (left column) ── */
.info-panel {
    background: linear-gradient(180deg, #2d1b2e 0%, #4a1942 100%);
    border-radius: 14px;
    padding: 1rem 0.9rem;
    color: white;
    height: 100%;
    min-height: 600px;
}
.panel-logo-text {
    text-align: center;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 0.8rem;
}
.panel-section {
    background: rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 0.65rem 0.75rem;
    margin-bottom: 0.65rem;
    border: 1px solid rgba(255,255,255,0.1);
    color: white;
    font-size: 0.8rem;
    line-height: 1.7;
}
.panel-title {
    font-family: 'Playfair Display', serif;
    font-size: 0.88rem;
    font-weight: 600;
    color: #f8bbd0;
    margin-bottom: 0.35rem;
}
.panel-link {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 0.2rem 0.6rem;
    margin: 0.15rem 0.15rem 0 0;
    font-size: 0.76rem;
    text-decoration: none;
    border: 1px solid rgba(255,255,255,0.2);
    color: white;
}
.panel-link:hover { background: rgba(255,255,255,0.22); color: white; }
.hours-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.77rem;
    padding: 0.15rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    color: white;
}
.service-chip {
    display: inline-block;
    background: rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 0.12rem 0.5rem;
    font-size: 0.7rem;
    margin: 0.08rem;
    border: 1px solid rgba(255,255,255,0.15);
    color: white;
}
.wa-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    background: #25D366;
    color: white !important;
    border-radius: 10px;
    padding: 0.45rem 0.7rem;
    text-decoration: none !important;
    font-weight: 700;
    font-size: 0.82rem;
    margin-top: 0.45rem;
    box-shadow: 0 2px 6px rgba(37,211,102,0.3);
}
.wa-btn:hover { background: #1da851; }

/* ── CHAT INPUT ── */
.stChatInput > div {
    border: 2.5px solid #C2185B !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 12px rgba(194,24,91,0.15) !important;
}

/* ── LEAD BANNER ── */
.lead-banner {
    background: linear-gradient(90deg, #1b5e20, #2e7d32);
    color: white;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
    margin-top: 0.5rem;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ── Festival Banner ─────────────────────────────────────────────────────────────
# TO CHANGE: Edit the text between the quotes below, then push to GitHub.
# TO HIDE:   Set FESTIVAL_BANNER = ""
FESTIVAL_BANNER = "🌸 Wedding Season Special — Book your Bridal Package now! Call Bini Didi: +91 98531 15511"

# ── Load system prompt ──────────────────────────────────────────────────────────
@st.cache_data
def load_system_prompt():
    try:
        with open("system_prompt.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "You are Lyra, a helpful beauty consultant for Forever 21 Beauty Studio."

# ── Load logo ───────────────────────────────────────────────────────────────────
@st.cache_data
def load_logo():
    try:
        with open("forever21_logo.png", "rb") as f:
            data = base64.b64encode(f.read()).decode()
            return f"data:image/png;base64,{data}"
    except FileNotFoundError:
        return None

# ── Gemini client ───────────────────────────────────────────────────────────────
@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

# ── Google Sheets ───────────────────────────────────────────────────────────────
def save_lead_to_sheet(name: str, phone: str, source: str = "Website"):
    try:
        sa_info = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(
            sa_info, scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        gc = gspread.authorize(creds)
        sheet = gc.open_by_key(st.secrets["GOOGLE_SHEET_ID"]).worksheet("Leads")
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
        sheet.append_row([timestamp, name, phone, "New Lead", source])
        return True
    except Exception as e:
        st.error(f"Sheet error: {e}")
        return False

# ── Service categories ──────────────────────────────────────────────────────────
SERVICE_CATEGORIES = [
    "Threading", "Waxing", "Bleach", "Cleanup", "De Tan",
    "Facial", "Hydra Facial", "Hair Cut", "Hair Colour",
    "Hair Spa", "Hair Treatment", "Hair Wash", "Hair Style",
    "Pedicure & Manicure", "Make-Up", "Nail Art", "Mehendi",
    "Body Massage", "Piercing", "Saree Draping"
]

# ── Chat ────────────────────────────────────────────────────────────────────────
def chat_with_lyra(messages: list, system_prompt: str) -> str:
    client = get_gemini_client()
    gemini_messages = []
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        gemini_messages.append(
            types.Content(role=role, parts=[types.Part(text=m["content"])])
        )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=system_prompt),
        contents=gemini_messages,
    )
    return response.text

def extract_lead(text: str):
    pattern = r'LEAD_CAPTURED:\{"name":"([^"]+)","phone":"([^"]+)"\}'
    match = re.search(pattern, text)
    if match:
        clean = re.sub(pattern, "", text).strip()
        return clean, match.group(1), match.group(2)
    return text, None, None

# ── Session state ───────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "lead_saved" not in st.session_state:
    st.session_state.lead_saved = False

system_prompt = load_system_prompt()
logo_src = load_logo()

# ══════════════════════════════════════════════════════════════════════
# FESTIVAL BANNER
# ══════════════════════════════════════════════════════════════════════
if FESTIVAL_BANNER:
    st.markdown(f"<div class='festival-banner'>🎉 {FESTIVAL_BANNER}</div>",
                unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# TWO COLUMN LAYOUT
# ══════════════════════════════════════════════════════════════════════
left_col, right_col = st.columns([1, 2.4])

# ── LEFT COLUMN — Info Panel ────────────────────────────────────────
with left_col:
    # Build entire left panel as ONE single HTML block
    chips = "".join([f"<span class='service-chip'>{s}</span>" for s in SERVICE_CATEGORIES])
    
    if logo_src:
        logo_html = f"<div style='text-align:center; padding-bottom:0.8rem; border-bottom:1px solid rgba(255,255,255,0.1); margin-bottom:0.8rem;'><img src='{logo_src}' style='max-width:130px; border-radius:8px;'/></div>"
    else:
        logo_html = "<div style='text-align:center; padding-bottom:0.8rem; border-bottom:1px solid rgba(255,255,255,0.1); margin-bottom:0.8rem;'><div style='font-size:2rem;'>💄</div><div style='font-family:Playfair Display,serif; font-size:1rem; font-weight:700; color:#f8bbd0;'>Forever 21</div><div style='font-size:0.7rem; color:#e0b0c8; letter-spacing:1px; text-transform:uppercase;'>Beauty Studio</div></div>"

    panel_html = f"""
    <div style='background:linear-gradient(180deg,#2d1b2e 0%,#4a1942 100%);
                border-radius:14px; padding:1rem 0.9rem; color:white;
                min-height:600px; font-family:Lato,sans-serif;'>
        {logo_html}
        <div style='background:rgba(255,255,255,0.07); border-radius:10px;
                    padding:0.65rem 0.75rem; margin-bottom:0.65rem;
                    border:1px solid rgba(255,255,255,0.1); font-size:0.8rem; line-height:1.7;'>
            <div style='font-family:Playfair Display,serif; font-size:0.88rem;
                        font-weight:600; color:#f8bbd0; margin-bottom:0.35rem;'>📍 Find Us</div>
            <span style='color:white;'>MIG, Lane-3, Kalinga Vihar (K9A)<br>
            Bhubaneswar – 751019, Odisha<br>
            <span style='opacity:0.7; font-size:0.73rem;'>Near Vivanta Hotel & D N Regalia Mall</span></span><br>
            <a href='https://maps.app.goo.gl/B7oszYnEmBxMxLVe8' target='_blank'
               style='display:inline-flex; align-items:center; gap:0.35rem;
                      background:rgba(255,255,255,0.12); border-radius:20px;
                      padding:0.2rem 0.6rem; margin-top:0.3rem; font-size:0.76rem;
                      text-decoration:none; color:white; border:1px solid rgba(255,255,255,0.2);'>
               🗺️ Open in Maps</a>
        </div>
        <div style='background:rgba(255,255,255,0.07); border-radius:10px;
                    padding:0.65rem 0.75rem; margin-bottom:0.65rem;
                    border:1px solid rgba(255,255,255,0.1); font-size:0.8rem;'>
            <div style='font-family:Playfair Display,serif; font-size:0.88rem;
                        font-weight:600; color:#f8bbd0; margin-bottom:0.35rem;'>📞 Contact Us</div>
            <a href='tel:+919853115511'
               style='display:inline-flex; align-items:center; gap:0.35rem;
                      background:rgba(255,255,255,0.12); border-radius:20px;
                      padding:0.2rem 0.6rem; font-size:0.76rem; text-decoration:none;
                      color:white; border:1px solid rgba(255,255,255,0.2);'>
               📱 +91 98531 15511</a><br>
            <a href='https://wa.me/919853115511?text=Namaskar%20Bini%20Didi!%20I%20would%20like%20to%20know%20more%20about%20your%20services.'
               target='_blank'
               style='display:flex; align-items:center; justify-content:center; gap:0.4rem;
                      background:#25D366; color:white; border-radius:10px;
                      padding:0.45rem 0.7rem; text-decoration:none; font-weight:700;
                      font-size:0.82rem; margin-top:0.45rem;
                      box-shadow:0 2px 6px rgba(37,211,102,0.3);'>
               💬 Chat on WhatsApp</a>
        </div>
        <div style='background:rgba(255,255,255,0.07); border-radius:10px;
                    padding:0.65rem 0.75rem; margin-bottom:0.65rem;
                    border:1px solid rgba(255,255,255,0.1); font-size:0.8rem;'>
            <div style='font-family:Playfair Display,serif; font-size:0.88rem;
                        font-weight:600; color:#f8bbd0; margin-bottom:0.35rem;'>🕐 Working Hours</div>
            <div style='display:flex; justify-content:space-between; padding:0.15rem 0;
                        border-bottom:1px solid rgba(255,255,255,0.06); color:white;'>
                <span>Mon – Sat</span><span style='color:#f8bbd0;'>10 AM – 8 PM</span>
            </div>
            <div style='display:flex; justify-content:space-between; padding:0.15rem 0; color:white;'>
                <span>Sunday</span><span style='color:#f8bbd0;'>10 AM – 6 PM</span>
            </div>
            <div style='font-size:0.68rem; opacity:0.6; margin-top:0.3rem; color:white;'>
                * Confirm timings while booking</div>
        </div>
        <div style='background:rgba(255,255,255,0.07); border-radius:10px;
                    padding:0.65rem 0.75rem; margin-bottom:0.65rem;
                    border:1px solid rgba(255,255,255,0.1); font-size:0.8rem;'>
            <div style='font-family:Playfair Display,serif; font-size:0.88rem;
                        font-weight:600; color:#f8bbd0; margin-bottom:0.35rem;'>💅 Our Services</div>
            {chips}
        </div>
        <div style='background:rgba(255,255,255,0.07); border-radius:10px;
                    padding:0.65rem 0.75rem; margin-bottom:0.65rem;
                    border:1px solid rgba(255,255,255,0.1); font-size:0.8rem;'>
            <div style='font-family:Playfair Display,serif; font-size:0.88rem;
                        font-weight:600; color:#f8bbd0; margin-bottom:0.35rem;'>🌐 Follow & Review Us</div>
            <a href='https://www.instagram.com/forever_21_beauty_studio?igsh=MWwxenQ0cHI1YmlidQ=='
               target='_blank'
               style='display:inline-flex; align-items:center; gap:0.35rem;
                      background:rgba(255,255,255,0.12); border-radius:20px;
                      padding:0.2rem 0.6rem; margin:0.15rem 0.1rem 0 0; font-size:0.76rem;
                      text-decoration:none; color:white; border:1px solid rgba(255,255,255,0.2);'>
               📸 Instagram</a>
            <a href='https://www.facebook.com/share/17J8yCJafA/' target='_blank'
               style='display:inline-flex; align-items:center; gap:0.35rem;
                      background:rgba(255,255,255,0.12); border-radius:20px;
                      padding:0.2rem 0.6rem; margin:0.15rem 0.1rem 0 0; font-size:0.76rem;
                      text-decoration:none; color:white; border:1px solid rgba(255,255,255,0.2);'>
               👍 Facebook</a>
            <a href='https://share.google/nZogQL8Y5usCwPmWy' target='_blank'
               style='display:inline-flex; align-items:center; gap:0.35rem;
                      background:rgba(255,255,255,0.12); border-radius:20px;
                      padding:0.2rem 0.6rem; margin:0.15rem 0.1rem 0 0; font-size:0.76rem;
                      text-decoration:none; color:white; border:1px solid rgba(255,255,255,0.2);'>
               ⭐ Google</a>
        </div>
        <div style='text-align:center; padding:0.6rem 0 0.2rem 0;
                    font-size:0.7rem; opacity:0.45; font-style:italic; color:white;'>
            "Always Young, Always Beautiful."
        </div>
    </div>
    """
    st.markdown(panel_html, unsafe_allow_html=True)

# ── RIGHT COLUMN — Chat ─────────────────────────────────────────────
with right_col:

    # Header
    st.markdown("""
    <div class='lyra-header'>
        <h1>✨ Forever 21 Beauty Studio</h1>
        <p>Powered by Lyra AI • Your Personal Beauty Consultant</p>
    </div>""", unsafe_allow_html=True)

    # Welcome box
    st.markdown("""
    <div class='welcome-box'>
        <div class='welcome-title'>
            Namaskar! I'm Lyra, your Digital Host at Forever 21 Beauty Studio. 🌸
        </div>
        With Bini Didi, I'm here to help you remain
        <em>Always Young and Always Beautiful.</em><br><br>
        How can I help you to be a glowing beauty today?
        <div style='margin-top:0.4rem;'>
            <span class='lang-chip'>🇬🇧 English</span>
            <span class='lang-chip'>🇮🇳 हिन्दी</span>
            <span class='lang-chip'>🏝️ ଓଡ଼ିଆ</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # Chat input
    user_input = st.chat_input("💬 Type your message here and press Enter…")

    # Chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Process input
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Lyra is thinking…"):
                raw = chat_with_lyra(st.session_state.messages, system_prompt)

            display_text, lead_name, lead_phone = extract_lead(raw)
            st.markdown(display_text)

            if lead_name and lead_phone and not st.session_state.lead_saved:
                saved = save_lead_to_sheet(lead_name, lead_phone, source="Website")
                if saved:
                    st.session_state.lead_saved = True
                    st.markdown(f"""
                    <div class='lead-banner'>
                        ✅ Thank you, {lead_name}!
                        Bini Didi will call you at {lead_phone} shortly. 🌸
                    </div>""", unsafe_allow_html=True)

        st.session_state.messages.append(
            {"role": "assistant", "content": display_text}
        )

    # Clear button
    if st.session_state.messages:
        if st.button("🔄 Start New Conversation", use_container_width=False):
            st.session_state.messages = []
            st.session_state.lead_saved = False
            st.rerun()
