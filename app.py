import base64, re, smtplib, urllib.parse
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

STORE = "Tangudu Viswanadham Grocery Store"
PHONE, WA = "9676013866", "919676013866"
EMAIL = "maneeshtangudu2007@gmail.com"
ADDRESS = "Parlakhemundi - Narasannapeta Rd, Aludu, Kummarigunta, Andhra Pradesh 532426"
HOURS = "Every day, 7:00 am – 8:30 pm"
ASSETS = Path(__file__).parent / "assets"

CATALOG = {
    "Rice & flours": ["Rice (Sona Masoori)", "Rice (Raw)", "Wheat flour (Atta)", "Maida", "Rava / Sooji", "Poha"],
    "Dals & pulses": ["Toor dal", "Moong dal", "Urad dal", "Chana dal", "Green gram", "Bengal gram", "Rajma"],
    "Oils & ghee": ["Sunflower oil", "Groundnut oil", "Palm oil", "Coconut oil", "Ghee"],
    "Spices & masala": ["Red chilli", "Turmeric", "Coriander seeds", "Cumin", "Mustard", "Tamarind", "Garam masala"],
    "Sugar, salt & tea": ["Sugar", "Jaggery", "Salt", "Tea powder", "Coffee powder"],
    "Household": ["Washing powder", "Dish wash", "Soap", "Agarbatti", "Matchbox"],
}
UNITS = ["kg", "g", "litre", "packet", "bag (25 kg)", "bag (50 kg)", "piece", "dozen"]

st.set_page_config(page_title=STORE, page_icon="🛒", layout="wide")

def b64(name):
    p = ASSETS / name
    return base64.b64encode(p.read_bytes()).decode() if p.exists() else ""

st.markdown(f"""
<style>
/* Force a light, high-contrast look on every device (also when the phone/browser is in dark mode) */
:root {{color-scheme: light}}
#MainMenu, footer {{visibility:hidden}}
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{background:#FFFFFF !important}}
.stApp, .stApp p, .stApp li, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
[data-testid="stMarkdownContainer"] *, [data-testid="stWidgetLabel"] *, [data-testid="stCaptionContainer"] * {{color:#12332B !important}}
.block-container {{max-width:1100px; padding-top:1rem}}
html {{scroll-behavior:smooth}}
.stApp input, .stApp textarea {{background:#FFFFFF !important; color:#12332B !important; -webkit-text-fill-color:#12332B !important; border:1.5px solid #8FA39B !important; border-radius:8px}}
.stApp input::placeholder, .stApp textarea::placeholder {{color:#6B7F78 !important; -webkit-text-fill-color:#6B7F78 !important}}
[data-baseweb="select"] > div {{background:#FFFFFF !important; border:1.5px solid #8FA39B !important}}
[data-baseweb="select"] *, [data-baseweb="popover"] * {{color:#12332B !important; background-color:#FFFFFF}}
[data-testid="stExpander"] {{border:1.5px solid #CFDAD2; border-radius:10px; background:#F7FAF6}}
[data-testid="stExpander"] summary * {{color:#12332B !important; font-weight:600}}
[data-testid="stFileUploaderDropzone"] {{background:#FFFFFF !important; border:2px dashed #12332B !important}}
[data-testid="stFileUploaderDropzone"] * {{color:#12332B !important}}
[data-testid="stFileUploaderDropzone"] button {{background:#FFFFFF !important; border:1.5px solid #12332B !important}}
.stApp [data-testid="stBaseButton-primary"] {{background:#C8321E !important; border:0 !important}}
.stApp [data-testid="stBaseButton-primary"] * {{color:#FFFFFF !important; font-weight:600}}
.stApp [data-testid="stBaseButton-secondary"] {{background:#FFFFFF !important; border:1.5px solid #12332B !important}}
.stApp [data-testid="stBaseButton-secondary"] * {{color:#12332B !important}}
.stApp a[data-testid^="stBaseLinkButton"] {{background:#128C4A !important; border:0 !important}}
.stApp a[data-testid^="stBaseLinkButton"] * {{color:#FFFFFF !important; font-weight:700}}
/* Extra fixes: boxes, alerts, number box and expander that Streamlit paints dark in dark mode */
[data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="textarea"] {{background:#FFFFFF !important}}
[data-testid="stNumberInput"] button {{background:#FFFFFF !important; color:#12332B !important}}
[data-testid="stExpander"] details, [data-testid="stExpander"] summary {{background:#F7FAF6 !important}}
[data-testid="stAlert"], [data-testid="stAlertContainer"] {{background:#E6F2E9 !important; border:1.5px solid #7FA58B !important; border-radius:10px}}
[data-testid="stAlert"] *, [data-testid="stAlertContainer"] * {{color:#0B2A22 !important}}
[data-testid="stFileUploaderDropzone"] small, [data-testid="stFileUploaderFile"] * {{color:#12332B !important}}
.stApp hr {{border-color:#CFDAD2}}
.st-key-typebox, .st-key-photobox {{border:2px solid #F2B705; background:#FFFBEA; border-radius:14px; padding:18px}}
.st-key-typebox *, .st-key-photobox * {{color:#12332B !important}}
.hero {{background:linear-gradient(105deg,rgba(10,45,37,.95) 35%,rgba(10,45,37,.55)),url(data:image/png;base64,{b64('hero.png')}) center/cover;
  border-radius:18px; padding:64px 44px; margin-bottom:22px}}
.stApp .hero h1 {{font-size:clamp(2rem,5vw,3.4rem); line-height:1.1; margin:0 0 14px; font-weight:800; color:#FFFFFF !important}}
.stApp .hero .tag {{font-size:1.3rem; margin:0; color:#FFFFFF !important}}
.stApp .hero .tel {{font-size:1.15rem; margin:6px 0 24px; color:#F2D675 !important}}
.btn {{display:inline-block; padding:12px 24px; border-radius:8px; font-weight:600; text-decoration:none !important; margin:0 10px 8px 0}}
.stApp .btn.p {{background:#F2B705; color:#12332B !important}} .stApp .btn.s {{border:2px solid #fff; color:#FFFFFF !important}}
.info {{display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:14px; margin-bottom:34px}}
.card {{background:#F3F6F1; border-radius:12px; padding:18px 20px; border:1px solid #CFDAD2}}
.stApp .card b {{display:block; margin-bottom:4px; color:#B02A18 !important}}
.stApp .card a {{color:#12332B; text-decoration:underline}}
.stApp h2.sec {{margin:36px 0 6px; font-size:1.9rem}}
.sub {{margin-bottom:18px}} .stApp .sub {{color:#3E5A52}}
.cats {{display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:12px}}
.cat {{border:1px solid #CFDAD2; border-left:5px solid #F2B705; border-radius:10px; padding:14px 16px; background:#FFFFFF}}
.stApp .cat small {{color:#3E5A52}}
.stApp .foot {{margin-top:46px; padding:22px 0; border-top:1px solid #CFDAD2; text-align:center; color:#3E5A52}}
@media (max-width:640px) {{.hero {{padding:40px 22px}}}}
</style>

<div class="hero">
  <h1>{STORE}</h1>
  <p class="tag">Grocery and kirana items at wholesale prices</p>
  <p class="tel">కిరాణా సరుకులు హోల్‌సేల్ ధరలకే</p>
  <a class="btn p" href="#order">Place your order</a>
  <a class="btn s" href="tel:+91{PHONE}">Call {PHONE}</a>
</div>

<div class="info">
  <div class="card"><b>Timings</b>{HOURS}</div>
  <div class="card"><b>Phone / WhatsApp</b><a href="tel:+91{PHONE}">{PHONE}</a></div>
  <div class="card"><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></div>
  <div class="card"><b>Address</b>{ADDRESS}</div>
</div>

<h2 class="sec">What we stock</h2>
<div class="sub">Bulk and retail stock for kirana shops, hotels, functions and homes.</div>
<div class="cats">
  <div class="cat">Rice &amp; flours<br><small>బియ్యం, పిండి</small></div>
  <div class="cat">Dals &amp; pulses<br><small>పప్పులు</small></div>
  <div class="cat">Oils &amp; ghee<br><small>నూనెలు, నెయ్యి</small></div>
  <div class="cat">Spices &amp; masala<br><small>మసాలా దినుసులు</small></div>
  <div class="cat">Sugar, salt &amp; tea<br><small>చక్కెర, ఉప్పు, టీ</small></div>
  <div class="cat">Household<br><small>గృహోపయోగ వస్తువులు</small></div>
</div>
""", unsafe_allow_html=True)

if (ASSETS / "produce.png").exists():
    st.write("")
    st.image(str(ASSETS / "produce.png"), use_container_width=True)

# ---------------- ORDER ----------------
st.markdown('<div id="order"></div><h2 class="sec">Place your order</h2>'
            '<div class="sub">Type your list or send a photo of it. Then add your details and press the button. '
            'We will call you to confirm the price.</div>', unsafe_allow_html=True)
st.session_state.setdefault("items", [])

def send_email(subject, body, image=None):
    cfg = st.secrets.get("gmail")
    if not cfg:
        return False
    msg = EmailMessage()
    msg["Subject"], msg["From"], msg["To"] = subject, cfg["user"], EMAIL
    msg.set_content(body)
    if image is not None:
        kind, _, sub = (image.type or "image/jpeg").partition("/")
        msg.add_attachment(image.getvalue(), maintype=kind, subtype=sub or "jpeg", filename=image.name)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(cfg["user"], cfg["app_password"])
        s.send_message(msg)
    return True

left, right = st.columns(2)
with left:
    with st.container(key="typebox"):
        st.markdown("### ✍️ Type your list")
        typed = st.text_area("Write your items and quantities",
                             placeholder="Example:\nRice 25 kg\nToor dal 5 kg\nSunflower oil 5 litre",
                             height=200)
with right:
    with st.container(key="photobox"):
        st.markdown("### 📷 Send a photo of your list")
        photo = st.file_uploader("Upload a clear photo", type=["png", "jpg", "jpeg", "webp"])
        if photo:
            st.image(photo, width=220)

with st.expander("Or pick items from our list (optional)"):
    c1, c2, c3, c4 = st.columns([2, 2, 1, 1.4])
    cat = c1.selectbox("Category", list(CATALOG) + ["Other (type below)"])
    item = c2.text_input("Item name") if cat.startswith("Other") else c2.selectbox("Item", CATALOG[cat])
    qty = c3.number_input("Quantity", min_value=1, value=1, step=1)
    unit = c4.selectbox("Unit", UNITS)
    if st.button("Add to list"):
        if item.strip():
            st.session_state["items"].append((item.strip(), int(qty), unit))
        else:
            st.warning("Type the item name first.")
    for i, (n, q, u) in enumerate(st.session_state["items"]):
        a, b = st.columns([6, 1])
        a.write(f"{i+1}. {n} – {q} {u}")
        if b.button("Remove", key=f"rm{i}"):
            st.session_state["items"].pop(i)
            st.rerun()

st.markdown("### Your contact and delivery details")
d1, d2 = st.columns(2)
name = d1.text_input("Your name")
phone = d2.text_input("Mobile number", placeholder="10-digit mobile number")
address = st.text_area("Delivery address or pickup note", height=90)

if st.button("Place Order via WhatsApp", type="primary", use_container_width=True):
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]
    items = st.session_state["items"]
    if not name.strip() or not address.strip():
        st.error("Please enter your name and address.")
    elif len(digits) != 10:
        st.error("Please enter a 10-digit mobile number.")
    elif not (typed.strip() or photo or items):
        st.error("Please type your list, upload a photo of it, or pick at least one item.")
    else:
        parts = []
        if typed.strip():
            parts.append("Typed list:\n" + typed.strip())
        if items:
            parts.append("Picked items:\n" + "\n".join(f"- {n}: {q} {u}" for n, q, u in items))
        if photo:
            parts.append("Photo of list: attached (I am sending it in this chat).")
        body = (f"New order - {datetime.now():%d %b %Y, %I:%M %p}\n\nName: {name.strip()}\n"
                f"Phone: {digits}\nAddress: {address.strip()}\n\n" + "\n\n".join(parts))
        try:
            send_email(f"New order from {name.strip()} ({digits})", body, photo)
        except Exception:
            pass
        url = f"https://wa.me/{WA}?text=" + urllib.parse.quote(body)
        st.success("Your order is ready. Tap the green button to send it on WhatsApp.")
        if photo:
            st.info("After WhatsApp opens, tap the attach icon and add your photo of the list.")
        st.link_button("Open WhatsApp and send order", url, use_container_width=True)
        components.html(f"<script>window.open('{url}','_blank');</script>", height=0)
        st.session_state["items"] = []

st.markdown(f'<div class="foot">© {datetime.now().year} {STORE}<br>{ADDRESS}</div>', unsafe_allow_html=True)
