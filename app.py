# VERSION: 8.7 — Phone validation, bold Hindi tagline, Odia confirmations, 4 new services, tagline in nav

import streamlit as st
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

# ── Minimal CSS — only for elements Streamlit renders directly ─────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=Lato:wght@300;400;700&display=swap');

html, body, [class*="css"] { font-family: 'Lato', sans-serif; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container { padding-top: 0.5rem !important; }

.lyra-header {
    background: linear-gradient(135deg, #8B3A62 0%, #C2185B 50%, #8B3A62 100%);
    color: white; padding: 1rem 1.5rem; border-radius: 14px;
    margin-bottom: 0.8rem; text-align: center;
    box-shadow: 0 4px 18px rgba(139,58,98,0.35);
}
.lyra-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem; font-weight: 700; margin: 0 0 0.1rem 0;
}
.lyra-header p { font-size: 0.82rem; margin: 0; opacity: 0.88; }

.lyra-tagline {
    font-family: 'Playfair Display', serif;
    font-style: italic; font-weight: 700;
    color: #C2185B; letter-spacing: 0.3px;
    font-size: 0.9rem; text-align: center;
    margin: 0.2rem 0 0.8rem 0;
    text-shadow: 0 1px 2px rgba(194,24,91,0.15);
}

.welcome-box {
    background: linear-gradient(135deg, #fff9fb 0%, #fce4ec 100%);
    border-left: 4px solid #C2185B; border-radius: 10px;
    padding: 0.85rem 1rem; margin-bottom: 0.8rem;
    font-size: 0.88rem; line-height: 1.7; color: #3a3a3a;
}
.welcome-title {
    font-family: 'Playfair Display', serif;
    font-size: 1rem; font-weight: 700; color: #8B3A62; margin-bottom: 0.35rem;
}
.tagline {
    font-family: 'Playfair Display', serif;
    font-style: italic; font-weight: 700;
    color: #C2185B; letter-spacing: 0.3px;
    font-size: 1rem;
    text-shadow: 0 1px 2px rgba(194,24,91,0.15);
}
.lang-row { display:flex; flex-wrap:wrap; gap:0.4rem; margin-top:0.5rem; }
.lchip {
    background: #8B3A62; color: white; border-radius: 20px;
    padding: 0.18rem 0.65rem; font-size: 0.74rem; font-weight: 600;
    display: inline-block;
}
.lchip2 {
    background: #6d1f4a; color: white; border-radius: 20px;
    padding: 0.18rem 0.65rem; font-size: 0.74rem; font-weight: 600;
    display: inline-block;
}
.lchip3 {
    background: #4a0d33; color: white; border-radius: 20px;
    padding: 0.18rem 0.65rem; font-size: 0.74rem; font-weight: 600;
    display: inline-block;
}
@keyframes flashBanner {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}
.festival-banner {
    background: linear-gradient(90deg, #880e4f, #c2185b, #880e4f);
    color: white; text-align: center; padding: 0.6rem 1rem;
    border-radius: 8px; font-size: 1.05rem; font-weight: 700;
    margin-bottom: 0.8rem; letter-spacing: 0.4px;
    animation: flashBanner 1.5s ease-in-out infinite;
}
.lead-banner {
    background: linear-gradient(90deg, #1b5e20, #2e7d32);
    color: white; border-radius: 10px; padding: 0.6rem 1rem;
    font-size: 0.85rem; margin-top: 0.5rem; font-weight: 600;
}
/* Compress all left panel spacing globally */
[data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] .stButton,
[data-testid="stSidebar"] .stSelectbox, [data-testid="stSidebar"] .stLinkButton {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}
[data-testid="stSidebar"] p {
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.3 !important;
}
/* Compress main page left column too */
section[data-testid="column"]:first-child .stMarkdown p {
    margin: 0 !important;
    line-height: 1.4 !important;
}
section[data-testid="column"]:first-child .element-container {
    margin-bottom: 0 !important;
    margin-top: 0 !important;
}
section[data-testid="column"]:first-child .stMarkdown {
    min-height: 0 !important;
}
section[data-testid="column"]:first-child div[data-testid="stVerticalBlock"] > div {
    gap: 0 !important;
}
section[data-testid="column"]:first-child .stButton {
    margin: 0.1rem 0 !important;
}
section[data-testid="column"]:first-child .stSelectbox {
    margin: 0.1rem 0 !important;
}
section[data-testid="column"]:first-child .stLinkButton {
    margin: 0.1rem 0 !important;
}
.stChatInput > div {
    border: 2.5px solid #C2185B !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 12px rgba(194,24,91,0.15) !important;
}
/* ── Make service expander prominent ── */
[data-testid="stExpander"] {
    border: 2px solid #C2185B !important;
    border-radius: 12px !important;
    background: linear-gradient(135deg, #fff9fb, #fce4ec) !important;
    margin-bottom: 0.8rem !important;
}
[data-testid="stExpander"] summary {
    font-weight: 700 !important;
    color: #8B3A62 !important;
    font-size: 0.95rem !important;
}
.svc-row {
    display:flex; justify-content:space-between; align-items:center;
    padding: 0.3rem 0.7rem; border-bottom: 1px solid #fce4ec;
    font-size: 0.83rem; background: white;
}
.svc-badge {
    background: #8B3A62; color: white; border-radius: 12px;
    padding: 0.1rem 0.6rem; font-size: 0.72rem; font-weight: 600;
    white-space: nowrap;
}
/* ── NAV BUTTON STYLING ── */
div[data-testid="stButton"] button[kind="secondary"] {
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    border-radius: 10px !important;
    border: 2px solid #C2185B !important;
    color: #8B3A62 !important;
    background: white !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] button[kind="secondary"]:hover {
    background: #fce4ec !important;
}
</style>
""", unsafe_allow_html=True)

# ── Config ─────────────────────────────────────────────────────────────────────
FESTIVAL_BANNER = "👰✨ Hey Brides-to-Be! Jan–Apr slots are filling fast — very few left! Book your Bridal Package now! 💍🌸"
ADMIN_PASSWORD_HASH = hashlib.sha256("Bini".encode()).hexdigest()

# ── Phone validation ───────────────────────────────────────────────────────────
def is_valid_indian_mobile(phone: str) -> bool:
    """Validate Indian mobile number: 10 digits, starts with 6/7/8/9."""
    phone = phone.strip()
    # Remove +91 or 91 prefix if present
    if phone.startswith("+91"):
        phone = phone[3:].strip()
    elif phone.startswith("91") and len(phone) == 12:
        phone = phone[2:]
    # Remove spaces and dashes
    phone = re.sub(r"[\s\-]", "", phone)
    # Must be exactly 10 digits starting with 6, 7, 8, or 9
    return bool(re.match(r"^[6-9]\d{9}$", phone))

# ── Service data ───────────────────────────────────────────────────────────────
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
        "Face": 30, "Hand": 30, "Leg": 30, "Foot": 20, "Back": 20
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
        "Pedicure Standard": 30, "Pedicure Premium / Ozone": 60,
        "Manicure Standard": 30, "Manicure Ozone": 45
    },
    "Make-Up": {
        "Light / Party": 60, "Reception / Bridal": 60,
        "HD Bridal": 60, "Engagement": 120
    },
    "Nail & Extensions": {
        "Nail Extension / Nail Art": 60, "Nail Filling": 20
    },
    "Mehendi": {
        "Hand Mehendi": 60, "Hair Mehendi": 120
    },
    "Massage & Body Care": {
        "Body Massage": 60, "Hair Oil Massage": 40
    },
    "Piercing": {
        "Ear Piercing": 30, "Nose Piercing": 30, "Ear Lobing": 30
    },
    "Eye & Lash": {
        "Eyelash Extension": 60
    },
    "Skin & Advanced": {
        "Mole Removal": 30, "Earlobe Repair": 45
    },
    "Saree Draping": {
        "Saree Draping": 30
    }
}

GALLERY_ITEMS = [
    {"category": "Bridal Makeup", "label": "💍 Bridal Transformation",
     "image_key": "bridal", "description": "HD Bridal Makeup — Radiant & Timeless"},
    {"category": "Hydra Facial", "label": "✨ Hydra Facial",
     "image_key": "hydrafacial", "description": "Hydra Facial — Deep Hydration & Glow"},
    {"category": "Hair Treatment", "label": "💇 Hair Transformation",
     "image_key": "hair", "description": "Hair Treatment — Beautiful Styles"},
    {"category": "Eyelash", "label": "👁️ Eyelash Extensions",
     "image_key": "eyelash", "description": "Eyelash Extensions — Before & After"},
    {"category": "Nail Art", "label": "💅 Nail Art & Extensions",
     "image_key": "nails", "description": "Nail Art & Extensions — Stunning Results"},
    {"category": "Hair Colour", "label": "🎨 Hair Colour",
     "image_key": "hair_color", "description": "Balayage & Global Colour — Stunning Results"},
]

# ── Load logo ──────────────────────────────────────────────────────────────────
def get_logo_base64(filename="f21_logo_new.png"):
    try:
        with open(filename, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

# ── Google Sheets ──────────────────────────────────────────────────────────────
def get_sheet():
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        sa_info = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(sa_info, scopes=scope)
        client = gspread.authorize(creds)
        sheet_id = st.secrets["GOOGLE_SHEET_ID"]
        return client.open_by_key(sheet_id).worksheet("Leads")
    except Exception as e:
        st.error(f"Sheet error: {e}")
        return None

def save_lead(name: str, phone: str):
    try:
        sheet = get_sheet()
        if sheet:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row([timestamp, name, phone, "New Lead", "Lyra Chatbot"])
            return True
    except Exception as e:
        st.error(f"Lead save error: {e}")
    return False

# ── Gemini client ──────────────────────────────────────────────────────────────
@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

def load_system_prompt():
    try:
        with open("system_prompt.txt", "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return "You are Lyra, an AI beauty consultant for Forever 21 Beauty Studio, Bhubaneswar."

# ── Session state ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "lead_captured" not in st.session_state:
    st.session_state.lead_captured = False
if "lead_name" not in st.session_state:
    st.session_state.lead_name = ""
if "lead_phone" not in st.session_state:
    st.session_state.lead_phone = ""
if "page" not in st.session_state:
    st.session_state.page = "chat"
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ── Layout: two columns ────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 2.2])

# ══════════════════════════════════════════════════════════════════════════════
# LEFT COLUMN
# ══════════════════════════════════════════════════════════════════════════════
with col_left:
    # Logo
    logo_b64 = get_logo_base64("f21_logo_new.png")
    if logo_b64:
        st.markdown(
            f'<div style="text-align:center;margin-bottom:0.3rem;">'
            f'<img src="data:image/png;base64,{logo_b64}" style="max-width:140px;border-radius:12px;"/>'
            f'</div>',
            unsafe_allow_html=True
        )

    # Studio name + tagline in nav area
    st.markdown(
        '<div style="text-align:center;margin-bottom:0.2rem;">'
        '<span style="font-family:\'Playfair Display\',serif;font-size:1.05rem;'
        'font-weight:700;color:#8B3A62;">Forever 21 Beauty Studio</span>'
        '</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="lyra-tagline">✨ Always Young, Always Beautiful. ✨</div>',
        unsafe_allow_html=True
    )

    st.divider()

    # Nav buttons
    if st.button("💬 Chat with Lyra", use_container_width=True):
        st.session_state.page = "chat"
    if st.button("🔍 Service Explorer", use_container_width=True):
        st.session_state.page = "services"
    if st.button("🖼️ Gallery", use_container_width=True):
        st.session_state.page = "gallery"
    if st.button("⏱️ Duration Planner", use_container_width=True):
        st.session_state.page = "planner"
    if st.button("🔒 Admin", use_container_width=True):
        st.session_state.page = "admin"

    st.divider()

    # Studio info
    st.markdown("**📍 Location**")
    st.markdown("Lane-3, Kalinga Vihar (K9A)")
    st.markdown("Bhubaneswar – 751019")
    st.markdown("Near **Vivanta Hotel** & D N Regalia Mall")
    st.markdown("**📞 +91 98531 15511**")
    st.markdown("**⏰ Every Day: 9 AM – 9 PM**")

    st.divider()

    # Social links
    st.markdown("**🌐 Follow Us**")
    st.link_button("📸 Instagram", "https://www.instagram.com/forever_21_beauty_studio?igsh=MWwxenQ0cHI1YmlidQ==", use_container_width=True)
    st.link_button("👍 Facebook", "https://www.facebook.com/share/17J8yCJafA/", use_container_width=True)
    st.link_button("⭐ Google Reviews", "https://share.google/nZogQL8Y5usCwPmWy", use_container_width=True)
    st.link_button("🗺️ Get Directions", "https://maps.app.goo.gl/B7oszYnEmBxMxLVe8", use_container_width=True)
    st.link_button("💬 WhatsApp", "https://wa.me/919853115511", use_container_width=True)

    st.divider()
    st.markdown(
        '<p style="font-size:0.7rem;color:#aaa;text-align:center;">'
        'Powered by Lyra AI · Forever 21 Beauty Studio<br>'
        'AI responses are for guidance only.</p>',
        unsafe_allow_html=True
    )

# ══════════════════════════════════════════════════════════════════════════════
# RIGHT COLUMN
# ══════════════════════════════════════════════════════════════════════════════
with col_right:

    # ── PAGE: CHAT ─────────────────────────────────────────────────────────────
    if st.session_state.page == "chat":
        # Header
        st.markdown("""
        <div class="lyra-header">
            <h1>💄 Lyra — Your Beauty Consultant</h1>
            <p>Forever 21 Beauty Studio · Bhubaneswar · Ask me anything about beauty!</p>
        </div>
        """, unsafe_allow_html=True)

        # Festival banner
        st.markdown(f'<div class="festival-banner">{FESTIVAL_BANNER}</div>', unsafe_allow_html=True)

        # Welcome box
        st.markdown("""
        <div class="welcome-box">
            <div class="welcome-title">🌸 Welcome to Forever 21 Beauty Studio!</div>
            I'm <b>Lyra</b>, your digital beauty consultant. I can help you with:<br>
            • Services & durations &nbsp;|&nbsp; • Bridal packages<br>
            • Skin & hair advice &nbsp;|&nbsp; • Booking via Bini Didi<br>
            <div class="lang-row">
                <span class="lchip">🇮🇳 English</span>
                <span class="lchip2">🇮🇳 हिंदी</span>
                <span class="lchip3">🇮🇳 ଓଡ଼ିଆ</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Lead captured banner
        if st.session_state.lead_captured:
            st.markdown(
                f'<div class="lead-banner">✅ Lead captured — {st.session_state.lead_name} '
                f'({st.session_state.lead_phone}) — Bini will call shortly!</div>',
                unsafe_allow_html=True
            )

        # Chat history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat input
        if prompt := st.chat_input("Ask Lyra about services, booking, or beauty tips... 💬"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Build Gemini conversation
            system_prompt = load_system_prompt()
            client = get_gemini_client()

            history = []
            for m in st.session_state.messages[:-1]:
                role = "user" if m["role"] == "user" else "model"
                history.append(types.Content(role=role, parts=[types.Part(text=m["content"])]))

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=0.7,
                        max_output_tokens=1024,
                    ),
                    contents=history + [
                        types.Content(role="user", parts=[types.Part(text=prompt)])
                    ],
                )
                raw_reply = response.text or ""
            except Exception as e:
                raw_reply = f"Sorry, I'm having a connection issue. Please try again! 🌸 (Error: {e})"

            # ── Parse LEAD_CAPTURED tag ────────────────────────────────────────
            lead_match = re.search(
                r'LEAD_CAPTURED:\{"name":"([^"]+)","phone":"([^"]+)"\}',
                raw_reply
            )
            display_reply = re.sub(
                r'\nLEAD_CAPTURED:\{[^}]+\}', '', raw_reply
            ).strip()

            if lead_match and not st.session_state.lead_captured:
                captured_name = lead_match.group(1)
                captured_phone = lead_match.group(2)

                # ── PHONE VALIDATION ──────────────────────────────────────────
                if is_valid_indian_mobile(captured_phone):
                    # Valid phone — save lead
                    st.session_state.lead_captured = True
                    st.session_state.lead_name = captured_name
                    st.session_state.lead_phone = captured_phone
                    save_lead(captured_name, captured_phone)
                else:
                    # Invalid phone — do NOT save, strip tag from display
                    display_reply = display_reply  # tag already stripped above
                    # Append a gentle correction note if not already in reply
                    if "valid" not in display_reply.lower() and "10" not in display_reply:
                        display_reply += "\n\n⚠️ Please share a valid 10-digit Indian mobile number so Bini Didi can call you. 😊"

            st.session_state.messages.append({"role": "assistant", "content": display_reply})
            with st.chat_message("assistant"):
                st.markdown(display_reply)

            if st.session_state.lead_captured:
                st.rerun()

    # ── PAGE: SERVICES ─────────────────────────────────────────────────────────
    elif st.session_state.page == "services":
        st.markdown("""
        <div class="lyra-header">
            <h1>🔍 Service Explorer</h1>
            <p>Browse all 106 services — 20 categories</p>
        </div>
        """, unsafe_allow_html=True)

        search_term = st.text_input("🔎 Search services...", placeholder="e.g. facial, waxing, bridal")

        for category, services in SERVICES_WITH_DURATION.items():
            # Filter by search
            if search_term:
                filtered = {
                    k: v for k, v in services.items()
                    if search_term.lower() in k.lower() or search_term.lower() in category.lower()
                }
            else:
                filtered = services

            if not filtered:
                continue

            with st.expander(f"✨ {category} ({len(filtered)} services)"):
                rows_html = ""
                for svc, dur in filtered.items():
                    if isinstance(dur, int):
                        badge = f"{dur} min"
                    else:
                        badge = str(dur)
                    rows_html += (
                        f'<div class="svc-row">'
                        f'<span>{svc}</span>'
                        f'<span class="svc-badge">⏱ {badge}</span>'
                        f'</div>'
                    )
                st.markdown(rows_html, unsafe_allow_html=True)

        st.markdown(
            '<p style="font-size:0.78rem;color:#999;margin-top:1rem;">'
            '💬 Prices not shown — Bini Didi calls to offer the best personalised rate.</p>',
            unsafe_allow_html=True
        )

    # ── PAGE: GALLERY ──────────────────────────────────────────────────────────
    elif st.session_state.page == "gallery":
        st.markdown("""
        <div class="lyra-header">
            <h1>🖼️ Our Gallery</h1>
            <p>Real transformations at Forever 21 Beauty Studio</p>
        </div>
        """, unsafe_allow_html=True)

        st.info("📸 Gallery photos coming soon! Ask Lyra about any service in the Chat tab. 🌸")

        for item in GALLERY_ITEMS:
            st.markdown(f"**{item['label']}** — {item['description']}")

    # ── PAGE: DURATION PLANNER ─────────────────────────────────────────────────
    elif st.session_state.page == "planner":
        st.markdown("""
        <div class="lyra-header">
            <h1>⏱️ Duration Planner</h1>
            <p>Plan your visit — select services to estimate total time</p>
        </div>
        """, unsafe_allow_html=True)

        total_minutes = 0
        selected_services = []

        for category, services in SERVICES_WITH_DURATION.items():
            with st.expander(f"📋 {category}"):
                for svc, dur in services.items():
                    if isinstance(dur, int):
                        if st.checkbox(f"{svc} ({dur} min)", key=f"plan_{category}_{svc}"):
                            total_minutes += dur
                            selected_services.append(f"{svc} ({dur} min)")

        if selected_services:
            hours = total_minutes // 60
            mins = total_minutes % 60
            duration_str = f"{hours}h {mins}m" if hours > 0 else f"{mins} min"
            st.success(f"⏱️ **Estimated total time: {duration_str}**")
            st.markdown("**Selected services:**")
            for s in selected_services:
                st.markdown(f"• {s}")
            st.markdown(
                f'<div class="lead-banner">📞 Book now — call +91 98531 15511 '
                f'or chat with Lyra to schedule your {duration_str} session!</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown("👆 Select services above to calculate your visit duration.")

    # ── PAGE: ADMIN ────────────────────────────────────────────────────────────
    elif st.session_state.page == "admin":
        st.markdown("""
        <div class="lyra-header">
            <h1>🔒 Admin Dashboard</h1>
            <p>Forever 21 Beauty Studio — Lead Management</p>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.admin_logged_in:
            pwd = st.text_input("Enter admin password:", type="password")
            if st.button("Login"):
                if hashlib.sha256(pwd.encode()).hexdigest() == ADMIN_PASSWORD_HASH:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("Incorrect password.")
        else:
            st.success("✅ Logged in as Bini Didi")
            if st.button("Logout"):
                st.session_state.admin_logged_in = False
                st.rerun()

            try:
                sheet = get_sheet()
                if sheet:
                    data = sheet.get_all_records()
                    if data:
                        st.markdown(f"**Total Leads: {len(data)}**")
                        import pandas as pd
                        df = pd.DataFrame(data)
                        st.dataframe(df, use_container_width=True)

                        # Stats
                        if "Status" in df.columns:
                            status_counts = df["Status"].value_counts()
                            col1, col2, col3, col4 = st.columns(4)
                            col1.metric("New Leads", status_counts.get("New Lead", 0))
                            col2.metric("Called", status_counts.get("Called", 0))
                            col3.metric("Booked", status_counts.get("Booked", 0))
                            col4.metric("Lost", status_counts.get("Lost", 0))
                    else:
                        st.info("No leads yet. Start chatting to capture leads!")
            except Exception as e:
                st.error(f"Error loading leads: {e}")

# ── Legal disclaimer ───────────────────────────────────────────────────────────
st.markdown(
    '<p style="font-size:0.65rem;color:#ccc;text-align:center;margin-top:1rem;">'
    'Lyra AI provides general beauty guidance only. For medical skin/hair conditions, '
    'please consult a qualified dermatologist. © 2026 Forever 21 Beauty Studio.</p>',
    unsafe_allow_html=True
)
