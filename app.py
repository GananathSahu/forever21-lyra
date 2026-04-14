# VERSION: 5.2 — Remove planner, fix tagline, chips with duration, address, language tabs
import streamlit as st
import streamlit.components.v1 as components
import re
import base64
import hashlib
from datetime import datetime, date
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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Lato:wght@300;400;700&display=swap');

html, body, [class*="css"] { font-family: 'Lato', sans-serif; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container { padding-top: 0.5rem !important; padding-bottom: 1rem !important; }

/* ── FESTIVAL BANNER ── */
.festival-banner {
    background: linear-gradient(90deg, #880e4f, #c2185b, #880e4f);
    color: white; text-align: center;
    padding: 0.5rem 1rem; border-radius: 8px;
    font-size: 0.85rem; font-weight: 600;
    margin-bottom: 0.8rem; letter-spacing: 0.3px;
    box-shadow: 0 2px 8px rgba(136,14,79,0.35);
}

/* ── HEADER ── */
.lyra-header {
    background: linear-gradient(135deg, #8B3A62 0%, #C2185B 50%, #8B3A62 100%);
    color: white; padding: 1rem 1.5rem;
    border-radius: 14px; margin-bottom: 0.8rem;
    text-align: center; box-shadow: 0 4px 18px rgba(139,58,98,0.35);
}
.lyra-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem; font-weight: 700; margin: 0 0 0.1rem 0;
}
.lyra-header p { font-size: 0.82rem; margin: 0; opacity: 0.88; }

/* ── TAGLINE STYLE ── */
.tagline {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    color: #C2185B;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-shadow: 0 1px 3px rgba(194,24,91,0.25);
}

/* ── WELCOME BOX ── */
.welcome-box {
    background: linear-gradient(135deg, #fff9fb 0%, #fce4ec 100%);
    border-left: 4px solid #C2185B; border-radius: 10px;
    padding: 0.8rem 1rem; margin-bottom: 0.8rem;
    font-size: 0.87rem; line-height: 1.65; color: #3a3a3a;
}
.welcome-title {
    font-family: 'Playfair Display', serif;
    font-size: 0.97rem; font-weight: 600; color: #8B3A62; margin-bottom: 0.35rem;
}
.lang-chip {
    display: inline-block; background: #8B3A62; color: white;
    border-radius: 20px; padding: 0.15rem 0.55rem;
    font-size: 0.73rem; font-weight: 600; margin: 0.3rem 0.2rem 0 0;
}

/* ── CHAT INPUT ── */
.stChatInput > div {
    border: 2.5px solid #C2185B !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 12px rgba(194,24,91,0.15) !important;
}

/* ── LEAD BANNER ── */
.lead-banner {
    background: linear-gradient(90deg, #1b5e20, #2e7d32);
    color: white; border-radius: 10px;
    padding: 0.6rem 1rem; font-size: 0.85rem;
    margin-top: 0.5rem; font-weight: 600;
}

/* ── DURATION PLANNER ── */
.planner-box {
    background: linear-gradient(135deg, #fce4ec, #fff9fb);
    border: 2px solid #C2185B; border-radius: 12px;
    padding: 0.9rem 1rem; margin-bottom: 0.8rem;
}
.planner-title {
    font-family: 'Playfair Display', serif;
    color: #8B3A62; font-size: 1rem; font-weight: 700;
    margin-bottom: 0.5rem;
}
.duration-result {
    background: #8B3A62; color: white;
    border-radius: 10px; padding: 0.6rem 1rem;
    font-size: 0.88rem; margin-top: 0.6rem; font-weight: 600;
}

/* ── GALLERY ── */
.gallery-card {
    border-radius: 12px; overflow: hidden;
    border: 2px solid #f8bbd0;
    box-shadow: 0 3px 10px rgba(139,58,98,0.15);
    margin-bottom: 0.8rem;
}
.gallery-label {
    background: #8B3A62; color: white;
    padding: 0.35rem 0.7rem; font-size: 0.78rem; font-weight: 600;
}

/* ── ADMIN ── */
.admin-metric {
    background: linear-gradient(135deg, #8B3A62, #C2185B);
    color: white; border-radius: 12px;
    padding: 1rem; text-align: center;
    margin-bottom: 0.5rem;
}
.admin-metric .metric-value {
    font-size: 2rem; font-weight: 700;
    font-family: 'Playfair Display', serif;
}
.admin-metric .metric-label {
    font-size: 0.78rem; opacity: 0.88;
}
.status-new { background: #e3f2fd; color: #1565c0; border-radius: 20px; padding: 0.15rem 0.6rem; font-size: 0.75rem; font-weight: 600; }
.status-called { background: #fff8e1; color: #f57f17; border-radius: 20px; padding: 0.15rem 0.6rem; font-size: 0.75rem; font-weight: 600; }
.status-booked { background: #e8f5e9; color: #2e7d32; border-radius: 20px; padding: 0.15rem 0.6rem; font-size: 0.75rem; font-weight: 600; }
.status-lost { background: #ffebee; color: #c62828; border-radius: 20px; padding: 0.15rem 0.6rem; font-size: 0.75rem; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── Config ─────────────────────────────────────────────────────────────────────
FESTIVAL_BANNER = "🌸 Wedding Season Special — Book your Bridal Package now! Call Bini Didi: +91 98531 15511"
ADMIN_PASSWORD_HASH = hashlib.sha256("Bini".encode()).hexdigest()

# ── Service data with durations ────────────────────────────────────────────────
SERVICES_WITH_DURATION = {
    "Threading": {
        "Eyebrow": 30, "Upper Lip": 30, "Chin": 30,
        "Forehead": 30, "Full Face": 30
    },
    "Waxing": {
        "Half Arms": 30, "Full Arms": 30, "Under Arms": 30,
        "Half Legs": 30, "Full Legs": 60, "Full Body": 90,
        "Full Face": 30, "Back": 20, "Belly": 20, "Foot": 15
    },
    "Bleach": {
        "Fruit Bleach": 30, "Gold Bleach": 30,
        "Oxy Bleach": 30, "Back Bleach": 20
    },
    "Cleanup": {
        "Fruit": 30, "Aroma": 30, "Lotus": 30, "Shahnaz": 30,
        "Anti Tan": 30, "De Tan": 30, "Papaya": 30,
        "Acne Cleanup": 30, "Natures Gold": 35, "Natures Diamond": 35
    },
    "De Tan": {
        "Face": 30, "Hand": 30, "Leg": 30,
        "Foot": 20, "Back": 20
    },
    "Facial": {
        "Fruit / Mix Fruit": 30, "Gold / Pearl / Diamond": 60,
        "Aroma Magic": 60, "Lotus": 60, "Panchatatva": 60,
        "Anti Acne / Anti Tan": 30, "Wine Facial": 60,
        "Vitamin C": 60, "Shahnaz Gold": 60, "O3+ Bridal": 60,
        "Anti Aging / Anti Pigment": 80, "Lacto Protein": 80,
        "Biolume H2O": 60, "Biolume Bridal": 90
    },
    "Hydra Facial": {
        "Silver / Pearl / Bridal": 120, "Vitamin C": 120,
        "Calendula Chia Seed": 120, "Lavender Orchid": 120,
        "Kale Extract": 120, "Dragon Fruit Matcha": 120,
        "Totally Flawless": 120, "Aroma Skin Glow": 90
    },
    "Hair Cut": {
        "Straight / U / V": 30, "Blunt / Feather / Layer": 30,
        "Mushroom / Step / Butterfly": 30, "Kids": 30, "Front": 15
    },
    "Hair Colour": {
        "Root Touch": 30, "Full Application": 30,
        "Ombre": 60, "Global": 60, "Balayage": 60,
        "Henna": 30, "Wash & Dry": 30
    },
    "Hair Spa": {
        "Deep Conditioning": 30, "Berina / Wella / Loreal": 30,
        "Berina Collagen": 30
    },
    "Hair Treatment": {
        "Straightening": 180, "Smoothening": 180,
        "Rebonding": 180, "Keratin": 180,
        "Botox": 180, "Dandruff Treatment": 180
    },
    "Hair Wash": {
        "Wash & Dry": 15, "Wash & Blow Dry": 15, "Only Blow Dry": 15
    },
    "Hair Style": {
        "Crimping": 30, "Temporary Curl": 20,
        "Temporary Straightening": 130, "Full Hair Style": 60
    },
    "Pedicure & Manicure": {
        "Pedicure (Standard)": 30, "Pedicure Premium / Ozone": 60,
        "Manicure (Standard)": 30, "Manicure Ozone": 45
    },
    "Make-Up": {
        "Light / Party": 60, "Reception / Bridal": 60,
        "HD Bridal": 60, "Engagement": 120
    },
    "Nail Art / Extension": {
        "Nail Extension / Nail Art": 60, "Nail Filling": 20
    },
    "Mehendi": {
        "Hand Mehendi": 60, "Hair Mehendi": 120
    },
    "Body": {
        "Body Massage": 60, "Hair Oil Massage": 40
    },
    "Piercing": {
        "Ear Piercing": 30, "Nose Piercing": 30, "Ear Lobing": 30
    },
    "Saree Draping": {
        "Saree Draping": 30
    }
}

# ── Gallery data (placeholders — Bini to update with real photos/videos) ───────
GALLERY_ITEMS = [
    {
        "category": "Bridal Makeup",
        "label": "💍 Bridal Transformation",
        "type": "placeholder",
        "youtube": "",
        "description": "HD Bridal Makeup — Radiant & Timeless"
    },
    {
        "category": "Facial",
        "label": "✨ Glow Facial",
        "type": "placeholder",
        "youtube": "",
        "description": "Hydra Facial — Before & After"
    },
    {
        "category": "Hair Treatment",
        "label": "💇 Hair Transformation",
        "type": "placeholder",
        "youtube": "",
        "description": "Keratin Treatment — Silky Smooth Results"
    },
    {
        "category": "Mehendi",
        "label": "🌿 Bridal Mehendi",
        "type": "placeholder",
        "youtube": "",
        "description": "Intricate Bridal Mehendi Design"
    },
    {
        "category": "Nail Art",
        "label": "💅 Nail Art",
        "type": "placeholder",
        "youtube": "",
        "description": "Custom Nail Extension & Art"
    },
    {
        "category": "Hair Colour",
        "label": "🎨 Hair Colour",
        "type": "placeholder",
        "youtube": "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "description": "Balayage & Global Colour — Stunning Results"
    },
]

# ── Helper functions ────────────────────────────────────────────────────────────
@st.cache_data
def load_system_prompt():
    try:
        with open("system_prompt.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "You are Lyra, a helpful beauty consultant for Forever 21 Beauty Studio."

@st.cache_data
def load_logo():
    try:
        with open("forever21_logo.png", "rb") as f:
            data = base64.b64encode(f.read()).decode()
            return f"data:image/png;base64,{data}"
    except FileNotFoundError:
        return None

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

def get_sheet():
    sa_info = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(
        sa_info, scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    gc = gspread.authorize(creds)
    return gc.open_by_key(st.secrets["GOOGLE_SHEET_ID"]).worksheet("Leads")

def save_lead_to_sheet(name: str, phone: str, source: str = "Website"):
    try:
        sheet = get_sheet()
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
        sheet.append_row([timestamp, name, phone, "New Lead", source])
        return True
    except Exception as e:
        st.error(f"Sheet error: {e}")
        return False

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

def format_duration(minutes: int) -> str:
    if minutes < 60:
        return f"{minutes} minutes"
    h = minutes // 60
    m = minutes % 60
    if m == 0:
        return f"{h} hour{'s' if h > 1 else ''}"
    return f"{h} hour{'s' if h > 1 else ''} {m} minutes"

# ── Session state ───────────────────────────────────────────────────────────────
for key, val in [
    ("messages", []), ("lead_saved", False),
    ("admin_logged_in", False), ("page", "chat")
]:
    if key not in st.session_state:
        st.session_state[key] = val

system_prompt = load_system_prompt()
logo_src = load_logo()

# ── Build left panel HTML ───────────────────────────────────────────────────────
def build_left_panel(logo_src):
    if logo_src:
        logo_html = f"""
        <div style='text-align:center; padding-bottom:0.8rem;
             border-bottom:1px solid rgba(255,255,255,0.15); margin-bottom:0.8rem;'>
            <div style='background:white; border-radius:10px;
                 padding:0.6rem 0.8rem; display:inline-block;
                 border:2px solid rgba(248,187,208,0.6);
                 box-shadow:0 2px 8px rgba(0,0,0,0.2);'>
                <img src='{logo_src}' style='max-width:120px; border-radius:4px;
                     display:block;'/>
            </div>
        </div>"""
    else:
        logo_html = """
        <div style='text-align:center; padding-bottom:0.8rem;
             border-bottom:1px solid rgba(255,255,255,0.15); margin-bottom:0.8rem;'>
            <div style='font-size:2rem;'>💄</div>
            <div style='font-family:Playfair Display,serif; font-size:1rem;
                 font-weight:700; color:#f8bbd0;'>Forever 21</div>
            <div style='font-size:0.7rem; color:#e0b0c8; letter-spacing:1px;
                 text-transform:uppercase;'>Beauty Studio</div>
        </div>"""

    def section(title, body):
        return f"""
        <div style='background:rgba(255,255,255,0.07); border-radius:10px;
                    padding:0.65rem 0.75rem; margin-bottom:0.65rem;
                    border:1px solid rgba(255,255,255,0.1); font-size:0.8rem; line-height:1.7;'>
            <div style='font-family:Playfair Display,serif; font-size:0.88rem;
                        font-weight:600; color:#f8bbd0; margin-bottom:0.35rem;'>{title}</div>
            {body}
        </div>"""

    def link_btn(href, label, extra=""):
        return f"""<a href='{href}' target='_blank'
            style='display:inline-flex; align-items:center; gap:0.35rem;
                   background:rgba(255,255,255,0.12); border-radius:20px;
                   padding:0.2rem 0.6rem; margin:0.15rem 0.1rem 0 0; font-size:0.76rem;
                   text-decoration:none; color:white;
                   border:1px solid rgba(255,255,255,0.2); {extra}'>{label}</a>"""

    location_body = f"""
        <span style='color:white;'>Lane-3, Kalinga Vihar (K9A)<br>
        Bhubaneswar – 751019, Odisha<br>
        <span style='opacity:0.7; font-size:0.73rem;'>Near Vivanta Hotel & D N Regalia Mall</span></span><br>
        {link_btn('https://maps.app.goo.gl/B7oszYnEmBxMxLVe8', '🗺️ Open in Maps')}"""

    contact_body = f"""
        {link_btn('tel:+919853115511', '📱 +91 98531 15511')}
        <a href='https://wa.me/919853115511?text=Namaskar%20Bini%20Didi!%20I%20would%20like%20to%20know%20more%20about%20your%20services.'
           target='_blank'
           style='display:flex; align-items:center; justify-content:center; gap:0.4rem;
                  background:#25D366; color:white; border-radius:10px;
                  padding:0.45rem 0.7rem; text-decoration:none; font-weight:700;
                  font-size:0.82rem; margin-top:0.45rem;
                  box-shadow:0 2px 6px rgba(37,211,102,0.3);'>
            💬 Chat on WhatsApp</a>"""

    hours_body = """
        <div style='display:flex; justify-content:space-between; padding:0.15rem 0;
                    border-bottom:1px solid rgba(255,255,255,0.06); color:white;'>
            <span>Mon – Sat</span><span style='color:#f8bbd0;'>10 AM – 8 PM</span>
        </div>
        <div style='display:flex; justify-content:space-between; padding:0.15rem 0; color:white;'>
            <span>Sunday</span><span style='color:#f8bbd0;'>10 AM – 6 PM</span>
        </div>
        <div style='font-size:0.68rem; opacity:0.6; margin-top:0.3rem; color:white;'>
            * Confirm timings while booking</div>"""

    cats = list(SERVICES_WITH_DURATION.keys())
    chips = "".join([
        f"<span style='display:inline-block; background:rgba(255,255,255,0.1);"
        f"border-radius:20px; padding:0.12rem 0.5rem; font-size:0.7rem; margin:0.08rem;"
        f"border:1px solid rgba(255,255,255,0.15); color:white;'>{s}</span>"
        for s in cats
    ])

    social_body = (
        link_btn('https://www.instagram.com/forever_21_beauty_studio?igsh=MWwxenQ0cHI1YmlidQ==', '📸 Instagram') +
        link_btn('https://www.facebook.com/share/17J8yCJafA/', '👍 Facebook') +
        link_btn('https://share.google/nZogQL8Y5usCwPmWy', '⭐ Google')
    )

    tagline = """
        <div style='text-align:center; padding:0.7rem 0 0.2rem 0;'>
            <span style='font-family:Playfair Display,serif; font-style:italic;
                 font-size:0.78rem; font-weight:600; color:#f8bbd0; letter-spacing:0.5px;'>
                ✨ "Always Young, Always Beautiful." ✨</span>
        </div>"""

    return f"""
    <div style='background:linear-gradient(180deg,#2d1b2e 0%,#4a1942 100%);
                border-radius:14px; padding:1rem 0.9rem; color:white;
                font-family:Lato,sans-serif;'>
        {logo_html}
        {section('📍 Find Us', location_body)}
        {section('📞 Contact Us', contact_body)}
        {section('🕐 Working Hours', hours_body)}
        {section('💅 Our Services', chips)}
        {section('🌐 Follow & Review Us', social_body)}
        {tagline}
    </div>"""

# ══════════════════════════════════════════════════════════════════════
# PAGE NAVIGATION
# ══════════════════════════════════════════════════════════════════════
col_nav1, col_nav2, col_nav3, col_nav4 = st.columns([2, 1, 1, 1])
with col_nav1:
    if FESTIVAL_BANNER:
        st.markdown(f"<div class='festival-banner'>🎉 {FESTIVAL_BANNER}</div>",
                    unsafe_allow_html=True)
with col_nav2:
    if st.button("💬 Chat with Lyra", use_container_width=True):
        st.session_state.page = "chat"
        st.rerun()
with col_nav3:
    if st.button("🖼️ Gallery", use_container_width=True):
        st.session_state.page = "gallery"
        st.rerun()
with col_nav4:
    if st.button("🔐 Bini's Dashboard", use_container_width=True):
        st.session_state.page = "admin"
        st.rerun()

st.markdown("<hr style='margin:0.3rem 0 0.6rem 0; border-color:rgba(139,58,98,0.2);'>",
            unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# PAGE: CHAT
# ══════════════════════════════════════════════════════════════════════
if st.session_state.page == "chat":

    left_col, right_col = st.columns([1, 2.4])

    with left_col:
        components.html(build_left_panel(logo_src), height=900, scrolling=True)

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
            <span class='tagline'>Always Young and Always Beautiful.</span><br><br>
            How can I help you to be a glowing beauty today?
            <div style='margin-top:0.5rem;'>
                <div style='font-size:0.75rem; color:#8B3A62; font-weight:700;
                     margin-bottom:0.3rem; text-transform:uppercase; letter-spacing:0.5px;'>
                    I speak your language:
                </div>
                <span class='lang-chip'>🇬🇧 English</span>
                <span class='lang-chip'>🇮🇳 हिन्दी</span>
                <span class='lang-chip'>🏝️ ଓଡ଼ିଆ</span>
                <div style='margin-top:0.35rem;'>
                    <span class='lang-chip' style='background:#6d1f4a;'>
                        🇬🇧+🇮🇳 English–Hindi</span>
                    <span class='lang-chip' style='background:#6d1f4a;'>
                        🇬🇧+🏝️ English–Odia</span>
                    <span class='lang-chip' style='background:#4a0d33;'>
                        🌐 All Three</span>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)



        # ── Service Explorer ───────────────────────────────────────
        with st.expander("💅 Explore Our Services & Time Required"):
            st.markdown(
                "<div style='font-size:0.82rem; color:#8B3A62; font-weight:600;"
                "margin-bottom:0.4rem;'>Tap any category to see services & duration:</div>",
                unsafe_allow_html=True
            )
            for cat, services in SERVICES_WITH_DURATION.items():
                with st.expander(f"✦ {cat}"):
                    rows = ""
                    for svc, dur in services.items():
                        dur_str = f"{dur} min" if dur < 60 else (
                            f"{dur//60}h" if dur % 60 == 0 else f"{dur//60}h {dur%60}min"
                        )
                        rows += (
                            f"<div style='display:flex; justify-content:space-between;"
                            f"padding:0.25rem 0.5rem; border-bottom:1px solid #fce4ec;"
                            f"font-size:0.82rem; align-items:center;'>"
                            f"<span style='color:#3a3a3a;'>{svc}</span>"
                            f"<span style='background:#8B3A62; color:white; border-radius:12px;"
                            f"padding:0.1rem 0.55rem; font-size:0.72rem; font-weight:600;'>"
                            f"⏱ {dur_str}</span></div>"
                        )
                    st.markdown(
                        f"<div style='border:1px solid #f8bbd0; border-radius:8px;"
                        f"overflow:hidden;'>{rows}</div>",
                        unsafe_allow_html=True
                    )

        # ── Chat ────────────────────────────────────────────────

        user_input = st.chat_input("💬 Type your message here and press Enter…")

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

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

        if st.session_state.messages:
            if st.button("🔄 Start New Conversation", use_container_width=False):
                st.session_state.messages = []
                st.session_state.lead_saved = False
                st.rerun()

# ══════════════════════════════════════════════════════════════════════
# PAGE: GALLERY
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.page == "gallery":

    st.markdown("""
    <div class='lyra-header'>
        <h1>🖼️ Our Work — Before & After Gallery</h1>
        <p>Real transformations at Forever 21 Beauty Studio</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#fce4ec; border-radius:10px; padding:0.7rem 1rem;
                margin-bottom:1rem; font-size:0.85rem; color:#880e4f; border-left:4px solid #C2185B;'>
        📸 <strong>Gallery coming soon!</strong> Bini Didi is preparing beautiful before & after photos.
        Check back soon to see real transformations from our studio.
    </div>""", unsafe_allow_html=True)

    # Filter by category
    all_cats = list(set([g["category"] for g in GALLERY_ITEMS]))
    selected_filter = st.selectbox("Filter by category", ["All"] + sorted(all_cats))

    filtered = GALLERY_ITEMS if selected_filter == "All" else \
        [g for g in GALLERY_ITEMS if g["category"] == selected_filter]

    cols = st.columns(3)
    for i, item in enumerate(filtered):
        with cols[i % 3]:
            if item["youtube"]:
                st.markdown(f"""
                <div class='gallery-card'>
                    <iframe width='100%' height='180'
                        src='{item["youtube"]}'
                        frameborder='0' allowfullscreen
                        style='display:block;'></iframe>
                    <div class='gallery-label'>{item["label"]}</div>
                    <div style='padding:0.4rem 0.7rem; font-size:0.78rem;
                                color:#555; background:white;'>
                        {item["description"]}
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='gallery-card'>
                    <div style='background:linear-gradient(135deg,#fce4ec,#f8bbd0);
                                height:160px; display:flex; align-items:center;
                                justify-content:center; flex-direction:column;'>
                        <div style='font-size:2.5rem; margin-bottom:0.3rem;'>📸</div>
                        <div style='font-size:0.78rem; color:#8B3A62; font-weight:600;'>
                            Photo Coming Soon</div>
                    </div>
                    <div class='gallery-label'>{item["label"]}</div>
                    <div style='padding:0.4rem 0.7rem; font-size:0.78rem;
                                color:#555; background:white;'>
                        {item["description"]}
                    </div>
                </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; margin-top:1.5rem; padding:1rem;
                background:#fce4ec; border-radius:12px;'>
        <div style='font-family:Playfair Display,serif; font-size:1rem;
                    color:#8B3A62; font-weight:600; margin-bottom:0.4rem;'>
            Want to see your transformation here? 🌸
        </div>
        <div style='font-size:0.85rem; color:#555;'>
            Book your appointment and let Bini Didi work her magic!
        </div>
        <a href='https://wa.me/919853115511'
           style='display:inline-block; background:#25D366; color:white;
                  border-radius:10px; padding:0.5rem 1.2rem; margin-top:0.6rem;
                  text-decoration:none; font-weight:700; font-size:0.85rem;'>
            💬 Book via WhatsApp
        </a>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# PAGE: ADMIN DASHBOARD
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.page == "admin":

    if not st.session_state.admin_logged_in:
        st.markdown("""
        <div class='lyra-header'>
            <h1>🔐 Bini's Dashboard</h1>
            <p>Forever 21 Beauty Studio — Admin Access</p>
        </div>""", unsafe_allow_html=True)

        col_a, col_b, col_c = st.columns([1, 1.2, 1])
        with col_b:
            st.markdown("<br>", unsafe_allow_html=True)
            pwd = st.text_input("Enter Password", type="password",
                                placeholder="Enter your password")
            if st.button("🔓 Login", use_container_width=True):
                if hashlib.sha256(pwd.encode()).hexdigest() == ADMIN_PASSWORD_HASH:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("Incorrect password. Please try again.")
    else:
        st.markdown("""
        <div class='lyra-header'>
            <h1>📊 Bini's Lead Dashboard</h1>
            <p>Forever 21 Beauty Studio — All Leads</p>
        </div>""", unsafe_allow_html=True)

        # Logout
        if st.button("🔒 Logout", key="logout"):
            st.session_state.admin_logged_in = False
            st.rerun()

        # Load leads
        try:
            sheet = get_sheet()
            all_data = sheet.get_all_values()

            if len(all_data) <= 1:
                st.info("No leads yet. Start chatting to capture leads!")
            else:
                headers = all_data[0] if all_data[0][0] == "Timestamp" else \
                    ["Timestamp", "Name", "Phone", "Status", "Source"]
                rows = all_data[1:] if all_data[0][0] == "Timestamp" else all_data

                # Normalise rows
                leads = []
                for r in rows:
                    while len(r) < 5:
                        r.append("")
                    leads.append({
                        "Timestamp": r[0], "Name": r[1],
                        "Phone": r[2], "Status": r[3], "Source": r[4]
                    })

                # ── Date filter ──
                st.markdown("### 📅 Filter by Date")
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    date_from = st.date_input("From", value=date(2026, 1, 1))
                with col_d2:
                    date_to = st.date_input("To", value=date.today())

                def parse_date(ts):
                    try:
                        return datetime.strptime(ts[:10], "%d-%m-%Y").date()
                    except:
                        return date(2026, 1, 1)

                filtered_leads = [
                    l for l in leads
                    if date_from <= parse_date(l["Timestamp"]) <= date_to
                ]

                # ── Metrics ──
                total = len(filtered_leads)
                new = sum(1 for l in filtered_leads if l["Status"] == "New Lead")
                called = sum(1 for l in filtered_leads if l["Status"] == "Called")
                booked = sum(1 for l in filtered_leads if l["Status"] == "Booked")
                lost = sum(1 for l in filtered_leads if l["Status"] == "Lost")

                m1, m2, m3, m4, m5 = st.columns(5)
                for col, label, val, color in [
                    (m1, "Total Leads", total, "#8B3A62"),
                    (m2, "New", new, "#1565c0"),
                    (m3, "Called", called, "#f57f17"),
                    (m4, "Booked", booked, "#2e7d32"),
                    (m5, "Lost", lost, "#c62828"),
                ]:
                    with col:
                        st.markdown(f"""
                        <div class='admin-metric' style='background:{color};'>
                            <div class='metric-value'>{val}</div>
                            <div class='metric-label'>{label}</div>
                        </div>""", unsafe_allow_html=True)

                # ── Leads table ──
                st.markdown(f"### 📋 Leads ({len(filtered_leads)} shown)")

                for i, lead in enumerate(reversed(filtered_leads)):
                    status = lead["Status"] or "New Lead"
                    status_class = {
                        "New Lead": "status-new",
                        "Called": "status-called",
                        "Booked": "status-booked",
                        "Lost": "status-lost"
                    }.get(status, "status-new")

                    with st.expander(
                        f"👤 {lead['Name']} — {lead['Phone']} | {lead['Timestamp']}"
                    ):
                        c1, c2, c3 = st.columns([2, 2, 2])
                        with c1:
                            st.markdown(f"**Name:** {lead['Name']}")
                            st.markdown(f"**Phone:** [{lead['Phone']}](tel:{lead['Phone']})")
                        with c2:
                            st.markdown(f"**Date:** {lead['Timestamp']}")
                            st.markdown(f"**Source:** {lead.get('Source','Website')}")
                        with c3:
                            st.markdown(f"**Status:** <span class='{status_class}'>{status}</span>",
                                        unsafe_allow_html=True)
                            new_status = st.selectbox(
                                "Update Status",
                                ["New Lead", "Called", "Booked", "Lost"],
                                index=["New Lead", "Called", "Booked", "Lost"].index(status)
                                if status in ["New Lead", "Called", "Booked", "Lost"] else 0,
                                key=f"status_{i}"
                            )
                            if st.button("💾 Save", key=f"save_{i}"):
                                try:
                                    all_rows = sheet.get_all_values()
                                    for row_idx, row in enumerate(all_rows):
                                        if (len(row) >= 3 and
                                            row[1] == lead["Name"] and
                                            row[2] == lead["Phone"] and
                                            row[0] == lead["Timestamp"]):
                                            sheet.update_cell(row_idx + 1, 4, new_status)
                                            st.success("✅ Status updated!")
                                            break
                                except Exception as e:
                                    st.error(f"Update failed: {e}")

                        wa_link = f"https://wa.me/91{lead['Phone'].replace(' ','').replace('+91','').replace('-','')}"
                        st.markdown(
                            f"<a href='{wa_link}' target='_blank' "
                            f"style='background:#25D366; color:white; border-radius:8px; "
                            f"padding:0.3rem 0.8rem; text-decoration:none; "
                            f"font-size:0.82rem; font-weight:600;'>"
                            f"💬 WhatsApp this customer</a>",
                            unsafe_allow_html=True
                        )

        except Exception as e:
            st.error(f"Could not load leads: {e}")
