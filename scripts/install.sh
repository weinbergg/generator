#!/bin/bash

sudo apt update
sudo apt install make

# Установка библиотек из requirements.txt
pip install -r requirements.txt

# Запуск Flask-приложения
python app_prod.py  # Замените "ваш_файл.py" на имя вашего Flask-приложения
