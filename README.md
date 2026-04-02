# ✦ CurateAI
### AI-Powered Shopping Concierge · GoKwik PM Assignment

> An AI agent that lives inside a social chat thread — taking a shopper from product discovery to personalised checkout in 5 moments. No redirects. No app switching. Just chat.


## Demo Flow

```
Enter handle → OTP verify → Describe a look → Best price → Apply rewards → One-tap checkout
```



## The 5 Moments

| # | Moment | What the Agent Does |
|---|--------|---------------------|
| 1 | Login & Identity | Recognises the shopper via social handle + OTP. Loads profile, loyalty tier, and reward balance silently in context. |
| 2 | Shop the Look | Shopper shares an image or describes a style. Agent uses Claude vision + LLM to identify the look and surfaces 3–5 shoppable products. |
| 3 | Best Price | Checks the product price across the merchant network, surfaces the best deal, and flags active coupons and cashback. |
| 4 | Loyalty Apply | Surfaces the shopper's reward balance and applies it to the order — entirely within the chat thread, no redirect. |
| 5 | Checkout | Generates a pre-filled, personalised checkout link — identity pre-populated, rewards applied, best price locked — ready in one tap. |

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/pmayush/curateai/tree/main && cd curateai

# 2. Install dependencies
pip install streamlit anthropic

# 3. Run
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) — the demo runs fully without an API key.

**To enable real Claude vision on image uploads**, add your Anthropic API key in the sidebar of the running app. Get one free at [console.anthropic.com](https://console.anthropic.com).



## Architecture

```
curateai/
├── app.py           ← Single-file Streamlit app (all logic + UI)
├── README.md        ← This file
└── product_note.md  ← 1-page product thinking
```

### Shopper Profile (mocked)

```json
{
  "social_handle":  "@priya.styles",
  "loyalty_tier":   "Gold",
  "reward_balance": 840,
  "last_order_days": 12,
  "top_category":   "Ethnic Wear",
  "rto_count":      1,
  "saved_address":  "12 Marine Drive, Mumbai 400001",
  "past_brands":    ["Libas", "Biba", "W for Woman"]
}
```

### Product Catalog (mocked)

```json
{
  "id": "P001",
  "name": "Floral Anarkali Suit",
  "brand": "Libas",
  "merchants": { "Libas.com": 2499, "Myntra": 2699, "Ajio": 2799 },
  "original_price": 3299,
  "coupon": "LIBAS15",
  "coupon_pct": 15,
  "cashback_pct": 5,
  "tags": ["anarkali", "floral", "ethnic", "festive"]
}
```

### Agent State Machine

```
ask_identity → otp_sent → ask_look → apply_loyalty → done
     │              │           │            │           │
  Moment 1      Moment 1    Moments        Moment 4   Moment 5
  (handle)       (OTP)      2 + 3         (loyalty)  (checkout)
```

Moments 2, 3, and 4 are chained automatically — once the shopper shares a look, the agent surfaces products → best prices → loyalty options in a single threaded response.



## LLM Prompts

### Prompt 1 — Vision / Shop the Look
**Trigger:** User uploads an image (Moment 2)  
**Model:** `claude-sonnet-4-5`

```
You are a fashion AI for an Indian ethnic wear shopping app.
Analyse this image and identify:
  (1) the style of outfit,
  (2) key fashion elements (silhouette, fabric, occasion),
  (3) 3–5 search tags from this list:
      [anarkali, saree, lehenga, kurta, palazzo, dupatta, suit,
       festive, wedding, casual, embroidered, silk, cotton, floral, bridal].
Reply in 2 sentences max, then list the tags.
```

**Why constrained tags?** Prevents hallucinated categories that don't exist in the catalog. Keeps the agent fast and predictable.

### Prompt 2 — Product Matching (text input)
**Method:** Tag-based keyword scoring — no LLM call  
**Logic:** `score = count of catalog tags appearing in user query`  
**Why no LLM?** For text queries, lightweight tag matching is faster, cheaper, and more debuggable. LLM is reserved for the hard vision problem.

### Prompt 3 — Personalised Ranking (v2 planned)

```
You are a shopping concierge for a returning Gold-tier shopper.
Shopper profile: {profile_json}
Products found: {products_json}
Rank these products considering: loyalty tier, top category, past brands, RTO history.
Return a JSON array of product IDs in ranked order with a 1-sentence reason for the top pick.
```



## Model Choices

| Decision | Choice | Why |
|----------|--------|-----|
| Vision analysis | Claude Sonnet 4.5 | Multimodal, strong fashion understanding, single API call |
| Text matching | Tag scoring (no LLM) | Sub-10ms, deterministic, easier to debug |
| Checkout generation | Template (no LLM) | Structured data — LLMs add hallucination risk to prices |
| v2 ranking | Claude Haiku (planned) | Low-stakes personalisation, high throughput, cheap |



## Failure Modes Handled

| Edge Case | How It's Handled |
|-----------|-----------------|
| Unknown shopper | OTP flow falls through to new user path (v2) |
| Image not recognised | Fallback to "festive ethnic" category with top catalog picks |
| No products matched | Returns top 3 catalog items as default |
| API key missing | Full mock mode — all responses pre-designed |
| Rewards exceed price | `max(0, price - rewards)` prevents negative checkout value |



## What I'd Build in v2

1. **Real identity layer** — GoKwik network lookup by phone/social handle, real OTP via SMS
2. **Semantic search** — Replace tag matching with vector embeddings over a live product catalog
3. **Multi-brand basket** — Add products from multiple brands; agent optimises reward split across checkout
4. **Proactive concierge** — Agent notices the shopper hasn't ordered in 12 days and initiates the DM
5. **RTO risk scoring** — Flag high-RTO shoppers before checkout; offer prepaid incentive

