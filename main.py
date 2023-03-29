from flask import Flask, request
from dialogs import *
from random import randint
from triple_nonsense import *
from Find_Definition import check
from abbreviation import *
import pymorphy2
import time

morph = pymorphy2.MorphAnalyzer()
app = Flask(__name__)

status_list = {}
letter = ''
counter = 0
questions = []


def make_resp(response_text, end_session, buttons):
    resp = {
        'response': {
            'text': response_text,
            'end_session ': end_session,
            'buttons': buttons
        },
        'version': '1.0'
    }
    print(resp['response']['text'])
    with open('logs.txt', 'a', encoding="utf8") as f:
        f.write(f'Filya: {resp["response"]["text"]}')
        f.write('\n')
        f.write('\n')
        f.write('\n')
    print(' ')
    return resp


@app.route('/', methods=['POST'])
def response():

    # variables for response and working
    global status_list
    global letter
    global questions
    global counter
    end_session = False
    response_text = ''
    buttons = []

    # buttons sets
    all_btns = [{'title': 'Правила каждой', 'hide': False},
                {'title': 'Тройная чепуха', 'hide': False},
                {'title': 'Запрещённая буква', 'hide': False},
                {'title': 'Аббревиатура', 'hide': False}, ]
    dec_btns = [{'title': 'Я согласен', 'hide': False},
                {'title': 'Не хочу', 'hide': False}, ]

    # getting and filtering user input
    text = request.json.get('request', ()).get('command')
    text = text.lower()

    for k in ('!', '?', '.'): 
            text = text.replace(k, ' ')
    text = text.replace('ё', 'е')
    text = text.strip()

    # getting user's id
    user_id = request.json.get('session', ()).get('user_id')
    new = request.json.get('session', ()).get('new')

    if user_id not in status_list: status_list[user_id] = 0
    if new: status_list[user_id] = 0

    # writting logs
    print(text)
    print(f'status: {status_list[user_id]}    user id: {user_id}')
    with open('logs.txt', 'a', encoding="utf8") as f:
        f.write(time.ctime())
        f.write('\n')
        f.write(f'status: {status_list[user_id]}    user id: {user_id}')
        f.write('\n')
        f.write('\n')
        f.write(f'user: {text}')
        f.write('\n')
        f.write('\n')


    # checking if user wants to exit
    if text in exit_phrases:
        response_text = 'До свидания! Закрываю навык.'
        end_session = True
        buttons = []
        status_list[user_id] = 0
        return make_resp(response_text, end_session, buttons)

    # users bored phrases               
    if text in bored:
        response_text = 'Ну и чем займеся? Поиграем в другие игры или может помолчим?'
        buttons = all_btns
        status_list[user_id] = 0
        return make_resp(response_text, end_session, buttons)

    # find def in dict for user    
    if 'что значит' in text:
        s = text.split()
        response_text = f"По толковому словарю Ожигова: {check(s[s.index('значит') + 1])}. \nВо что будем играть дальше?"
        buttons = all_btns
        status_list[user_id] = 0
        print('hey')

        return make_resp(response_text, end_session, buttons)

    if text in help:
        response_text = 'для выхода из навыка скажи стоп, или название игры для того чтобы зайти в нее'
        status_list[user_id] = 0
        buttons = all_btns
        return make_resp(response_text, end_session, buttons)

    if 'что ты умеешь' in text:
        status_list[user_id] = 0
        response_text = 'У меня есть три игры для тебя: Первая - «Тройная чепуха», вторая - «Запрещённая буква», ' \
                        'третья - «Аббревиатура». Чтобы зайти в игру просто назови ее. Также ты всегда можешь ' \
                        'спросить у меня отперделение слов которые не знаешь и я попробую найти их в своем словарике '
        buttons = all_btns
        return make_resp(response_text, end_session, buttons)

    # main branch
    if status_list[user_id] == 0:
        if not text:
            response_text = intro
            buttons = all_btns

        elif text == 'правила каждой':
            response_text = rules
            buttons = all_btns

        elif text in abr_names:
            status_list[user_id] = 1
            response_text = abr_rules
            buttons = dec_btns

        elif text in zapr_names:
            status_list[user_id] = 2
            response_text = zapr_rules
            buttons = dec_btns

        elif text in troynaya_names:
            status_list[user_id] = 3
            response_text = troynaya_rules
            buttons = dec_btns

        elif text in disagree:
            response_text = 'Во что сыграем?'
            buttons = all_btns

        else:
            response_text = 'Я вас не поняла, повторите пожалуйста.'
            buttons = all_btns

        return make_resp(response_text, end_session, buttons)

    # pregame answer
    if status_list[user_id] in [1, 2, 3]:

        if status_list[user_id] == 1 and text in agree:
            response_text = 'Загадайте слово.'
            status_list[user_id] = 4
            buttons = []

        elif status_list[user_id] == 1 and text in disagree:
            response_text = 'Может в другую игру?'
            status_list[user_id] = 0
            buttons = all_btns


        elif status_list[user_id] == 2 and text in agree:
            response_text = 'Какую букву будем избегать?'
            status_list[user_id] = 5
            buttons = []

        elif status_list[user_id] == 2 and text in disagree:
            response_text = 'Может в другую игру?'
            status_list[user_id] = 0
            buttons = all_btns


        elif status_list[user_id] == 3 and text in agree:
            response_text = 'Загадайте букву.'
            status_list[user_id] = 6
            buttons = []

        elif status_list[user_id] == 3 and text in disagree:
            response_text = 'Может в другую игру?'
            status_list[user_id] = 0
            buttons = all_btns

        else:
            response_text = 'ошибка сервера, вас вернули в начало'
            buttons = all_btns
            status_list[user_id] = 0

        return make_resp(response_text, end_session, buttons)

    # games beg branch       
    if status_list[user_id] in [4, 5, 6]:

        if status_list[user_id] == 4:
            letter = text
            f = True
            for i in letter:
                if i not in alph: f = False
            if f:
                response_text = f'Я начинаю: {make_sentence(letter)}. Твоя очередь'
                status_list[user_id] = 7
            else:
                response_text = 'В слове есть буква на которую нет слов. Выбери другое слово'

        elif status_list[user_id] == 5:
            letter = text[-1]
            q = forb_let_questions[randint(0, len(forb_let_questions) - 1)]
            questions.append(q)
            response_text = f'Я начинаю: {q}'
            status_list[user_id] = 8

        elif status_list[user_id] == 6:
            letter = text[-1]
            if letter in alph:
                response_text = f'Я начинаю: {Gen_Three_Words(letter)}. Твоя очередь'
                status_list[user_id] = 9
            else:
                response_text = f'Я не знаю слов на букву: {letter}. Давай другую?'

        return make_resp(response_text, end_session, buttons)

    # gameplay branches
    if status_list[user_id] in [7, 8, 9]:

        if status_list[user_id] == 7:

            if check_sentence(text, letter):
                response_text = f'Интересно. Мой вариант: {make_sentence(letter)}. Твоя очередь'
            else:
                response_text = 'Не похоже на правильное предложение. Продолжим?'
                buttons = dec_btns
                status_list[user_id] = 10

        elif status_list[user_id] == 8:

            if counter < 10:

                if letter not in text:
                    q = forb_let_questions[randint(0, len(forb_let_questions) - 1)]
                    while q in questions: q = forb_let_questions[randint(0, len(forb_let_questions) - 1)]
                    questions.append(q)
                    response_text = str(q)
                    counter += 1
                else:
                    response_text = 'Упс... Видимо вы ощиблисью Хотите попробовать еще?'
                    buttons = dec_btns
                    counter = 0
                    questions = []
                    status_list[user_id] = 11

            elif counter == 10:
                response_text = 'Поздравляю вы молодец, говорите явно лучше меня. Хотите сыграть еще?'
                buttons = dec_btns
                counter = 0
                questions = []
                status_list[user_id] = 11


        elif status_list[user_id] == 9:

            if Check_Three_Words(text, letter):
                response_text = f'Интересно. Мой вариант: {Gen_Three_Words(letter)}. Твоя очередь'
            else:
                response_text = 'Не похоже на правильное предложение. Продолжим?'
                buttons = dec_btns
                status_list[user_id] = 12

        return make_resp(response_text, end_session, buttons)

    # lose branches
    if status_list[user_id] in [10, 11, 12]:

        if status_list[user_id] == 10:
            if text in disagree:
                status_list[user_id] = 0
                response_text = 'Во что сыграем?'
                buttons = all_btns

            elif text in agree:
                status_list[user_id] = 4
                response_text = 'Тогда продолжим. Загадай букву.'

            else:
                status_list[user_id] = 0
                response_text = 'я не понял, что вы сказали. И вышел из игры, мы можем начать заново или поиграить в другие игры'
                buttons = all_btns

        elif status_list[user_id] == 11:

            if text in disagree:
                status_list[user_id] = 0
                response_text = 'Во что сыграем?'
                buttons = all_btns

            elif text in agree:
                status_list[user_id] = 5
                response_text = 'Тогда продолжим. Загадай букву.'

            else:
                status_list[user_id] = 0
                response_text = 'я не понял, что вы сказали. И вышел из игры, мы можем начать заново или поиграить в другие игры'
                buttons = all_btns

        elif status_list[user_id] == 12:

            if text in disagree:
                status_list[user_id] = 0
                response_text = 'Во что сыграем?'
                buttons = all_btns

            elif text in agree:
                status_list[user_id] = 6
                response_text = 'Тогда продолжим. Загадай букву.'

            else:
                status_list[user_id] = 0
                response_text = 'я не понял, что вы сказали. И вышел из игры, мы можем начать заново или поиграить в другие игры'
                buttons = all_btns

        return make_resp(response_text, end_session, buttons)
    
    response_text = 'ошибка сервера'
    buttons == all_btns
    status_list[user_id] = 0
    
    return make_resp(response_text, end_session, buttons)


app.run(host='0.0.0.0', port=5000)
