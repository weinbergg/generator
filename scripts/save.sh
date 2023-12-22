#!/bin/sh

chatId=$1
botToken=$2
curdir=$3

echo "Sending directory $curdir"

# Создаем архив директории
zip -r "$curdir.zip" "$curdir"

# Отправляем архив
curl -F chat_id=$chatId -F document=@"$curdir.zip" https://api.telegram.org/bot$botToken/sendDocument



# #!/bin/sh

# chatId=<YOUR_CHAT_ID>
# botToken=<YOUR_BOT_TOKEN>
# curdir=$PWD
# echo sending $curdir/$1

# curl -F chat_id=$chatId -F document=@$curdir/$1 https://api.telegram.org/bot$botToken/sendDocument
# # more about gist on my site — amorev.ru/telegram-terminal-file-send