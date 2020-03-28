import random

import game1_constants

list_of_questions_for_users = {}


def get_quotes():
    return game1_constants.__quotes__


def clear_list_of_questions_for_user(user_id):
    if user_id in list_of_questions_for_users:
        list_of_questions_for_users[user_id].clear()
        list_of_questions_for_users.pop(user_id)


def get_current_question_for_user(vk_id):
    if vk_id not in list_of_questions_for_users or len(list_of_questions_for_users[vk_id]) == 0:
        return "error1"
    return list_of_questions_for_users[vk_id][-1]


def get_answer_for_question(question):
    quotes = get_quotes()
    if question not in quotes:
        return "not found"
    return quotes[question]


def get_quote(vk_id):
    quotes = list(get_quotes())
    if vk_id not in list_of_questions_for_users:
        list_of_questions_for_users[vk_id] = [quotes[random.randint(0, len(quotes)-1)]]
        return list_of_questions_for_users[vk_id][0]
    if len(quotes) == len(list_of_questions_for_users[vk_id]):
        return "Молодец! Ты ответил верно на все вопросы!"
    question = list_of_questions_for_users[vk_id][0]
    while question in list_of_questions_for_users[vk_id]:
        question = quotes[random.randint(0, len(quotes)-1)]
    list_of_questions_for_users[vk_id].append(question)
    return question
