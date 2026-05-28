import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = 27686030       # ضع الـ API ID الخاص بك
api_hash = '486e18582e097bbc7eee3c59204781c4' # ضع الـ API HASH الخاص بك

async def generate_session():
    print("جاري الاتصال بتليجرام لإنشاء جلسة جديدة...")
    
    # هنا بنستخدم StringSession فارغ عشان نولد واحد جديد
    client = TelegramClient(StringSession(), api_id, api_hash)
    
    # السطر ده هيطلب منك رقم الموبايل والكود في الـ Terminal
    await client.start()
    
    print("\n=== انسخ النص الطويل الذي بالأسفل ===")
    print(client.session.save())
    print("=======================================\n")
    
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(generate_session())
