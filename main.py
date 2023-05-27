import os
import time
from pyrogram import Client, filters

API_ID = 10311512
API_HASH = '49589a9b575a64954e9f59062c2a3e76'
BOT_TOKEN = '6269468548:AAG8upYBql2WDRYIdAGxnawJMycmj0WM7sE'

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

welcome_message = "مرحبًا! أنا بوت تليجرام لرفع الملفات. قم بإرسال ملف لي وسأقوم برفعه لك."

@app.on_message(filters.command('start'))
async def send_welcome(_, message):
    await message.reply_text(f"*{welcome_message}*", parse_mode="Markdown")

def upload_file(file_path):
    with open(file_path, 'rb') as file:
        response = app.send_document("2069862545", file)
        return response.link

@app.on_message(filters.document)
async def handle_document(_, message):
    file_name = message.document.file_name
    file_path = await app.download_media(message)
    upload_link = upload_file(file_path)
    if upload_link:
        await message.reply_text(f"*تم رفع الملف بنجاح!\n\nرابط التحميل: *{upload_link}\n\nلشراء أو تفعيل بوت مماثل لهذا، تواصل معي @VIP3GL", disable_web_page_preview=True, parse_mode="Markdown")
    else:
        await message.reply_text("*حدث خطأ أثناء رفع الملف.*", parse_mode="Markdown")

if __name__ == "__main__":
    app.run()
