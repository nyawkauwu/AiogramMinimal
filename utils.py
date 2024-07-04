from time import time

from aiogram import html

antiflood_dict = {}

def antiflood(user):
    limit = 0.2
    if user.id not in antiflood_dict or time() - antiflood_dict[user.id] > limit:
        antiflood_dict[user.id] = time()
        return True
    else:
        antiflood_dict[user.id] = time()
        return False
    
def link(user, force=False):
    if not force and user.username:
        return f"@{user.username}"
    else:
        return f"<a href='tg://user?id={user.id}'>{html.quote(user.first_name)}</a>"

def silent_link(tg_id, username, first_name):
    if username:
        return f"<a href='https://t.me/{username}'>{html.quote(first_name)}</a>"
    else:
        return f"<a href='tg://openmessage?user_id={tg_id}'>{html.quote(first_name)}</a>"
    
def hide_link(link):
    return f"<a href='{link}'>⁣</a>"

def get_message_tags(message):
    tags = []
    if message.entities:
        for entity in message.entities:
            if entity.type == "mention":
                tags.append({"text": message.text[entity.offset:][:entity.length]})
            elif entity.type == "text_mention":
                tags.append({"text": message.text[entity.offset:][:entity.length], "user": entity.user})
    return tags
