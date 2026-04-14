# VERSION: 6.4 — Tagline pink bold everywhere
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
.festival-banner {
    background: linear-gradient(90deg, #880e4f, #c2185b, #880e4f);
    color: white; text-align: center; padding: 0.5rem 1rem;
    border-radius: 8px; font-size: 0.85rem; font-weight: 600;
    margin-bottom: 0.8rem; letter-spacing: 0.3px;
}
.lead-banner {
    background: linear-gradient(90deg, #1b5e20, #2e7d32);
    color: white; border-radius: 10px; padding: 0.6rem 1rem;
    font-size: 0.85rem; margin-top: 0.5rem; font-weight: 600;
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
</style>
""", unsafe_allow_html=True)

# ── Config ─────────────────────────────────────────────────────────────────────
FESTIVAL_BANNER = "🌸 Wedding Season Special — Book your Bridal Package now! Call Bini Didi: +91 98531 15511"
ADMIN_PASSWORD_HASH = hashlib.sha256("Bini".encode()).hexdigest()

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

GALLERY_ITEMS = [
    {"category": "Bridal Makeup", "label": "💍 Bridal Transformation",
     "youtube": "", "description": "HD Bridal Makeup — Radiant & Timeless"},
    {"category": "Facial", "label": "✨ Glow Facial",
     "youtube": "", "description": "Hydra Facial — Before & After"},
    {"category": "Hair Treatment", "label": "💇 Hair Transformation",
     "youtube": "", "description": "Keratin Treatment — Silky Smooth Results"},
    {"category": "Mehendi", "label": "🌿 Bridal Mehendi",
     "youtube": "", "description": "Intricate Bridal Mehendi Design"},
    {"category": "Nail Art", "label": "💅 Nail Art",
     "youtube": "", "description": "Custom Nail Extension & Art"},
    {"category": "Hair Colour", "label": "🎨 Hair Colour",
     "youtube": "", "description": "Balayage & Global Colour — Stunning Results"},
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
            return base64.b64encode(f.read()).decode()
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

def save_lead_to_sheet(name, phone, source="Website"):
    try:
        sheet = get_sheet()
        sheet.append_row([datetime.now().strftime("%d-%m-%Y %H:%M"),
                          name, phone, "New Lead", source])
        return True
    except Exception as e:
        st.error(f"Sheet error: {e}")
        return False

def chat_with_lyra(messages, system_prompt):
    client = get_gemini_client()
    gemini_messages = [
        types.Content(
            role="user" if m["role"] == "user" else "model",
            parts=[types.Part(text=m["content"])]
        ) for m in messages
    ]
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=system_prompt),
        contents=gemini_messages,
    )
    return response.text

def extract_lead(text):
    pattern = r'LEAD_CAPTURED:\{"name":"([^"]+)","phone":"([^"]+)"\}'
    match = re.search(pattern, text)
    if match:
        return re.sub(pattern, "", text).strip(), match.group(1), match.group(2)
    return text, None, None

def format_duration(minutes):
    if minutes < 60:
        return f"{minutes} min"
    h = minutes // 60
    m = minutes % 60
    if m == 0:
        return f"{h}h"
    return f"{h}h {m}min"

def parse_date(ts):
    try:
        return datetime.strptime(ts[:10], "%d-%m-%Y").date()
    except Exception:
        return date(2026, 1, 1)

# ── Session state ───────────────────────────────────────────────────────────────
for key, val in [("messages", []), ("lead_saved", False),
                 ("admin_logged_in", False), ("page", "chat")]:
    if key not in st.session_state:
        st.session_state[key] = val

system_prompt = load_system_prompt()
logo_b64 = load_logo()

# ══════════════════════════════════════════════════════════════════════
# TOP NAV
# ══════════════════════════════════════════════════════════════════════
if FESTIVAL_BANNER:
    st.markdown(f"<div class='festival-banner'>🎉 {FESTIVAL_BANNER}</div>",
                unsafe_allow_html=True)

n1, n2, n3, n4 = st.columns([2.2, 1, 1, 1])
with n2:
    if st.button("💬 Chat", use_container_width=True):
        st.session_state.page = "chat"; st.rerun()
with n3:
    if st.button("🖼️ Gallery", use_container_width=True):
        st.session_state.page = "gallery"; st.rerun()
with n4:
    if st.button("🔐 Dashboard", use_container_width=True):
        st.session_state.page = "admin"; st.rerun()

st.markdown("<hr style='margin:0.3rem 0 0.6rem 0; border-color:rgba(139,58,98,0.2);'>",
            unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# PAGE: CHAT
# ══════════════════════════════════════════════════════════════════════
if st.session_state.page == "chat":

    left, right = st.columns([1, 2.4])

    # ── LEFT PANEL — pure Streamlit widgets ──────────────────────────
    with left:
        # ── Logo ──
        logo_b64 = load_logo()
        if logo_b64:
            st.markdown(
                f"<div style='text-align:center; padding:0.5rem 0 0.4rem 0;'>"
                f"<div style='display:inline-block; background:white;"
                f"border-radius:12px; padding:0.6rem 0.8rem;"
                f"border:3px solid #C2185B;"
                f"box-shadow:0 3px 10px rgba(194,24,91,0.25);'>"
                f"<img src='data:image/png;base64,{logo_b64}' "
                f"style='max-width:150px; display:block;'/>"
                f"</div></div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div style='text-align:center; padding:0.3rem 0;'>"
                "<span style='font-size:1.8rem;'>💄</span><br>"
                "<strong>Forever 21</strong><br>"
                "<small>Beauty Studio</small></div>",
                unsafe_allow_html=True
            )

        st.divider()

        # ── Find Us ──
        st.markdown("<span style='color:#C2185B; font-weight:700; font-size:0.95rem;'>📍 Find Us</span>", unsafe_allow_html=True)
        st.write("Lane-3, Kalinga Vihar (K9A)")
        st.write("Bhubaneswar – 751019, Odisha")
        st.caption("Near Vivanta Hotel & D N Regalia Mall")
        st.link_button("🗺️ Open in Maps",
                       "https://maps.app.goo.gl/B7oszYnEmBxMxLVe8",
                       use_container_width=True)

        st.divider()

        # ── Contact ──
        st.markdown("<span style='color:#C2185B; font-weight:700; font-size:0.95rem;'>📞 Contact Us</span>", unsafe_allow_html=True)
        st.link_button("📱 +91 98531 15511",
                       "tel:+919853115511",
                       use_container_width=True)
        st.link_button("💬 Chat on WhatsApp",
                       "https://wa.me/919853115511?text=Namaskar%20Bini%20Didi!%20I%20would%20like%20to%20know%20more%20about%20your%20services.",
                       use_container_width=True)

        st.divider()

        # ── Working Hours ──
        st.markdown("<span style='color:#C2185B; font-weight:700; font-size:0.95rem;'>🕐 Working Hours</span>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.caption("Mon – Sat")
            st.caption("Sunday")
        with c2:
            st.caption("10 AM – 8 PM")
            st.caption("10 AM – 6 PM")
        st.caption("* Confirm timings while booking")

        st.divider()

        # ── Services ──
        st.markdown("<span style='color:#C2185B; font-weight:700; font-size:0.95rem;'>💅 Our Services</span>", unsafe_allow_html=True)
        svc_names = list(SERVICES_WITH_DURATION.keys())
        st.caption(" · ".join(svc_names[:10]))
        st.caption(" · ".join(svc_names[10:]))

        st.divider()

        # ── Social Links ──
        st.markdown("<span style='color:#C2185B; font-weight:700; font-size:0.95rem;'>🌐 Follow & Review Us</span>", unsafe_allow_html=True)
        st.link_button("📸 Instagram",
                       "https://www.instagram.com/forever_21_beauty_studio?igsh=MWwxenQ0cHI1YmlidQ==",
                       use_container_width=True)
        st.link_button("👍 Facebook",
                       "https://www.facebook.com/share/17J8yCJafA/",
                       use_container_width=True)
        st.link_button("⭐ Google Review",
                       "https://share.google/nZogQL8Y5usCwPmWy",
                       use_container_width=True)

        st.divider()
        st.markdown(
            "<div style='text-align:center; padding:0.3rem 0;'>"
            "<span style='color:#C2185B; font-weight:700; font-style:italic; font-size:0.85rem;'>"
            "✨ Always Young, Always Beautiful. ✨"
            "</span></div>",
            unsafe_allow_html=True
        )

    # ── RIGHT COLUMN ─────────────────────────────────────────────────
    with right:
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
            <span class='tagline'>Always Young and Always Beautiful.</span>
            <br><br>How can I help you to be a glowing beauty today?
            <div class='lang-row'>
                <span class='lchip'>English</span>
                <span class='lchip'>हिन्दी</span>
                <span class='lchip'>ଓଡ଼ିଆ</span>
                <span class='lchip2'>English + हिन्दी</span>
                <span class='lchip2'>English + ଓଡ଼ିଆ</span>
                <span class='lchip3'>All Three</span>
            </div>
        </div>""", unsafe_allow_html=True)

        # ── Service Explorer ──
        with st.expander("💅 Explore Our Services & Time Required"):
            cat_choice = st.selectbox(
                "Select a category",
                ["— Choose a category —"] + list(SERVICES_WITH_DURATION.keys()),
                key="svc_cat"
            )
            if cat_choice != "— Choose a category —":
                svcs = SERVICES_WITH_DURATION[cat_choice]
                rows = "".join([
                    f"<div class='svc-row'>"
                    f"<span>{svc}</span>"
                    f"<span class='svc-badge'>⏱ {format_duration(dur)}</span>"
                    f"</div>"
                    for svc, dur in svcs.items()
                ])
                st.markdown(
                    f"<div style='border:2px solid #f8bbd0; border-radius:10px;"
                    f"overflow:hidden; margin-top:0.4rem;'>{rows}</div>",
                    unsafe_allow_html=True
                )

        # Chat
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
                    if save_lead_to_sheet(lead_name, lead_phone):
                        st.session_state.lead_saved = True
                        st.markdown(
                            f"<div class='lead-banner'>✅ Thank you, {lead_name}! "
                            f"Bini Didi will call you at {lead_phone} shortly. 🌸</div>",
                            unsafe_allow_html=True
                        )
            st.session_state.messages.append(
                {"role": "assistant", "content": display_text})

        if st.session_state.messages:
            if st.button("🔄 Start New Conversation"):
                st.session_state.messages = []
                st.session_state.lead_saved = False
                st.rerun()

# ══════════════════════════════════════════════════════════════════════
# PAGE: GALLERY
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.page == "gallery":
    st.markdown("""
    <div class='lyra-header'>
        <h1>🖼️ Before & After Gallery</h1>
        <p>Real transformations at Forever 21 Beauty Studio</p>
    </div>""", unsafe_allow_html=True)

    st.info("📸 Gallery coming soon! Bini Didi is preparing beautiful before & after photos.")

    cats = ["All"] + sorted(set(g["category"] for g in GALLERY_ITEMS))
    filt = st.selectbox("Filter by category", cats)
    items = GALLERY_ITEMS if filt == "All" else \
        [g for g in GALLERY_ITEMS if g["category"] == filt]

    cols = st.columns(3)
    for i, item in enumerate(items):
        with cols[i % 3]:
            if item["youtube"]:
                st.markdown(
                    f"<iframe width='100%' height='180' src='{item['youtube']}'"
                    f" frameborder='0' allowfullscreen></iframe>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='background:linear-gradient(135deg,#fce4ec,#f8bbd0);"
                    f"height:150px; border-radius:10px; display:flex;"
                    f"align-items:center; justify-content:center; flex-direction:column;"
                    f"border:2px solid #f8bbd0;'>"
                    f"<div style='font-size:2.2rem;'>📸</div>"
                    f"<div style='font-size:0.75rem; color:#8B3A62; font-weight:600;'>"
                    f"Photo Coming Soon</div></div>",
                    unsafe_allow_html=True
                )
            st.markdown(f"**{item['label']}**")
            st.caption(item["description"])

    st.markdown("""
    <div style='text-align:center; margin-top:1.5rem; padding:1rem;
         background:#fce4ec; border-radius:12px;'>
        <div style='font-family:Playfair Display,serif; font-size:1rem;
             color:#8B3A62; font-weight:600; margin-bottom:0.4rem;'>
            Want to see your transformation here? 🌸</div>
        <a href='https://wa.me/919853115511' target='_blank'
           style='display:inline-block; background:#25D366; color:white;
           border-radius:10px; padding:0.5rem 1.2rem; margin-top:0.5rem;
           text-decoration:none; font-weight:700; font-size:0.85rem;'>
           💬 Book via WhatsApp</a>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# PAGE: ADMIN DASHBOARD
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.page == "admin":
    st.markdown("""
    <div class='lyra-header'>
        <h1>📊 Bini's Dashboard</h1>
        <p>Forever 21 Beauty Studio — Lead Management</p>
    </div>""", unsafe_allow_html=True)

    if not st.session_state.admin_logged_in:
        _, mid, _ = st.columns([1, 1.2, 1])
        with mid:
            pwd = st.text_input("Password", type="password")
            if st.button("🔓 Login", use_container_width=True):
                if hashlib.sha256(pwd.encode()).hexdigest() == ADMIN_PASSWORD_HASH:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("Incorrect password.")
    else:
        if st.button("🔒 Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()

        try:
            sheet = get_sheet()
            all_data = sheet.get_all_values()
            rows = all_data[1:] if (all_data and all_data[0][0] == "Timestamp") \
                else all_data

            leads = []
            for r in rows:
                while len(r) < 5:
                    r.append("")
                leads.append({"Timestamp": r[0], "Name": r[1],
                               "Phone": r[2], "Status": r[3], "Source": r[4]})

            st.markdown("### 📅 Filter by Date")
            d1, d2 = st.columns(2)
            with d1:
                date_from = st.date_input("From", value=date(2026, 1, 1))
            with d2:
                date_to = st.date_input("To", value=date.today())

            filtered = [l for l in leads
                        if date_from <= parse_date(l["Timestamp"]) <= date_to]

            total = len(filtered)
            new = sum(1 for l in filtered if l["Status"] == "New Lead")
            called = sum(1 for l in filtered if l["Status"] == "Called")
            booked = sum(1 for l in filtered if l["Status"] == "Booked")
            lost = sum(1 for l in filtered if l["Status"] == "Lost")

            m1, m2, m3, m4, m5 = st.columns(5)
            for col, label, val in [
                (m1, "Total", total), (m2, "New", new),
                (m3, "Called", called), (m4, "Booked", booked),
                (m5, "Lost", lost)
            ]:
                with col:
                    st.metric(label, val)

            st.markdown(f"### 📋 Leads ({len(filtered)})")
            for i, lead in enumerate(reversed(filtered)):
                status = lead["Status"] or "New Lead"
                with st.expander(
                    f"👤 {lead['Name']} — {lead['Phone']} | {lead['Timestamp']}"
                ):
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.write(f"**Name:** {lead['Name']}")
                        st.write(f"**Phone:** {lead['Phone']}")
                    with c2:
                        st.write(f"**Date:** {lead['Timestamp']}")
                        st.write(f"**Source:** {lead.get('Source','Website')}")
                    with c3:
                        st.write(f"**Status:** {status}")
                        new_status = st.selectbox(
                            "Update",
                            ["New Lead", "Called", "Booked", "Lost"],
                            index=["New Lead","Called","Booked","Lost"].index(status)
                            if status in ["New Lead","Called","Booked","Lost"] else 0,
                            key=f"st_{i}"
                        )
                        if st.button("💾 Save", key=f"sv_{i}"):
                            try:
                                all_rows = sheet.get_all_values()
                                for ri, row in enumerate(all_rows):
                                    if (len(row) >= 3 and
                                        row[1] == lead["Name"] and
                                        row[2] == lead["Phone"] and
                                        row[0] == lead["Timestamp"]):
                                        sheet.update_cell(ri + 1, 4, new_status)
                                        st.success("✅ Updated!")
                                        break
                            except Exception as e:
                                st.error(f"Error: {e}")
                    phone_clean = lead["Phone"].replace(" ","").replace("+91","").replace("-","")
                    st.markdown(
                        f"<a href='https://wa.me/91{phone_clean}' target='_blank' "
                        f"style='background:#25D366; color:white; border-radius:8px; "
                        f"padding:0.3rem 0.8rem; text-decoration:none; font-weight:600; "
                        f"font-size:0.82rem;'>💬 WhatsApp this customer</a>",
                        unsafe_allow_html=True
                    )
        except Exception as e:
            st.error(f"Could not load leads: {e}")
