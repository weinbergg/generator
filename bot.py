import requests
from dotenv import load_dotenv
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import subprocess


load_dotenv()
bot_token = os.getenv("bot_token")
chat_id_g = os.getenv("chat_id_g")
chat_id_a = os.getenv("chat_id_a")

user_ids = [chat_id_g, chat_id_a]
    
def send_telegram_message(chat_id, text):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'  # Или HTML, если требуется разметка
    }
    response = requests.post(url, data=payload)
    return response

# Отправка сообщений всем пользователям из списка
def send_all(message):
    for user_id in user_ids:
        response = send_telegram_message(user_id, message)
        # Проверка успешности отправки сообщения
        if response.status_code == 200:
            print(f'Сообщение было успешно отправлено пользователю с ID {user_id}')
        else:
            print(f'Не удалось отправить сообщение пользователю с ID {user_id}. Ответ сервера: {response.json()}')
   

script_path= "./scripts/save.sh"

def send_directory(bot, update):
    # chat_id = update.message.chat_id
    chat_id = chat_id_g

    # Определение текущей папки
    curdir = os.path.dirname(os.path.abspath(__file__))
    
    # Обеспечение корректных аргументов для shell-команды
    safe_curdir = subprocess.quote(curdir)
    safe_chat_id = subprocess.quote(str(chat_id))
    safe_token = subprocess.quote(bot_token)

    # Подготовка и выполнение команды
    shell_command = f"bash {script_path} {safe_curdir} {safe_chat_id} {safe_token}"
    subprocess.run(shell_command, shell=True)

def listener():
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    # Регистрация обработчика команд
    dp.add_handler(CommandHandler("senddir", send_directory))

    updater.start_polling()
    updater.idle()


# def send_directory(bot, update)
# if __name__ == '__bot__':
#     listener()

# def send_directory(bot, update):
#     chat_id = update.message.chat_id

#     # Подготавливаем команду для отправки текущей папки bot.py
#     curdir = os.path.dirname(os.path.abspath('/root/monocreator/MonoCreatorNew/blocks'))
#     shell_command = f"bash {script_path} '{curdir}' '{chat_id}' '{bot_token}'"

#     # Выполняем shell-скрипт
#     subprocess.run(shell_command, shell=True)


# def listener():
#     updater = Updater(bot_token, use_context=True)
#     dp = updater.dispatcher

#         # Регистрируем обработчик команд
#     dp.add_handler(CommandHandler("senddir", send_directory))

#     updater.start_polling()
#     updater.idle()


# send_directory(bot, update)

# send_all('Привет!')

# send_telegram_message('123')

# chat_id = 'weinbergg'

# def send_telegram_message(message):
#     url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
#     data = {
#         "chat_id": chat_id,
#         "text": message
#     }
#     # try:
#     #     response = requests.post(url, data).json()
#     #     # print(response.get('description'))
#     #     return response
#     # except Exception as e:
#     #     print(f"Ошибка при отправке сообщения в Телеграм: {e}")
#     #     return None