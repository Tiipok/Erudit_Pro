from flask import Flask, request
from dialogs import *
from random import randint
from triple_nonsense import *
from Find_Definition import check
from abbreviation import *
import pymorphy2
import time

status_list = {}
letter_list = {}
counter = 0
questions = {}

app = Flask(__name__)


def make_resp(response_text, end_session, buttons, audio=''):

    text_to_say = response_text.replace('\n', ' ')
    resp = {
        'response': {
            'text': response_text,
            'tts': f'{audio, text_to_say}',
            'end_session ': end_session,
            'buttons': buttons
        },
        'version': '1.0'
    }
    
    # writing logs
    print(resp['response']['text'])
    with open('logs.txt', 'a', encoding="utf8") as f:
        f.write(f'Filia: {resp["response"]["text"]}')
        f.write('\n\n\n')
    print(' ')

    return resp


@app.route('/', methods=['POST'])
def response():
    # variables for response and working
    global status_list
    global letter_list
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

    for k in ('!', '?', '.', ':'):
        text = text.replace(k, ' ')
    text = text.replace('ё', 'е')
    text = text.strip()

    # getting user's id
    user_id = request.json.get('session', ()).get('user_id')
    new = request.json.get('session', ()).get('new')

    if user_id not in status_list: status_list[user_id] = 0
    if new: status_list[user_id] = 0

    # writing logs
    print(text)
    print(f'status: {status_list[user_id]}    user id: {user_id}')
    with open('logs.txt', 'a', encoding="utf8") as f:
        f.write(time.ctime())
        f.write('\n')
        f.write(f'status: {status_list[user_id]}    user id: {user_id}')
        f.write('\n\n')
        f.write(f'user: {text}')
        f.write('\n\n')

    # checking if user wants to exit
    if text in EXIT_phrases:
        response_text = 'До свидания! Закрываю навык.'
        end_session = True
        buttons = []
        status_list[user_id] = 0
        return make_resp(response_text, end_session, buttons)

    # find def in dict for user
    if any(word in text for word in FIND_phrases):

        buttons = all_btns
        status_list[user_id] = 0
        for sent in FIND_phrases:
            if sent in text:
                s = text.split()
                word = s[s.index(sent.split()[-1]) + 1]
                word = morph.parse(word)[0].normal_form
                ans = check(word)
                if not ans:
                    response_text = f"По толковому словарю Ожегова: {s[s.index(sent.split()[-1]) + 1]} - {ans}.\nВо что будем играть?"
                else: response_text = 'Мне не удалось найти определение этого слова в толковом словаре Ожегова.\nВо что будем играть?'

        return make_resp(response_text, end_session, buttons)

    # help branch
    if text in HELP:
        response_text = 'для выхода из навыка скажи стоп, или название игры для того чтобы зайти в нее'
        status_list[user_id] = 0
        buttons = all_btns
        return make_resp(response_text, end_session, buttons)

    if 'что ты умеешь' in text:
        status_list[user_id] = 0
        response_text = 'У меня есть три игры для тебя: Первая - «Тройная чепуха», вторая - «Запрещённая буква», ' \
                        'третья - «Аббревиатура». Чтобы зайти в игру просто назови ее. Также ты всегда можешь ' \
                        'спросить у меня определение слов которые не знаешь и я попробую найти их в своем словарике '
        buttons = all_btns
        return make_resp(response_text, end_session, buttons)

    # main branch
    if status_list[user_id] == 0:
        if not text:
            response_text = INTRO
            buttons = all_btns

        elif text in ALL_names:
            response_text = ALL_rules
            buttons = all_btns

        elif text in ABBREVIATION_names:
            status_list[user_id] = 1
            response_text = ABBREVIATION_rules
            buttons = dec_btns

        elif text in FORBIDEN_names:
            status_list[user_id] = 2
            response_text = FORBIDEN_rules
            buttons = dec_btns

        elif text in TRIPLE_names:
            status_list[user_id] = 3
            response_text = TRIPLE_rules
            buttons = dec_btns

        elif text in DISAGREE:
            response_text = 'Во что сыграем?'
            buttons = all_btns

        else:
            response_text = 'Я вас не понял, повторите пожалуйста.'
            buttons = all_btns

        return make_resp(response_text, end_session, buttons)

    # pregame answer
    if status_list[user_id] in [1, 2, 3]:

        if text in AGREE:
            if status_list[user_id] == 1:
                response_text = 'Загадайте слово.'
                status_list[user_id] = 4

            elif status_list[user_id] == 2:
                response_text = 'Какую букву будем избегать?'
                status_list[user_id] = 5

            elif status_list[user_id] == 3:
                response_text = 'Загадайте букву.'
                status_list[user_id] = 6

        elif text in DISAGREE:
            buttons = all_btns
            response_text = 'Может в другую игру?'
            status_list[user_id] = 0

        else:
            response_text = 'Я вас не понял, во что будем играть?'
            buttons = all_btns
            status_list[user_id] = 0

        return make_resp(response_text, end_session, buttons)

    # games beg branch       
    if status_list[user_id] in [4, 5, 6]:

        if status_list[user_id] == 4:

            letter_list[user_id] = text
            word = text
            f = True

            for i in word:
                if i not in alph: f = False
            if f:
                response_text = f'Я начинаю: {make_sentence(word)}. Твоя очередь'
                status_list[user_id] = 7
            else:
                response_text = 'В слове есть буква на которую нет слов. Выбери другое слово'

        elif status_list[user_id] == 5:

            letter_list[user_id] = text[-1]
            q = FORBIDEN_questions[randint(0, len(FORBIDEN_questions) - 1)]
            questions[user_id] = [q]
            response_text = f'Я начинаю: {q}'
            status_list[user_id] = 8

        elif status_list[user_id] == 6:

            letter_list[user_id] = text[-1]
            letter = text[-1]
            if letter in alph:
                response_text = f'Я начинаю: {Gen_Three_Words(letter)}. Твоя очередь'
                status_list[user_id] = 9
            else:
                response_text = f'Я не знаю слов на букву: {letter}. Давай другую?'

        return make_resp(response_text, end_session, buttons)

    # gameplay branches
    if status_list[user_id] in [7, 8, 9]:
        sound = ''

        if status_list[user_id] == 7:

            word = letter_list[user_id]

            if check_sentence(text, word):
                response_text = f'Интересно. Мой вариант: {make_sentence(word)}. Твоя очередь'
                sound = correct_sound
            else:
                response_text = 'Не похоже на правильное предложение. Продолжим?'
                buttons = dec_btns
                status_list[user_id] = 10
                sound = wrong_sound


        elif status_list[user_id] == 8:

            if counter < 10:

                letter = letter_list[user_id]
                if letter not in text:
                    q = FORBIDEN_questions[randint(0, len(FORBIDEN_questions) - 1)]
                    while q in questions[user_id]: q = FORBIDEN_questions[randint(0, len(FORBIDEN_questions) - 1)]
                    questions[user_id].append(q)
                    response_text = str(q)
                    sound = correct_sound
                    counter += 1

                else:
                    response_text = 'Упс... Видимо вы ошиблись. Хотите попробовать еще?'
                    buttons = dec_btns
                    counter = 0
                    questions[user_id] = []
                    status_list[user_id] = 11
                    sound = wrong_sound

            elif counter == 10:

                response_text = 'Поздравляю вы молодец, говорите явно лучше меня. Хотите сыграть еще?'
                buttons = dec_btns
                counter = 0
                questions[user_id] = []
                status_list[user_id] = 11
                sound = correct_sound


        elif status_list[user_id] == 9:

            letter = letter_list[user_id]

            if Check_Three_Words(text, letter):
                response_text = f'Интересно. Мой вариант: {Gen_Three_Words(letter)}. Твоя очередь'
                sound = correct_sound
            else:
                response_text = 'Не похоже на правильное предложение. Продолжим?'
                buttons = dec_btns
                status_list[user_id] = 12
                sound = wrong_sound

        return make_resp(response_text, end_session, buttons, sound)

    # lose branches
    if status_list[user_id] in [10, 11, 12]:

        if text in DISAGREE:
            status_list[user_id] = 0
            response_text = 'Во что сыграем?'
            buttons = all_btns

        elif text in AGREE:
            if status_list[user_id] == 10:
                status_list[user_id] = 4
                response_text = 'Тогда продолжим. Загадай слово.'

            elif status_list[user_id] == 11:
                status_list[user_id] = 5
                response_text = 'Тогда продолжим. Загадай букву.'

            elif status_list[user_id] == 12:
                status_list[user_id] = 6
                response_text = 'Тогда продолжим. Загадай букву.'

        else:
            status_list[user_id] = 0
            response_text = 'я не понял, что вы сказали. И вышел из игры, мы можем начать заново или поиграть в другие игры'
            buttons = all_btns

        return make_resp(response_text, end_session, buttons)

    response_text = 'я не понял, что вы сказали. И вышел из игры, мы можем начать заново или поиграть в другие игры'
    buttons = all_btns
    status_list[user_id] = 0

    return make_resp(response_text, end_session, buttons)


if __name__ == '__main__':
    morph = pymorphy2.MorphAnalyzer()
    app.run(host='0.0.0.0', port=5000)
