import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = 27686030 
api_hash = '486e18582e097bbc7eee3c59204781c4'

# ضع النص الطويل الحقيقي الذي استخرجته هنا بدلاً من الكلمة العربية
session_string = "1BJWap1sBuwzZocBuowhuSMhOYPL_Nkj_MQdcEdVWZ3hygFqAuo0H_ltxhGDHKMXZtajKv7Ig22xU_XpVEP78N1xCh_aN6WVelXRvYTZ1PIin1LvkjFAZLGoBNDcATZAzOa0ywyD1yY-RWnkc-owvGzCY4zgPmzmCn5BFGriQBz6pmJFaS2rltWfIAsU3-AJ5ZVjAYc9nR9lTWMO_45uDju-ECn5TuimrCDqoNSwrAuKBk0Q434LIaRL7UTsiS8tLkoMUiu1Xn-0owx9D0voePfmlYOT-yDeW1CFST13Bn_EgL0lf1W1Cc4GwEIZlfqx7IhWoh-ldaMfRqNzE6dqEezkL0EsIRRI=" 

async def main():
    client = TelegramClient(StringSession(session_string), api_id, api_hash)
    await client.start()
    print("البوت يعمل بنجاح!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())