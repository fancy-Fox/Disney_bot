# coding=utf-8
import json
import random
import requests
import urllib.request
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType


import commands
import secret_constants
import table_active_questions
import table_answers
import table_records
import table_user
import table_questions


vk_session = vk_api.VkApi(token=secret_constants.token)

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


def write_message(user_id, msg):
    random_id = random.randint(1, 1234567898765)
    vk_session.method('messages.send', {'user_id': user_id, 'message': msg, 'random_id': random_id})


def is_correct_event(event):
    return event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user


def help_commands(event):
    command = event.text.lower()
    if command in commands.__help__:
        write_message(event.user_id, 'Список доступных вам команд:\n' +
                      'Начать игру - чтобы поиграть;\n' +
                      'Отпусти и забудь! - чтобы бот спел вам песенку;\n')
        return True
    return False


def sing_song(event):
    command = event.text.lower()
    if command in commands.__song__:
        write_message(event.user_id, "Что прошло уже не вернуть!")
        write_message(event.user_id, "Встречу я первый свой рассвет!")
        write_message(event.user_id, "Пусть бушует шторм!")
        write_message(event.user_id, "Холод всегда мне был по душе!")
        return True
    return False


def print_question(user_id, question):
    try:
        write_message(user_id, question[1])
        write_message(user_id, '1)' + table_answers.get_answer(question[2])[0])
        write_message(user_id, '2)' + table_answers.get_answer(question[3])[0])
        write_message(user_id, '3)' + table_answers.get_answer(question[4])[0])
        write_message(user_id, '4)' + table_answers.get_answer(question[5])[0])
    except Exception:
        write_message(user_id, 'При выводе вопроса произошла ошибка!')


def game1_try_to_answer(user_id, answer):
    question_id = table_active_questions.get_active_question(user_id)
    if question_id == -1:
        return False
    question_id = question_id[0]
    correct_answer = table_questions.get_correct_answer(question_id)[0]
    if not answer.isdigit():
        return False
    user_answer = table_questions.get_number_of_answer_with_question_id_and_position(question_id, int(answer))
    return user_answer == correct_answer


def is_game1_start(event):
    command = event.text.lower()
    if command in commands.__game1_start__:
        user_id = event.user_id
        if table_active_questions.is_user_in_game(event.user_id):
            write_message(event.user_id, 'Вы уже участвуете в игре')
            current_question_id = table_active_questions.get_active_question(event.user_id)[0]
            question = table_questions.get_question(current_question_id)[0]
            print_question(event.user_id, question)
            return True
        getting_question = table_questions.get_some_question(user_id)
        if 'victory' in getting_question:
            write_message(event.user_id, 'Удивительно, но вы победили! Поздравляю!')
            table_active_questions.remove_all_question_for_user(event.user_id)
            return True
        if 'error' in getting_question:
            write_message(event.user_id, 'Что-то пошло не так, не удалось получить вопрос! Приносим свои извинения :-(')
            return True
        table_active_questions.add_new_question(user_id, int(getting_question[0]))
        question = table_questions.get_question(getting_question[0])
        print_question(event.user_id, question[0])
        return True
    return False


def is_game1(event):    # TODO объединить с функцией выше
    command = event.text.lower()
    if is_game1_start(event):
        return True
    if command in commands.__game1_record__:
        points = str(table_records.get_record_with_user_id(event.user_id))
        write_message(event.user_id, 'Ваш рекорд в игре: ' + points)
        return True
    if table_active_questions.is_user_in_game(event.user_id):
        if command in commands.__game1_pause__:     # TODO написать евристику для паузы
            return True
        if not game1_try_to_answer(event.user_id, command):
            points = str(table_active_questions.get_count_of_solved_questions(event.user_id))
            table_active_questions.remove_all_question_for_user(event.user_id)
            table_records.insert_new_record(event.user_id, points)
            write_message(event.user_id, 'Вы дали неверный ответ. Ваш счет: ' + points + '.\n Попробуйте снова!')
            return True
        getting_question = table_questions.get_some_question(event.user_id)
        if 'victory' in getting_question:
            write_message(event.user_id, 'Вы победили! Поздравляю!')
            points = str(table_active_questions.get_count_of_solved_questions(event.user_id))
            table_records.insert_new_record(event.user_id, points)
            table_active_questions.remove_all_question_for_user(event.user_id)
            return True
        if 'error' in getting_question:
            write_message(event.user_id, 'Что-то пошло не так, не удалось получить вопрос! Приносим свои извинения :-(')
            return True
        table_active_questions.add_new_question(event.user_id, getting_question[0])
        question = table_questions.get_question(getting_question[0])
        print_question(event.user_id, question[0])
        return True
    return False


def exit_command(event):
    if event.text.lower() == "вырубай" and (str(event.user_id) == "262942796" or str(event.user_id) == '308881991'
                                            or str(event.user_id) == '30806644'):
        write_message(event.user_id, "пока)")
        exit()


def is_from_admin(event):
    return False


def is_sync_command(event):
    if event.text.lower() in commands.__registration__:
        if table_user.insert_new_user(('unknown nick', event.user_id, )):
            write_message(event.user_id, 'Регистрация прошла успешно!')
        else:
            write_message(event.user_id, 'Вы уже зарегистрированы!')
        return True
    return False


def is_table_users_command(event):
    if is_sync_command(event):
        return True
    if is_rename_command(event):
        return True
    return False


def is_rename_command(event):
    split_command = event.text.split()
    if split_command[0] in commands.__rename__:
        for i in range(2, len(split_command) - 1):
            split_command[1] += split_command[i]
        if table_user.change_nick(event.user_id, split_command[1]):
            write_message(event.user_id, 'Смена имени произошло успешно!')
        else:
            write_message(event.user_id, 'Произошла ошибка при смене имени.')
        return True
    return False


def main():
    for event in longpoll.listen():
        if not is_correct_event(event):
            continue
        exit_command(event)
        if is_table_users_command(event):
            continue
        if is_from_admin(event):
            continue
        if help_commands(event):
            continue
        if is_game1(event):
            continue
        if sing_song(event):
            continue
        write_message(event.user_id, 'я вас не понимаю :-(')


main()
