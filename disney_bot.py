# coding=utf-8
import json
import random
import urllib.request
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType


import commands
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


def is_game1_start(event):
    command = event.text.lower()
    if command in commands.__game1__:
        user_id = event.user_id
        if user_id in list_of_people_to_game1:
            write_message(user_id, 'вы уже играете')
            return True
        list_of_people_to_game1.append(user_id)
        question = game1.get_quote(user_id)
        write_message(user_id, question)
        return True
    return False


def is_answer_correct(event, user_answer):
    quote = game1.get_current_question_for_user(event.user_id)
    if quote == "error1":
        return False
    return user_answer == game1.get_answer_for_question(quote)


def stop_game1(event):
    game1.clear_list_of_questions_for_user(event.user_id)
    if event.user_id in list_of_people_to_game1:
        list_of_people_to_game1.remove(event.user_id)


def is_game1_stop(event, command):
    if command in commands.__stop__:
        stop_game1(event)
        return True
    return False


def is_in_game_now(event):
    return event.user_id in list_of_people_to_game1


def is_game1(event):
    command = event.text.lower()
    if is_game1_start(event):
        return True
    if not is_in_game_now(event):
        return False
    if is_game1_stop(event, command):
        return True
    if is_answer_correct(event, command):
        write_message(event.user_id, "Вы ответили верно!")
        quote = game1.get_quote(event.user_id)
        if quote == "Молодец! Ты ответил верно на все вопросы!":
            write_message(event.user_id, quote)
            stop_game1(event)
            return True
        write_message(event.user_id, quote)
        return True
    stop_game1(event)
    write_message(event.user_id, "Увы, вы ошиблись(((   Попробуйте ещё разочек)))")
    return True


def main():
    for event in longpoll.listen():
        if not is_correct_event(event):
            continue
        if is_game1(event):
            continue
        write_message(event.user_id, 'я вас не понимаю :-(')


main()
