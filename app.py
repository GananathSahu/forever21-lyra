import streamlit as st
import json
import re
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
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;700&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Lato', sans-serif;
}

/* ── Hide Streamlit chrome ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ── Remove default top padding ── */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
}

/* ── HEADER BANNER ── */
.lyra-header {
    background: linear-gradient(135deg, #8B3A62 0%, #C2185B 50%, #8B3A62 100%);
    color: white;
    padding: 1.1rem 1.5rem 0.9rem 1.5rem;
    border-radius: 14px;
    margin-bottom: 1rem;
    text-align: center;
    box-shadow: 0 4px 18px rgba(139,58,98,0.35);
    position: relative;
    overflow: hidden;
}
.lyra-header::before {
    content: '';
    position: absolute;
    top: -40px; left: -40px;
    width: 180px; height: 180px;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
}
.lyra-header::after {
    content: '';
    position: absolute;
    bottom: -30px; right: -20px;
    width: 140px; height: 140px;
    border-radius: 50%;
    background: rgba(255,255,255,0.05);
}
.lyra-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem;
    font-weight: 700;
    margin: 0 0 0.15rem 0;
    letter-spacing: 0.5px;
}
.lyra-header p {
    font-size: 0.85rem;
    margin: 0;
    opacity: 0.88;
    font-weight: 300;
    letter-spacing: 0.8px;
}

/* ── WELCOME BOX ── */
.welcome-box {
    background: linear-gradient(135deg, #fff9fb 0%, #fce4ec 100%);
    border-left: 4px solid #C2185B;
    border-radius: 10px;
    padding: 0.85rem 1rem;
    margin-bottom: 0.9rem;
    font-size: 0.88rem;
    line-height: 1.65;
    color: #3a3a3a;
}
.welcome-box .welcome-title {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    font-weight: 600;
    color: #8B3A62;
    margin-bottom: 0.4rem;
}
.welcome-box .welcome-langs {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.5rem;
    flex-wrap: wrap;
}
.lang-chip {
    background: #8B3A62;
    color: white;
    border-radius: 20px;
    padding: 0.18rem 0.6rem;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.3px;
}

/* ── CHAT INPUT BOX ── */
.chat-input-wrapper {
    background: #fff;
    border: 2px solid #C2185B;
    border-radius: 12px;
    padding: 0.5rem;
    margin-bottom: 0.7rem;
    box-shadow: 0 2px 12px rgba(194,24,91,0.12);
}
.chat-input-label {
    font-size: 0.78rem;
    color: #8B3A62;
    font-weight: 700;
    margin-bottom: 0.2rem;
    padding-left: 0.2rem;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ── Make chat_input fill wrapper ── */
.stChatInput {
    border: none !important;
    box-shadow: none !important;
}
.stChatInput textarea {
    border: none !important;
    font-family: 'Lato', sans-serif !important;
    font-size: 0.93rem !important;
}

/* ── CHAT MESSAGES ── */
[data-testid="stChatMessage"] {
    border-radius: 12px;
    margin-bottom: 0.5rem;
    padding: 0.7rem 0.9rem;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2d1b2e 0%, #4a1942 100%);
    color: white;
}
[data-testid="stSidebar"] * {
    color: white !important;
}
[data-testid="stSidebar"] .sidebar-section {
    background: rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 0.7rem 0.8rem;
    margin-bottom: 0.75rem;
    border: 1px solid rgba(255,255,255,0.1);
}
[data-testid="stSidebar"] .sidebar-title {
    font-family: 'Playfair Display', serif;
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 0.4rem;
    color: #f8bbd0 !important;
    letter-spacing: 0.3px;
}
[data-testid="stSidebar"] .sidebar-item {
    font-size: 0.8rem;
    line-height: 1.7;
    opacity: 0.9;
}
[data-testid="stSidebar"] .social-link {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 0.25rem 0.7rem;
    margin: 0.2rem 0.2rem 0.2rem 0;
    font-size: 0.78rem;
    text-decoration: none;
    border: 1px solid rgba(255,255,255,0.2);
    transition: background 0.2s;
}
[data-testid="stSidebar"] .social-link:hover {
    background: rgba(255,255,255,0.22);
}
[data-testid="stSidebar"] .hours-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    padding: 0.18rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

/* ── SERVICE CHIP ── */
.service-cat {
    background: rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 0.15rem 0.55rem;
    font-size: 0.72rem;
    display: inline-block;
    margin: 0.1rem;
    border: 1px solid rgba(255,255,255,0.18);
}

/* ── SUCCESS/ERROR BANNER ── */
.lead-banner {
    background: linear-gradient(90deg, #1b5e20, #2e7d32);
    color: white;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
    margin-top: 0.5rem;
    font-weight: 600;
}

/* ── QUICK TOPIC PILLS ── */
.topic-pill {
    display: inline-block;
    background: #fce4ec;
    color: #8B3A62;
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 0.2rem;
    cursor: pointer;
    border: 1.5px solid #e8a0c0;
}
</style>
""", unsafe_allow_html=True)

# ── Load system prompt ──────────────────────────────────────────────────────────
@st.cache_data
def load_system_prompt():
    try:
        with open("system_prompt.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "You are Lyra, a helpful beauty consultant for Forever 21 Beauty Studio."

# ── Gemini client ───────────────────────────────────────────────────────────────
@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

# ── Google Sheets ───────────────────────────────────────────────────────────────
def save_lead_to_sheet(name: str, phone: str):
    try:
        sa_info = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(
            sa_info,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        gc = gspread.authorize(creds)
        sheet = gc.open_by_key(st.secrets["GOOGLE_SHEET_ID"]).worksheet("Leads")
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
        sheet.append_row([timestamp, name, phone, "New Lead"])
        return True
    except Exception as e:
        st.error(f"Sheet error: {e}")
        return False

# ── Service data ────────────────────────────────────────────────────────────────
SERVICES_JSON = """
Threading: Eyebrow (30min), Upper Lip (30min), Chin (30min), Forehead (30min), Full Face (30min).
Waxing Hydrosoluble: Half Arms (30min), Full Arms (30min), Under Arms (30min), Half Legs (30min), Full Legs (30min), Full Face (30min), Foot (15min), Full Body (90min), Back (20min), Belly (20min).
Waxing Liposoluble: Full Arms (30min), Under Arms (30min), Half Legs (30min), Full Legs (60min), Full Face (30min), Foot (15min), Full Body (90min), Back (30min), Belly (20min), Bean Wax Full Face (20min).
Bleach: Fruit (30min), Gold (30min), Oxy (30min), Back Bleach (20min).
Cleanup: Fruit (30min), Aroma (30min), Lotus (30min), Shahnaz (30min), Anti Tan Natures (30min), De Tan Jovees (30min), Papaya (30min), Acne Cleanup (30min), Natures Gold (35min), Natures Diamond (35min).
De Tan: Ozone Gio Radiance (30min), Natures Hand (30min), Raga (30min), Raaga Hand (30min), Raaga Leg (30min), Raaga Foot (20min), Natures Leg (30min), Natures Foot (20min), Raaga Back (20min), Natures Back (20min), O3+ Face (20min), Aryanveda Face (20min).
Facial: Fruit (30min), Mix Fruit (30min), Gold Natures (60min), Pearl Natures (30min), Diamond Natures (30min), Aroma Magic Skin Glow (60min), Aroma Gold (60min), Aroma Diamond (60min), Lotus Gold (60min), Lotus Fruit (30min), Panchatatva (60min), Anti Acne (30min), Anti Tan (30min), Shahnaz Gold (60min), O3+ Bridal (60min), Hydra Facial (150min), Wine Facial (60min), Ageless Vitamin C (60min), Pearl Aroma Magic (60min), Anti Aging Jovees (60min), Anti Pigment Natures (80min), Lacto Protein (80min), Biolume H2O (60min), Biolume Bridal (90min), Lavender Oatmeal (60min).
Hydra Facial: Lacto Protein (120min), Silver Aroma Magic (120min), Pearl Aroma Magic (120min), Vitamin C Aroma Magic (120min), Bridal Aroma Magic (120min), Calendula Chia Seed (120min), Lavender Orchid (120min), Kale Extract (120min), Brightening Lightening (120min), Bride Groom (120min), Dragon Fruit Matcha (120min), Pearl Organic Harvest (120min), Totally Flawless (120min), Aroma Skin Glow (90min).
Hair Cut: Straight (30min), U Cut (30min), V Cut (30min), Blunt (30min), Mushroom (30min), Feather (30min), Layer (30min), Step (30min), Kids (30min), Step with Layer (30min), Butterfly (30min), Front Hair Cut (15min).
Hair Colour: Root Touch (30min), Full Application (30min), Colour Stripping (30min), Ombre (60min), Global (60min), Balayage (60min), Henna (30min), Wash & Dry (30min), Botox Wash (30min), Root Touchup Berina (45min).
Hair Spa: Deep Conditioning (30min), XYZ (30min), Natures (30min), HairMac (30min), Berina (30min), Wella (30min), Loreal (30min), Berina Collagen (30min).
Hair Treatment: Straightening - Upto Shoulder/Below Shoulder/Upto Waist/High Volume (180min each). Smoothening - Upto Shoulder/Below Shoulder/Upto Waist/High Volume (180min each). Rebonding - Upto Shoulder/Below Shoulder/Upto Waist/High Volume (180min each). Keratin - Upto Shoulder/Below Shoulder/Upto Waist/High Volume (180min each). Botox - Upto Shoulder/Below Shoulder/Upto Waist/High Volume (180min each). Dandruff Treatment (180min).
Hair Wash: Wash & Dry Normal (15min), Wash & Dry Long (15min), Wash & Blow Dry (15min), Only Blow Dry (15min).
Hair Style: Crimping (30min), Temporary Straightening (130min), Temporary Curl (20min), Full Hair Style (60min).
Pedicure & Manicure: Pedicure (30min), Manicure (30min), Premium Pedicure (60min), Ozone Pedicure (60min), Ozone Manicure (45min).
Make-Up: Light Makeup (60min), Party Makeup (60min), Reception Makeup (60min), Bridal Makeup (60min), HD Bridal Makeup (60min), Engagement Makeup (120min).
Nail Extension: Nail Extension (60min), Nail Filling (20min), Nail Art (60min).
Mehendi: Hair Mehendi (120min), Hand Mehendi (60min).
Body: Body Massage (60min), Hair Oil Massage (39min).
Piercing: Ear Piercing (30min), Nose Piercing (30min), Ear Lobing Studex (30min).
Saree Draping: Saree Draping (30min).
"""

SERVICE_CATEGORIES = [
    "Threading", "Waxing", "Bleach", "Cleanup", "De Tan",
    "Facial", "Hydra Facial", "Hair Cut", "Hair Colour",
    "Hair Spa", "Hair Treatment", "Hair Wash", "Hair Style",
    "Pedicure & Manicure", "Make-Up", "Nail Art / Extension",
    "Mehendi", "Body Massage", "Piercing", "Saree Draping"
]

# ── Chat function ───────────────────────────────────────────────────────────────
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

# ── Lead extraction ─────────────────────────────────────────────────────────────
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

# ══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo placeholder (swap img src when logo is ready)
    st.markdown("""
    <div style='text-align:center; padding: 0.5rem 0 0.8rem 0;'>
        <div style='font-size:2.5rem;'>💄</div>
        <div style='font-family:Playfair Display,serif; font-size:1.05rem; font-weight:700; color:#f8bbd0; letter-spacing:0.5px;'>Forever 21</div>
        <div style='font-size:0.72rem; color:#e0b0c8; letter-spacing:1px; text-transform:uppercase;'>Beauty Studio</div>
    </div>
    """, unsafe_allow_html=True)

    # 📍 Location
    st.markdown("""
    <div class='sidebar-section'>
        <div class='sidebar-title'>📍 Find Us</div>
        <div class='sidebar-item'>
            MIG, Lane-3, Kalinga Vihar (K9A)<br>
            Bhubaneswar – 751019, Odisha<br>
            <span style='opacity:0.75; font-size:0.75rem;'>Near Vivanta Hotel & D N Regalia Mall</span>
        </div>
        <div style='margin-top:0.5rem;'>
            <a href='https://maps.google.com/?q=Kalinga+Vihar+K9A+Bhubaneswar' target='_blank' class='social-link'>
                🗺️ Open in Maps
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 📞 Contact
    st.markdown("""
    <div class='sidebar-section'>
        <div class='sidebar-title'>📞 Contact</div>
        <div class='sidebar-item'>
            <a href='tel:+919853115511' class='social-link'>📱 +91 98531 15511</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 🕐 Working Hours (placeholder — update when Bini confirms)
    st.markdown("""
    <div class='sidebar-section'>
        <div class='sidebar-title'>🕐 Working Hours</div>
        <div class='sidebar-item'>
            <div class='hours-row'><span>Mon – Sat</span><span style='color:#f8bbd0;'>10:00 AM – 8:00 PM</span></div>
            <div class='hours-row'><span>Sunday</span><span style='color:#f8bbd0;'>10:00 AM – 6:00 PM</span></div>
            <div style='font-size:0.7rem; opacity:0.65; margin-top:0.35rem;'>* Please confirm timings while booking</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 💅 Services Menu
    st.markdown("<div class='sidebar-section'><div class='sidebar-title'>💅 Our Services</div><div>", unsafe_allow_html=True)
    cols_per_row = 2
    for i in range(0, len(SERVICE_CATEGORIES), cols_per_row):
        row = SERVICE_CATEGORIES[i:i+cols_per_row]
        line = "".join([f"<span class='service-cat'>{s}</span>" for s in row])
        st.markdown(line, unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

    # 🌐 Social
    st.markdown("""
    <div class='sidebar-section'>
        <div class='sidebar-title'>🌐 Follow Us</div>
        <div>
            <a href='https://instagram.com/' target='_blank' class='social-link'>📸 Instagram</a>
            <a href='https://facebook.com/' target='_blank' class='social-link'>👍 Facebook</a>
        </div>
        <div style='font-size:0.7rem; opacity:0.55; margin-top:0.4rem;'>Links will be updated soon</div>
    </div>
    """, unsafe_allow_html=True)

    # Tagline
    st.markdown("""
    <div style='text-align:center; padding:0.8rem 0 0.3rem 0; font-size:0.72rem; opacity:0.5; font-style:italic; letter-spacing:0.5px;'>
        "Always Young, Always Beautiful."
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════

# Header banner
st.markdown("""
<div class='lyra-header'>
    <h1>✨ Forever 21 Beauty Studio</h1>
    <p>Powered by Lyra AI • Your Personal Beauty Consultant</p>
</div>
""", unsafe_allow_html=True)

# Welcome box
st.markdown("""
<div class='welcome-box'>
    <div class='welcome-title'>Namaskar! I'm Lyra, your Digital Host at Forever 21 Beauty Studio. 🌸</div>
    With Bini Didi, I'm here to help you remain <em>Always Young and Always Beautiful.</em><br><br>
    How can I help you to be a glowing beauty today?
    <div class='welcome-langs'>
        <span class='lang-chip'>🇬🇧 English</span>
        <span class='lang-chip'>🇮🇳 हिन्दी</span>
        <span class='lang-chip'>🏝️ ଓଡ଼ିଆ</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat input — wrapped in a visible styled box
st.markdown("<div class='chat-input-wrapper'><div class='chat-input-label'>💬 Type your message below</div>", unsafe_allow_html=True)
user_input = st.chat_input("Ask about any service, treatment or appointment…")
st.markdown("</div>", unsafe_allow_html=True)

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Process new input
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
            saved = save_lead_to_sheet(lead_name, lead_phone)
            if saved:
                st.session_state.lead_saved = True
                st.markdown(f"""
                <div class='lead-banner'>
                    ✅ Thank you, {lead_name}! Bini will call you at {lead_phone} shortly.
                </div>
                """, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": display_text})

# Clear button
if st.session_state.messages:
    if st.button("🔄 Start New Conversation", use_container_width=False):
        st.session_state.messages = []
        st.session_state.lead_saved = False
        st.rerun()
