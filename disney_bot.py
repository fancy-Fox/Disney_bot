# coding=utf-8
import json
import random
import urllib.request
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType


import comands
import game1
import secret_constants


vk_session = vk_api.VkApi(token=secret_constants.token)

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

list_of_people_to_game1 = []


def write_message(user_id, msg):
    random_id = random.randint(1, 1234567898765)
    vk_session.method('messages.send', {'user_id': user_id, 'message': msg, 'random_id': random_id})


def is_correct_event(event):
    return event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user


def is_games(event):
    command = event.text.lower()
    if command in comands.__game1__:
        user_id = event.user_id
        if user_id in list_of_people_to_game1:
            write_message(user_id, 'вы уже играете')
            return True
        list_of_people_to_game1.append(user_id)
        question = game1.get_quote(user_id)
        write_message(user_id, question)
        return True
    return False


def main():
    for event in longpoll.listen():
        if not is_correct_event(event):
            continue
        if is_games(event):
            continue
        write_message(event.user_id, 'я вас не понимаю :-(')


main()
