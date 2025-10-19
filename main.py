"""
Ultra Fast Telegram Userbot (Instant Comment + Auto Reply)
24/7 versiya (Replit + Flask + UptimeRobot)
Muallif: ChatGPT (GPT-5)
"""

from telethon import TelegramClient, events
import asyncio
import datetime
import random
from flask import Flask
import threading

# === SOZLAMALAR ===
API_ID = 25501859
API_HASH = "3794184d222264f05dbc4622f3962b5f"
SESSION_NAME = "userbot_session"

# === JAVOB VA KOMMENT SOZLAMALARI ===
AUTO_REPLY_TEXT = "Hozir javob bera olmayman. Keyinroq yozsangiz, albatta javob beraman."
AUTO_COMMENT_TEXTS = ["9860350149462219"]

# === KANAL KUZATISH (link yoki @username) ===
WATCHED_CHANNEL = "wkjefdckewnc"

# === FLASK WEB SERVER ===
app = Flask('')

@app.route('/')
def home():
    return "✅ Telegram Userbot 24/7 ishlayapti!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# Flask serverni alohida oqimda ishga tushuramiz
threading.Thread(target=run_flask).start()


# === TELETHON ASOSIY KOD ===
async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    # --- Xususiy xabarlarga avtomatik javob ---
    @client.on(events.NewMessage(incoming=True))
    async def reply_private(event):
        if event.is_private:
            try:
                await event.reply(AUTO_REPLY_TEXT)
                sender = await event.get_sender()
                print(f"[{datetime.datetime.now()}] ✅ {sender.first_name} ga javob yuborildi.")
            except Exception as e:
                print(f"⚠️ Xatolik (javob): {e}")

    # --- Kanalni kuzatish ---
    async def watch_channel():
        last_id = 0
        try:
            entity = await client.get_entity(WATCHED_CHANNEL)
            print(f"📡 Kanal kuzatish boshlandi: {entity.title}")
        except Exception as e:
            print(f"⚠️ Kanalga ulanib bo‘lmadi: {e}")
            return

        while True:
            try:
                posts = await client.get_messages(entity, limit=1)
                if posts and posts[0].id != last_id:
                    last_id = posts[0].id
                    msg_id = posts[0].id
                    text = random.choice(AUTO_COMMENT_TEXTS)
                    await client.send_message(entity=entity, message=text, comment_to=msg_id)
                    print(f"[{datetime.datetime.now()}] ⚡ Tezkor komment yozildi: {text}")
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"⚠️ Kuzatishda xatolik: {e}")
                await asyncio.sleep(3)

    async with client:
        print("🤖 Userbot ishga tushdi — real-time komment va javoblar faol.")
        await asyncio.gather(
            client.run_until_disconnected(),
            watch_channel(),
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("⏹ To‘xtatildi (foydalanuvchi tomonidan).")
