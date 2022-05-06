@echo off
:loop
python email_chat_bot.py
timeout 15
goto loop

