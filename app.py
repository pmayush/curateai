import streamlit as st
import os
import base64
import json

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CurateAI · Shopping Concierge",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# STYLES  (Instagram-DM dark theme)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
[data-testid="stAppViewContainer"] { background: #0d0d0d; }
[data-testid="stHeader"]           { background: transparent; }
[data-testid="stSidebar"]          { background: #111; border-right: 1px solid #222; }
[data-testid="stChatInput"]        { background: #1a1a1a !important; }

/* Chat bubbles */
[data-testid="stChatMessage"] { background: transparent !important; }
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p { font-size: 14px; line-height: 1.6; }

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Custom components */
.header-bar {
    background: #111;
    border-bottom: 1px solid #222;
    padding: 14px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
    border-radius: 12px;
}
.avatar { width: 38px; height: 38px; border-radius: 50%; background: linear-gradient(135deg, #f093fb, #f5576c); display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }
.header-text h4 { margin: 0; font-size: 15px; color: #f0f0f0; font-weight: 600; }
.header-text p  { margin: 0; font-size: 12px; color: #888; }
.online-dot { width: 8px; height: 8px; background: #22c55e; border-radius: 50%; display: inline-block; margin-left: 6px; }

.product-grid { display: flex; flex-wrap: wrap; gap: 10px; margin: 10px 0; }
.product-card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 14px;
    padding: 12px;
    width: 145px;
    text-align: center;
    transition: border-color 0.2s;
}
.product-card:hover { border-color: #f093fb; }
.product-card img { width: 100%; height: 140px; object-fit: cover; border-radius: 8px; margin-bottom: 8px; }
.product-name { font-size: 12px; font-weight: 600; color: #eee; margin: 0 0 2px; line-height: 1.3; }
.product-brand { font-size: 11px; color: #888; margin: 0 0 6px; }
.product-price { font-size: 13px; font-weight: 700; color: #f093fb; }
.product-og    { font-size: 11px; color: #555; text-decoration: line-through; }
.badge-discount { background: #f093fb22; color: #f093fb; font-size: 10px; padding: 2px 6px; border-radius: 20px; display: inline-block; margin-top: 4px; }

.price-table { background: #1a1a1a; border-radius: 12px; padding: 14px; margin: 8px 0; border: 1px solid #2a2a2a; }
.price-row { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid #222; font-size: 13px; }
.price-row:last-child { border-bottom: none; }
.price-best { color: #22c55e; font-weight: 700; }
.coupon-pill { background: #22c55e22; color: #22c55e; font-size: 11px; padding: 2px 8px; border-radius: 20px; display: inline-block; }

.loyalty-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border: 1px solid #0f3460;
    border-radius: 16px;
    padding: 18px;
    margin: 8px 0;
}
.loyalty-title { font-size: 13px; color: #888; margin: 0 0 6px; }
.loyalty-amount { font-size: 28px; font-weight: 700; color: #f0a500; margin: 0 0 4px; }
.loyalty-tier { background: #f0a50022; color: #f0a500; font-size: 12px; padding: 3px 10px; border-radius: 20px; display: inline-block; }

.checkout-card {
    background: #0d0d0d;
    border: 1px solid #2a2a2a;
    border-radius: 18px;
    padding: 20px;
    margin: 8px 0;
    position: relative;
    overflow: hidden;
}
.checkout-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #f093fb, #f5576c, #f0a500);
}
.checkout-row { display: flex; justify-content: space-between; padding: 5px 0; font-size: 13px; color: #bbb; }
.checkout-row strong { color: #eee; }
.checkout-total { font-size: 22px; font-weight: 700; color: #22c55e; }
.checkout-btn {
    display: block;
    background: linear-gradient(90deg, #f093fb, #f5576c);
    color: white !important;
    text-align: center;
    padding: 14px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 15px;
    text-decoration: none !important;
    margin-top: 14px;
    letter-spacing: 0.3px;
}

.profile-card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 14px;
    padding: 16px;
    margin: 8px 0;
    display: flex;
    align-items: center;
    gap: 14px;
}
.profile-avatar { font-size: 32px; }
.profile-name { font-size: 15px; font-weight: 600; color: #eee; margin: 0 0 2px; }
.profile-meta { font-size: 12px; color: #888; margin: 0; }
.gold-badge { background: linear-gradient(135deg, #f0a500, #ff6b00); color: #000; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 20px; display: inline-block; margin-left: 6px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MOCK DATA
# ─────────────────────────────────────────────────────────────────────────────
SHOPPER = {
    "name": "Priya Sharma",
    "social_handle": "@priya.styles",
    "phone_masked": "+91 ••••• 99999",
    "loyalty_tier": "Gold",
    "reward_balance": 840,
    "last_order_days": 12,
    "top_category": "Ethnic Wear",
    "rto_count": 1,
    "saved_address": "12 Marine Drive, Mumbai 400001",
    "past_brands": ["Libas", "Biba", "W for Woman"],
}

CATALOG = [
    {
        "id": "P001",
        "name": "Floral Anarkali Suit",
        "brand": "Libas",
        "category": "Ethnic Wear",
        "merchants": {"Libas.com": 2499, "Myntra": 2699, "Ajio": 2799},
        "original_price": 3299,
        "coupon": "LIBAS15",
        "coupon_pct": 15,
        "cashback_pct": 5,
        "img": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=320&h=400&fit=crop",
        "tags": ["anarkali", "floral", "ethnic", "kurta", "suit", "pink", "festive"],
    },
    {
        "id": "P002",
        "name": "Silk Banarasi Saree",
        "brand": "Craftsvilla",
        "category": "Ethnic Wear",
        "merchants": {"Craftsvilla": 4999, "Myntra": 5299, "Amazon": 5499},
        "original_price": 6500,
        "coupon": "CRAFT20",
        "coupon_pct": 20,
        "cashback_pct": 8,
        "img": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=320&h=400&fit=crop",
        "tags": ["saree", "silk", "banarasi", "wedding", "traditional", "festive"],
    },
    {
        "id": "P003",
        "name": "Palazzo Kurta Set",
        "brand": "W for Woman",
        "category": "Ethnic Wear",
        "merchants": {"W Store": 1899, "Myntra": 1999, "Nykaa Fashion": 2099},
        "original_price": 2499,
        "coupon": "WSTORE10",
        "coupon_pct": 10,
        "cashback_pct": 3,
        "img": "https://images.unsplash.com/photo-1617627143233-97e0e3c49c84?w=320&h=400&fit=crop",
        "tags": ["palazzo", "kurta", "set", "casual", "ethnic", "co-ord"],
    },
    {
        "id": "P004",
        "name": "Embroidered Lehenga",
        "brand": "Biba",
        "category": "Ethnic Wear",
        "merchants": {"Biba": 7499, "Myntra": 7899, "Flipkart": 7699},
        "original_price": 9999,
        "coupon": "BIBA25",
        "coupon_pct": 25,
        "cashback_pct": 10,
        "img": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=320&h=400&fit=crop",
        "tags": ["lehenga", "embroidered", "bridal", "festive", "wedding", "party"],
    },
    {
        "id": "P005",
        "name": "Cotton Printed Dupatta",
        "brand": "Fabindia",
        "category": "Accessories",
        "merchants": {"Fabindia": 899, "Myntra": 949, "Amazon": 999},
        "original_price": 1200,
        "coupon": "FABI10",
        "coupon_pct": 10,
        "cashback_pct": 2,
        "img": "https://images.unsplash.com/photo-1639447096618-f87a9e80cc1f?w=320&h=400&fit=crop",
        "tags": ["dupatta", "cotton", "printed", "accessory", "ethnic", "stole"],
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def find_products(query: str, top_n: int = 3):
    q = query.lower()
    scored = []
    for p in CATALOG:
        score = sum(1 for tag in p["tags"] if tag in q)
        scored.append((score, p))
    scored.sort(key=lambda x: -x[0])
    top = [p for s, p in scored if s > 0][:top_n]
    return top if top else CATALOG[:top_n]


def best_price_info(product: dict):
    best_merchant = min(product["merchants"], key=product["merchants"].get)
    best_price = product["merchants"][best_merchant]
    discount = round((1 - best_price / product["original_price"]) * 100)
    return best_merchant, best_price, discount


def render_product_grid(products: list) -> str:
    cards = ""
    for p in products:
        merchant, price, disc = best_price_info(p)
        cards += f"""
        <div class="product-card">
            <img src="{p['img']}" alt="{p['name']}" />
            <div class="product-name">{p['name']}</div>
            <div class="product-brand">{p['brand']}</div>
            <div class="product-og">₹{p['original_price']:,}</div>
            <div class="product-price">₹{price:,}</div>
            <div class="badge-discount">{disc}% off</div>
        </div>"""
    return f'<div class="product-grid">{cards}</div>'


def render_price_table(products: list) -> str:
    rows = ""
    for p in products:
        merchant, price, disc = best_price_info(p)
        coupon_badge = f'<span class="coupon-pill">{p["coupon"]}</span>' if p.get("coupon") else ""
        rows += f"""
        <div class="price-row">
            <span>{p['name']}</span>
            <span><span class="price-best">₹{price:,}</span> @ {merchant} &nbsp;{coupon_badge}</span>
        </div>"""
    return f'<div class="price-table">{rows}</div>'


def render_profile_card(s: dict) -> str:
    return f"""
    <div class="profile-card">
        <div class="profile-avatar">👤</div>
        <div>
            <div class="profile-name">{s['name']} &nbsp;<span class="gold-badge">✦ {s['loyalty_tier']}</span></div>
            <div class="profile-meta">{s['social_handle']} · Rewards: <b style="color:#f0a500">₹{s['reward_balance']}</b> · Last order: {s['last_order_days']}d ago</div>
            <div class="profile-meta" style="margin-top:3px">📍 {s['saved_address']}</div>
        </div>
    </div>"""


def render_loyalty_card(s: dict) -> str:
    return f"""
    <div class="loyalty-card">
        <div class="loyalty-title">YOUR REWARD BALANCE</div>
        <div class="loyalty-amount">₹{s['reward_balance']}</div>
        <div class="loyalty-tier">✦ {s['loyalty_tier']} Member</div>
        <div style="margin-top:10px; font-size:13px; color:#bbb">
            Apply to your order and save ₹{s['reward_balance']} instantly. <br/>
            <b style="color:#eee">Reply "yes" to apply</b> or "skip" to proceed without.
        </div>
    </div>"""


def render_checkout_card(s: dict, product: dict, price_after_rewards: int) -> str:
    merchant, best_price, disc = best_price_info(product)
    coupon_line = f'<div class="checkout-row"><span>Coupon ({product["coupon"]})</span><span style="color:#f093fb">- ₹{round(best_price * product["coupon_pct"] / 100)}</span></div>' if product.get("coupon") else ""
    checkout_url = f"https://checkout.gokwik.co/demo?ref=curateai&user={s['social_handle'].replace('@','')}&product={product['id']}&price={price_after_rewards}&rewards={s['reward_balance']}"
    return f"""
    <div class="checkout-card">
        <div style="font-size:12px; color:#888; margin-bottom:12px; text-transform:uppercase; letter-spacing:1px">Your Personalised Checkout</div>
        <div style="font-size:15px; font-weight:600; color:#eee; margin-bottom:14px">{product['name']} · {product['brand']}</div>
        <div class="checkout-row"><span>Price @ {merchant}</span><span>₹{best_price:,}</span></div>
        {coupon_line}
        <div class="checkout-row"><span>GoKwik Rewards</span><span style="color:#22c55e">- ₹{s['reward_balance']}</span></div>
        <div class="checkout-row"><span>Cashback ({product['cashback_pct']}%)</span><span style="color:#22c55e">+ ₹{round(price_after_rewards * product['cashback_pct'] / 100)} back</span></div>
        <div style="border-top:1px solid #2a2a2a; margin: 10px 0 12px;"></div>
        <div class="checkout-row"><span style="font-size:14px">Total to Pay</span><span class="checkout-total">₹{max(0, price_after_rewards):,}</span></div>
        <div style="margin:10px 0 4px; font-size:12px; color:#666">
            📍 {s['saved_address']} &nbsp;|&nbsp; 👤 {s['name']}
        </div>
        <a href="{checkout_url}" target="_blank" class="checkout-btn">→ Tap to Checkout · Identity Pre-filled</a>
    </div>"""


def call_claude_vision(api_key: str, image_bytes: bytes, image_type: str) -> str:
    """Call Claude claude-sonnet-4-5 to identify fashion look from image."""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        b64 = base64.standard_b64encode(image_bytes).decode("utf-8")
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {"type": "base64", "media_type": image_type, "data": b64},
                    },
                    {
                        "type": "text",
                        "text": (
                            "You are a fashion AI for an Indian ethnic wear shopping app. "
                            "Analyse this image and identify: (1) the style of outfit, "
                            "(2) key fashion elements (silhouette, fabric, occasion), "
                            "(3) 3–5 search tags from this list: "
                            "[anarkali, saree, lehenga, kurta, palazzo, dupatta, suit, festive, wedding, casual, embroidered, silk, cotton, floral, bridal]. "
                            "Reply in 2 sentences max, then list the tags."
                        ),
                    },
                ],
            }],
        )
        return response.content[0].text
    except Exception as e:
        return f"ethnic festive wear — tags: anarkali, floral, festive"


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────────────────────
def init():
    defaults = {
        "stage": "ask_identity",
        "messages": [],
        "shopper": None,
        "products": [],
        "best_product": None,
        "rewards_applied": False,
        "api_key": "",
        "initialized": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()


# ─────────────────────────────────────────────────────────────────────────────
# AGENT LOGIC
# ─────────────────────────────────────────────────────────────────────────────
def add_msg(role: str, content: str, html: str = ""):
    st.session_state.messages.append({"role": role, "content": content, "html": html})


def handle_input(user_text: str, image_info: dict = None):
    add_msg("user", user_text)
    stage = st.session_state.stage

    # ── MOMENT 1: Identity ────────────────────────────────────────────────────
    if stage == "ask_identity":
        add_msg("agent",
            "Sending OTP to your number... 📱\n\n"
            "For this demo, your OTP is **`1234`**. Enter it below to verify.")
        st.session_state.stage = "otp_sent"

    elif stage == "otp_sent":
        if "1234" in user_text.strip():
            s = SHOPPER
            st.session_state.shopper = s
            profile_html = render_profile_card(s)
            add_msg("agent",
                f"✅ Verified! Welcome back, **{s['name']}** 👋\n\n"
                "Loaded your profile, loyalty tier, and reward balance.",
                html=profile_html)
            add_msg("agent",
                "What would you like to shop today?\n\n"
                "🖼️ **Upload a photo** of a look you love, or just **describe it** — "
                "e.g. *'something festive for Diwali'* or *'a saree for a wedding'*")
            st.session_state.stage = "ask_look"
        else:
            add_msg("agent", "That doesn't look right. Try **`1234`** for this demo.")

    # ── MOMENT 2: Shop the Look ───────────────────────────────────────────────
    elif stage == "ask_look":
        look_description = user_text

        if image_info:
            if st.session_state.api_key:
                vision_result = call_claude_vision(
                    st.session_state.api_key,
                    image_info["bytes"],
                    image_info["type"],
                )
                look_description = vision_result
                add_msg("agent",
                    f"✨ Got it! Here's what I see:\n\n_{vision_result}_\n\n"
                    "Searching our catalog for the closest matches...")
            else:
                add_msg("agent",
                    "✨ Love this look! Scanning the catalog for ethnic festive styles "
                    "that match the vibe...\n\n_(Add a Claude API key in the sidebar for real vision analysis)_")
        else:
            add_msg("agent",
                f"Searching across **{len(CATALOG)}+ styles** for _{look_description}_... ✨")

        products = find_products(look_description if not image_info else "festive ethnic kurta saree")
        st.session_state.products = products
        st.session_state.best_product = products[0]

        grid_html = render_product_grid(products)
        add_msg("agent",
            f"Found **{len(products)} picks** curated just for you 🛍️",
            html=grid_html)

        # ── MOMENT 3: Best Price ──────────────────────────────────────────────
        price_html = render_price_table(products)
        add_msg("agent",
            "🔍 **Price check across our merchant network:**\n\n"
            "Here's the best available deal — with all active coupons flagged:",
            html=price_html)

        # ── MOMENT 4: Loyalty ─────────────────────────────────────────────────
        s = st.session_state.shopper
        loyalty_html = render_loyalty_card(s)
        add_msg("agent",
            "💰 **One more thing** — you have rewards waiting:",
            html=loyalty_html)
        st.session_state.stage = "apply_loyalty"

    # ── MOMENT 5: Checkout ────────────────────────────────────────────────────
    elif stage == "apply_loyalty":
        s = st.session_state.shopper
        product = st.session_state.best_product
        _, best_price, _ = best_price_info(product)

        if any(w in user_text.lower() for w in ["yes", "apply", "sure", "ok", "yeah", "yep", "use"]):
            st.session_state.rewards_applied = True
            final_price = max(0, best_price - s["reward_balance"])
            checkout_html = render_checkout_card(s, product, final_price)
            add_msg("agent",
                f"✅ **₹{s['reward_balance']} rewards applied!**\n\n"
                "Your personalised checkout is ready — one tap and you're done:",
                html=checkout_html)
        else:
            checkout_html = render_checkout_card(s, product, best_price)
            add_msg("agent",
                "No problem! Your checkout is still locked at the best price:",
                html=checkout_html)

        st.session_state.stage = "done"

    elif stage == "done":
        add_msg("agent",
            "Your order's all set! 🎉\n\n"
            "Want to shop another look, or explore something else?")
        st.session_state.stage = "ask_look"


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✦ CurateAI")
    st.caption("AI Shopping Concierge · GoKwik PM Demo")
    st.divider()

    st.markdown("**Shopper Profile (Mock)**")
    s_preview = {
        "handle": SHOPPER["social_handle"],
        "tier": f"{SHOPPER['loyalty_tier']} ✦",
        "rewards": f"₹{SHOPPER['reward_balance']}",
        "top_category": SHOPPER["top_category"],
        "rto_count": SHOPPER["rto_count"],
    }
    st.json(s_preview)

    st.divider()
    st.markdown("**Claude API Key** _(optional)_")
    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="sk-ant-api03-...",
        label_visibility="collapsed",
    )
    if api_key:
        st.session_state.api_key = api_key
        st.success("Key saved — vision analysis active!")
    else:
        st.caption("Demo runs fully without a key. Add one to enable real Claude vision on image uploads.")

    st.divider()
    if st.button("🔄 Reset Demo", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    st.divider()
    st.markdown("**The 5 Moments**")
    stages_done = {
        "ask_identity": 0, "otp_sent": 1,
        "ask_look": 2, "apply_loyalty": 4, "done": 5,
    }
    current = stages_done.get(st.session_state.stage, 0)
    for i, label in enumerate([
        "Login & Identity", "Shop the Look",
        "Best Price", "Loyalty Apply", "Checkout"
    ], 1):
        icon = "✅" if i < current else ("🔵" if i == current else "⬜")
        st.markdown(f"{icon} Moment {i}: {label}")


# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-bar">
    <div class="avatar">✦</div>
    <div class="header-text">
        <h4>CurateAI &nbsp;<span class="online-dot"></span></h4>
        <p>Your personal shopping concierge · Powered by GoKwik Network</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# INITIAL WELCOME MESSAGE
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state.initialized:
    add_msg("agent",
        "Hi! I'm **CurateAI** ✦ — your personal shopping concierge.\n\n"
        "I know what you shop, what you've earned in rewards, and I can find you "
        "the best price across thousands of brands — all right here in chat.\n\n"
        "**Enter your Instagram handle or phone number to get started** 👇")
    st.session_state.initialized = True


# ─────────────────────────────────────────────────────────────────────────────
# RENDER CONVERSATION
# ─────────────────────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "agent":
        with st.chat_message("assistant", avatar="assistant"):
            if msg["content"]:
                st.markdown(msg["content"])
            if msg.get("html"):
                st.markdown(msg["html"], unsafe_allow_html=True)
    else:
        with st.chat_message("user", avatar="user"):
            st.markdown(msg["content"])


# ─────────────────────────────────────────────────────────────────────────────
# IMAGE UPLOAD (active only during shop_look stage)
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.stage == "ask_look":
    uploaded = st.file_uploader(
        "📸 Share a look (optional)",
        type=["jpg", "jpeg", "png", "webp"],
        key="img_upload",
        label_visibility="visible",
    )
    if uploaded:
        with st.chat_message("user", avatar="user"):
            st.image(uploaded, width=220, caption="Look I love 👆")
        img_info = {
            "bytes": uploaded.read(),
            "type": uploaded.type or "image/jpeg",
        }
        handle_input("I want to shop this look", image_info=img_info)
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# CHAT INPUT
# ─────────────────────────────────────────────────────────────────────────────
placeholder_map = {
    "ask_identity": "Enter your handle or phone number...",
    "otp_sent":     "Enter OTP (hint: 1234)...",
    "ask_look":     "Describe what you want to shop...",
    "apply_loyalty": "Type 'yes' to apply rewards, or 'skip'...",
    "done":          "Want to shop something else?",
}
placeholder = placeholder_map.get(st.session_state.stage, "Message CurateAI...")

user_input = st.chat_input(placeholder)
if user_input:
    handle_input(user_input)
    st.rerun()
