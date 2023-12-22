from bs4 import BeautifulSoup as bs
import requests
from functions.sql import base_create, base_insert
import deepl
import os
from ftplib import FTP
import paramiko
from dotenv import load_dotenv


def load_html_template(file_path):
    with open(file_path, "r") as inf:
        txt = inf.read()
    return bs(txt, "html.parser")


def save_html_template(soup, file_path):
    with open(file_path, "w") as outf:
        outf.write(str(soup))


def insert_into_db(path, data, name):
    base_create(path, name)
    for line in data:
        base_insert(path, name, line)


load_dotenv('/root/monocreator/MonoCreatorNew/.env')
DEEPL_KEY = os.getenv("DEEPL_KEY")
def translate(phrase):
    translator = deepl.Translator(DEEPL_KEY)
    result = translator.translate_text(phrase, target_lang="EN-US")
    translated_text = result.text

    return translated_text


def get_dollar():

    url = "https://www.google.com/search?q=курс+доллара+к+рублю"

    response = requests.get(url)
    soup = bs(response.content, "html.parser")
    result = soup.find("div", class_="BNeawe iBp4i AP7Wnd").get_text().split()[0]
    
    return float(result.replace(",", "."))


def send_host(ip, user, passwd, path_from, path_to, path_name):
    try:
        # создаем соединение
        ftp = FTP(ip)
        # пытаемся залогиниться
        ftp.login(user, passwd)
        ftp.mkd(f'/sites/{path_name}')
        # имя файла, который нужно отправить
        # открываем файл в бинарном режиме
        with open(path_from, 'rb') as file:
            # отправляем файл на ftp в папку /path/to/directory/
            ftp.storbinary('STOR %s' % path_to, file)
            # uncompress_command = f'unzip -o {file} -d {path_to}'
            # ftp.sendcmd(uncompress_command)
            # try:
            #     ftp.sendcmd(uncompress_command)
            # except Exception as e:
            #     print(f'Could not uncompress file: {e}')

        # закрываем соединение
        ftp.quit()

    except Exception as e:
        print("FTP error:", e)

    
def unzip_on_hosting(hostname, username, password, path_to, path_name):
    try:
        # Создаем SSH-клиент
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Устанавливаем соединение
        client.connect(hostname, username=username, password=password)
        
        # Формируем команду unzip
        print("Path to archive:", f"{path_to}")
        # unzip_command = f"tar -xf {path_to} -C {path_name}"
        unzip_command = f"unzip -o {path_to} -d {path_name}"

        
        # Выводим информацию о выполняемой команде
        print("Executing command:", unzip_command)
        
        # Выполняем команду unzip
        stdin, stdout, stderr = client.exec_command(unzip_command)
        
        # Выводим результат выполнения команды
        print("Command output:")
        print(stdout.read().decode())
        print("Error output:")
        print(stderr.read().decode())
        
        # Проверяем код возврата команды unzip
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            print("Unzip completed successfully.")
        else:
            print("Unzip command failed with exit status:", exit_status)
            print("Error output:")
            print(stderr.read().decode())
        
        # Закрываем соединение
        client.close()
    except paramiko.AuthenticationException as auth_error:
        print("Authentication error:", auth_error)
    except paramiko.SSHException as ssh_error:
        print("SSH error:", ssh_error)
    except Exception as e:
        print("Other error:", e)


def create_page(path, name, title, text):
    soup = load_html_template(f"html/{name}.html")

    title_tag = soup.find(id=f"{name}").find("h3")
    title_tag.string = title

    text_tag = soup.find(id=f"{name}").find("p")
    text_tag.string = text

    save_html_template(soup, f"{path}/{name}.html")

