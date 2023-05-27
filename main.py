import os
import requests
from pyrogram import Client, filters

TOKEN = "6269468548:AAG8upYBql2WDRYIdAGxnawJMycmj0WM7sE"
API_ID = 10311512
API_HASH = "49589a9b575a64954e9f59062c2a3e76"

bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN
)

link = "https://uploadfile.herokuapp.com/"

welcome_message = "مرحبًا! أنا بوت تليجرام لرفع الملفات. قم بإرسال ملف لي وسأقوم برفعه لك."

@bot.on_message(filters.command("start"))
def send_welcome(client, message):
    client.send_message(message.chat.id, welcome_message)

def upload_file(file_url, file_name):
    response = requests.get(file_url)
    file_data = response.content
    with open(file_name, "wb") as file:
        file.write(file_data)
    response = requests.post("https://api.anonfiles.com/upload", files={'file': open(file_name, "rb")})
    if response.status_code == 200:
        data = response.json()
        if data['status']:
            return data['data']['file']['url']['short']
    return None

@bot.on_message(filters.document)
def handle_document(client, message):
    file_info = client.get_file(message.document.file_id)
    file_path = client.download_media(file_info)
    file_name = message.document.file_name
    upload_link = upload_file(file_path, file_name)
    os.remove(file_path)
    if upload_link:
        client.send_message(message.chat.id, f"تم رفع الملف بنجاح!\n\nرابط التحميل: {upload_link}\n\nلشراء أو تفعيل بوت مماثل لهذا، تواصل معي @VIP3GL", disable_web_page_preview=True)
    else:
        client.send_message(message.chat.id, "حدث خطأ أثناء رفع الملف.")

bot.run()
