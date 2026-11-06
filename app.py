import base64, smtplib, urllib.parse
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
import streamlit as st

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

st.set_page_config(page_title=f"{STORE}", page_icon="🛒", layout="wide")

def b64(name):
    p = ASSETS / name
    return base64.b64encode(p.read_bytes()).decode() if p.exists() else ""

st.markdown(f"""
<style>
#MainMenu, footer, header [data-testid="stToolbar"] {{visibility:hidden}}
.block-container {{max-width:1100px; padding-top:1rem}}
html {{scroll-behavior:smooth}}
.hero {{background:linear-gradient(105deg,rgba(10,45,37,.94) 35%,rgba(10,45,37,.55)),url(data:image/png;base64,{b64('hero.png')}) center/cover;
  border-radius:18px; padding:64px 44px; color:#fff; margin-bottom:22px}}
.hero h1 {{font-size:clamp(2rem,5vw,3.4rem); line-height:1.1; margin:0 0 14px; color:#fff; font-weight:800}}
.hero .tag {{font-size:1.3rem; margin:0}} .hero .tel {{font-size:1.15rem; margin:6px 0 24px; color:#F2D675}}
.btn {{display:inline-block; padding:12px 24px; border-radius:8px; font-weight:600; text-decoration:none!important; margin:0 10px 8px 0}}
.btn.p {{background:#F2B705; color:#12332B!important}} .btn.s {{border:2px solid #fff; color:#fff!important}}
.info {{display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:14px; margin-bottom:34px}}
.card {{background:#F3F6F1; border-radius:12px; padding:18px 20px; border:1px solid #DCE5DD}}
.card b {{display:block; margin-bottom:4px; color:#C8321E}} .card a {{color:#12332B}}
h2.sec {{margin:36px 0 6px; font-size:1.9rem; color:#12332B}}
.sub {{color:#4F6B64; margin-bottom:18px}}
.cats {{display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:12px}}
.cat {{border:1px solid #DCE5DD; border-left:5px solid #F2B705; border-radius:10px; padding:14px 16px; background:#fff}}
.cat small {{color:#4F6B64}}
.foot {{margin-top:46px; padding:22px 0; border-top:1px solid #DCE5DD; color:#4F6B64; text-align:center}}
@media (max-width:640px) {{.hero {{padding:40px 22px}}}}
</style>

<div class="hero">
  <h1>{STORE}</h1>
  <p class="tag">Grocery and kirana items at wholesale prices</p>
  <p class="tel">కిరాణా సరుకులు హోల్‌సేల్ ధరలకే</p>
  <a class="btn p" href="#order">Build your order</a>
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
st.markdown('<div id="order"></div><h2 class="sec">Build your order</h2>'
            '<div class="sub">Add items one by one, or send a photo of your handwritten list. We will call you to confirm the price.</div>',
            unsafe_allow_html=True)

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

tab_build, tab_photo = st.tabs(["Type your list", "Send a photo of your list"])

with tab_build:
    c1, c2, c3, c4 = st.columns([2, 2, 1, 1.4])
    cat = c1.selectbox("Category", list(CATALOG) + ["Other (type below)"])
    if cat.startswith("Other"):
        item = c2.text_input("Item name")
    else:
        item = c2.selectbox("Item", CATALOG[cat])
    qty = c3.number_input("Quantity", min_value=1, value=1, step=1)
    unit = c4.selectbox("Unit", UNITS)
    if st.button("Add to list", type="primary"):
        if item.strip():
            st.session_state["items"].append((item.strip(), int(qty), unit))
        else:
            st.warning("Type the item name first.")
    if st.session_state["items"]:
        st.markdown("**Your list**")
        for i, (n, q, u) in enumerate(st.session_state["items"]):
            a, b = st.columns([6, 1])
            a.write(f"{i+1}. {n} – {q} {u}")
            if b.button("Remove", key=f"rm{i}"):
                st.session_state["items"].pop(i)
                st.rerun()
    else:
        st.info("Your list is empty. Add your first item above.")

with tab_photo:
    photo = st.file_uploader("Upload a clear photo of your list", type=["png", "jpg", "jpeg", "webp"])
    if photo:
        st.image(photo, width=320)
    note = st.text_area("Anything else we should know? (optional)", height=80)

st.markdown("### Your contact and delivery details")
d1, d2 = st.columns(2)
name = d1.text_input("Your name")
phone = d2.text_input("Mobile number", max_chars=15)
address = st.text_area("Delivery address / pickup note", height=90)

if st.button("Place order", type="primary", use_container_width=True):
    items, ok = st.session_state["items"], True
    if not name.strip() or len(phone.strip()) < 10 or not address.strip():
        st.error("Please fill your name, a 10-digit mobile number and your address.")
        ok = False
    elif not items and not photo:
        st.error("Add at least one item, or upload a photo of your list.")
        ok = False
    if ok:
        lines = "\n".join(f"- {n}: {q} {u}" for n, q, u in items) or "(see attached photo)"
        extra = f"\nNote: {note.strip()}" if note.strip() else ""
        body = (f"New order - {datetime.now():%d %b %Y, %I:%M %p}\n\nName: {name}\nPhone: {phone}\n"
                f"Address: {address}\n\nItems:\n{lines}{extra}")
        sent = False
        try:
            sent = send_email(f"New order from {name} ({phone})", body, photo)
        except Exception:
            sent = False
        if sent:
            st.success("Order sent. We will call you shortly to confirm.")
            st.session_state["items"] = []
        else:
            st.warning("We could not send this automatically. Please tap the button below to send it on WhatsApp.")
        wa_text = urllib.parse.quote(body + ("\n\n(Photo of list: I will attach it in this chat.)" if photo else ""))
        st.link_button("Send on WhatsApp", f"https://wa.me/{WA}?text={wa_text}")

st.markdown(f'<div class="foot">© {datetime.now().year} {STORE}<br>{ADDRESS}</div>', unsafe_allow_html=True)
