import os

import telebot

import requests

from flask import Flask, request

from threading import Thread

link = "https://uploadfile.herokuapp.com/"

server = Flask("WebHook!")

TOKEN = "6269468548:AAG8upYBql2WDRYIdAGxnawJMycmj0WM7sE"

bot = telebot.TeleBot(TOKEN)

welcome_message = "مرحبًا! أنا بوت تليجرام لرفع الملفات. قم بإرسال ملف لي وسأقوم برفعه لك."

@bot.message_handler(commands=['start'])

def send_welcome(message):

    bot.reply_to(message, "*"+welcome_message+"*", parse_mode="Markdown")

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

@bot.message_handler(content_types=['document'])

def handle_document(message):

    file_id = message.document.file_id

    file_info = bot.get_file(file_id)

    file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}'

    file_name = message.document.file_name

    upload_link = upload_file(file_url, file_name)

    if upload_link:

        bot.reply_to(message, f"*تم رفع الملف بنجاح!\n\nرابط التحميل: *{upload_link}\n\nلشراء أو تفعيل بوت مماثل لهذا، تواصل معي @VIP3GL", disable_web_page_preview=True, parse_mode="Markdown")

    else:

        bot.reply_to(message, "*حدث خطأ أثناء رفع الملف.*", parse_mode="Markdown")

@server.route('/' + TOKEN, methods=['POST'])

def getMessage():

    json_string = request.get_data().decode('utf-8')

    update = telebot.types.Update.de_json(json_string)

    bot.process_new_updates([update])

    return "!", 200

@server.route("/")

def webhook():

    bot.remove_webhook()

    bot.set_webhook(url=link + TOKEN)

    return "!", 200

if __name__ == "__main__":

    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
