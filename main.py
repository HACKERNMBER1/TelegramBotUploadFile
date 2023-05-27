import os
from pyrogram import Client, filters
import requests

app = Client(
    "my_bot",
    api_id=10311512,
    api_hash="49589a9b575a64954e9f59062c2a3e76",
    bot_token="6269468548:AAG8upYBql2WDRYIdAGxnawJMycmj0WM7sE"
)

welcome_message = "مرحبًا! أنا بوت تليجرام لرفع الملفات. قم بإرسال ملف لي وسأقوم برفعه لك."

@app.on_message(filters.command("start"))
def start(client, message):
    client.send_message(
        message.chat.id,
        f"<b>{welcome_message}</b>",
        parse_mode="html"
    )

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

@app.on_message(filters.document)
def handle_document(client, message):
    file_info = message.document
    file_url = client.get_download_url(file_info)
    file_name = file_info.file_name
    upload_link = upload_file(file_url, file_name)
    if upload_link:
        client.send_message(
            message.chat.id,
            f"<b>تم رفع الملف بنجاح!\n\nرابط التحميل: {upload_link}\n\nلشراء أو تفعيل بوت مماثل لهذا، تواصل معي @VIP3GL</b>",
            disable_web_page_preview=True,
            parse_mode="html"
        )
    else:
        client.send_message(
            message.chat.id,
            "<b>حدث خطأ أثناء رفع الملف.</b>",
            parse_mode="html"
        )

if __name__ == "__main__":
    app.run()
