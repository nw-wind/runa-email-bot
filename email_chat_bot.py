#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import email
import logging
from imapclient import IMAPClient
import base64
import requests

from config import *

if log_level is None:
    log_level = logging.DEBUG

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=log_level)
log=logging.getLogger(__name__)
log.info("Бот в полветра. Старт.")

url = f"https://api.telegram.org/bot{token}/sendMessage"

def tryb64(s):
    ds = []
    dh = email.header.decode_header(s)   
    log.debug(f"Header: {dh}")
    for th in dh:
        log.debug(f"{type(th[0])}")
        try:
            if th[1] is None:
                en = 'utf-8'
            else:
                en = th[1]
            ds.append(th[0].decode(en))
            log.debug(f"base64: {ds}")
        except (UnicodeDecodeError, AttributeError, TypeError):
            ds.append(str(th[0]))
            log.debug(f"str: {ds}")
    return "".join(ds)

with IMAPClient(imap_server, use_uid=True) as server:
    server.login(imap_login, imap_password)
    info = server.select_folder('INBOX')
    messages = server.search("UNSEEN")
    #messages = server.search("SEEN")
    for uid, message_data in server.fetch(messages, "RFC822").items():
         email_message = email.message_from_bytes(message_data[b"RFC822"])
         efrom = tryb64(email_message.get("From"))
         esubject = tryb64(email_message.get("Subject"))
         log.debug(f"{uid}\nFrom: {efrom}\nSubject: {esubject}")
         for part in email_message.walk():
             if part.get_content_type() == "text/plain":
                 body = part.get_payload()
                 dbody = " ".join(body.split("\n")).replace("\r","")
                 log.debug(f"{body}")
                 log.info(f"Письмо: {dbody}")
                 chat_data = {
                    "chat_id": group_id,
                    "disable_web_page_preview": 1,
                    "text": body
                 }
                 rc = requests.post(url, data=chat_data)
                 log.debug(f"Ответ: {rc}")
             else:
                 log.debug(f"Непонятное: {part.get_content_type()}")
                 
log.info("Бот в полветра. Стоп.")
