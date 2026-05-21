import asyncio
import logging
import os
import json
import httpx
from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger(__name__)

API_ID       = int(os.getenv("TELEGRAM_API_ID"))
API_HASH     = os.getenv("TELEGRAM_API_HASH")
DEST_CHANNEL = os.getenv("DEST_CHANNEL")
GEMINI_KEY   = os.getenv("GEMINI_API_KEY")

SOURCE_CHANNELS = [
    ch.strip()
    for ch in os.getenv("SOURCE_CHANNELS", "").split(",")
    if ch.strip()
]

# ─── Gemini ──────────────────────────────────────────────────────
async def classify(text: str) -> dict:
    """
    يصنف الرسالة ويرجع dict دايماً — حتى لو مش عرض.
    """
    prompt = f"""صنّف الرسالة التالية وأرجع JSON فقط بدون أي نص أو backticks.

الرسالة:
{text}

أرجع دايماً هذا الشكل:
{{
  "is_deal": true أو false,
  "category": "إلكترونيات" أو "أجهزة منزلية" أو "موضة وأزياء" أو "صحة وجمال" أو "رياضة" أو "طعام ومشروبات" أو "كتب وتعليم" أو "أخرى",
  "store": "amazon" أو "noon" أو "jumia" أو "other",
  "discount": رقم أو null
}}

إذا كانت الرسالة مش عرض (أخبار، كلام عادي، إعلان بدون سعر):
is_deal = false والباقي "أخرى" و "other" و null"""

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}",
                json={"contents": [{"parts": [{"text": prompt}]}]}
            )
        data = resp.json()
        raw  = data["candidates"][0]["content"]["parts"][0]["text"]
        raw  = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
    except Exception as e:
        log.warning(f"⚠️ Gemini error: {e}")
        # لو فشل الـ API — يبعت تحت أخرى
        return {"is_deal": False, "category": "أخرى", "store": "other", "discount": None}


# ─── مساعدات ────────────────────────────────────────────────────
CATEGORY_EMOJI = {
    "إلكترونيات":     "📱",
    "أجهزة منزلية":  "🏠",
    "موضة وأزياء":   "👗",
    "صحة وجمال":     "💄",
    "رياضة":         "⚽",
    "طعام ومشروبات": "🍔",
    "كتب وتعليم":    "📚",
    "أخرى":          "🗂️",
}

STORE_LABEL = {
    "amazon": "📦 أمازون",
    "noon":   "🟡 نون",
    "jumia":  "🟠 جوميا",
    "other":  "🛒",
}

def build_tag(result: dict, channel_name: str) -> str:
    cat      = result.get("category", "أخرى")
    store    = result.get("store", "other")
    discount = result.get("discount")
    is_deal  = result.get("is_deal", False)

    emoji    = CATEGORY_EMOJI.get(cat, "🗂️")
    parts    = [f"{emoji} {cat}", STORE_LABEL.get(store, "🛒")]

    if is_deal and discount:
        parts.append(f"🔥 خصم {discount}%")

    if not is_deal:
        parts.append("🗂️ أخرى")

    parts.append(f"📢 @{channel_name}")
    return " | ".join(parts)


# ─── البوت ──────────────────────────────────────────────────────
async def main():
    log.info("🚀 تشغيل البوت...")

    client = TelegramClient("deals_session", API_ID, API_HASH)
    await client.start()
    log.info("✅ متصل بتيليجرام")

    dest_entity = await client.get_entity(DEST_CHANNEL)
    dest_id     = dest_entity.id
    log.info(f"📬 قناة الوجهة: {DEST_CHANNEL}")

    source_entities = []
    for ch in SOURCE_CHANNELS:
        try:
            entity = await client.get_entity(ch)
            source_entities.append(entity)
            log.info(f"📡 متابعة: {ch}")
        except Exception as e:
            log.warning(f"⚠️ خطأ في {ch}: {e}")

    source_ids   = {e.id for e in source_entities}
    source_names = {e.id: (e.username or e.title) for e in source_entities}

    @client.on(events.NewMessage(chats=list(source_ids)))
    async def handle(event):
        text         = event.message.text or ""
        channel_name = source_names.get(event.chat_id, str(event.chat_id))

        # صنّف بـ Gemini
        result = await classify(text) if text.strip() else {"is_deal": False, "category": "أخرى", "store": "other", "discount": None}

        tag = build_tag(result, channel_name)
        label = "✅ عرض" if result.get("is_deal") else "🗂️ أخرى"
        log.info(f"[{channel_name}] {label} → {result.get('category')} | {result.get('store')}")

        try:
            await client.send_message(dest_id, f"`{tag}`", parse_mode="md")
            await client.forward_messages(dest_id, event.message)
        except Exception as e:
            log.error(f"❌ فشل الإرسال: {e}")

    log.info(f"👂 يراقب {len(source_entities)} قناة — كل رسالة تتبعت")
    log.info("─" * 50)
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())