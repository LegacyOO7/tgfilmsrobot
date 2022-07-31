# MIT License
# Copyright (c) 2022 Muhammed
import os, re
search = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default


# Creator
CREATOR_NAME = os.environ.get("CREATOR_NAME", "???")
CREATOR_USERNAME = os.environ.get("CREATOR_USERNAME", "???")

# Account
API_HASH = os.environ.get("API_HASH", "")
API_ID = os.environ.get("API_ID", "")
# About Bot
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
PICS = os.environ.get("PICS", "")
# Database
DATABASE_NAME = os.environ.get("DATABASE_NAME", "LuciferMoringstar-Robot")
DATABASE_URI = os.environ.get("DATABASE_URI", "")
# Chats & Users
ADMINS = os.environ.get("ADMINS", "2028425293 1637186875")
SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "TgFilmsupdates")
AUTH_CHANNEL = os.environ.get("AUTH_CHANNEL", "")
CHANNELS = [int(ch) if search.search(ch) else ch for ch in os.environ.get("CHANNELS", "").split()]
LOG_CHANNEL = os.environ.get("LOG_CHANNEL", "")
GET_FILECHANNEL = os.environ.get("GET_FILECHANNEL", "")
FILTER_DEL_SECOND = int(os.environ.get("FILTER_DEL_SECOND", "600"))

# AutoFilter
AUTH_GROUPS = os.environ.get("AUTH_GROUPS", "")
AUTH_USERS = [int(user) if search.search(user) else user for user in os.environ.get('AUTH_USERS', '').split()]
FILTER_BUTTONS = os.environ.get("FILTER_BUTTONS", "10")
PROTECT_FILES = is_enabled((os.environ.get('PROTECT_FILES', "True")), True) 
