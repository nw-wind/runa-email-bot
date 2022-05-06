# Бот для ООО Руна, читает почту и отправляет в группу ТГ

Для установки надо:

```
pip3 install virtualenv
pip3 -m vertualenv venv
source ./venv/bin/activate
pip3 install imapclient requests
```

В винде что-то типа:
```
pip3 install virtualenv
pip3 -m vertualenv venv
venv/bin/activate.bat
pip3 install imapclient requests
```

Для запуска надо:

```
cd папка
while true; do python3 email_chat_bot.py; sleep 15; done
```

Ну или в крон поставить как-то...

