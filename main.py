from flask import Flask, request
from dialogs import *
from random import randint
from TroyChepuha import *
from Find_Definition import check
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
app = Flask(__name__)

status = 0

@app.route('/', methods=['POST'])
def response():
    end_session = False
    global status

    text = request.json.get('request', ()).get('command')
    text = text.lower()

    response_text = ''
    buttons = []

    # checking if user wants to exit
    if text in exit_phrases:
        response_text = 'До свидания! Закрываю навык.'
        end_session = True
        buttons = []
        status = -1

    # games branch
    if status in [4, 5, 6]:

        if status == 4:
            pass

        elif status == 5:
            pass

        elif status == 6:
            pass

    # pregame answer
    if status in [1, 2, 3]:

        if status == 1 and text in agree:
            response_text = 'Начинаем! Загадайте букву.'
            status = 4
            buttons = []

        elif status == 1 and text in disagree:
            response_text = 'Может в другую игру?'
            status = 0
            buttons = [{'title': 'Правила каждой', 'hide': False},
                       {'title': 'Тройная чепуха', 'hide': False},
                       {'title': 'Запрещённая буква', 'hide': False},
                       {'title': 'Аббревиатура', 'hide': False}, ]


        elif status == 2 and text in agree:
            response_text = 'Какую букву будем избегать?'
            status = 5
            buttons = []

        elif status == 2 and text in disagree:
            response_text = 'Может в другую игру?'
            status = 0
            buttons = [{'title': 'Правила каждой', 'hide': False},
                       {'title': 'Тройная чепуха', 'hide': False},
                       {'title': 'Запрещённая буква', 'hide': False},
                       {'title': 'Аббревиатура', 'hide': False}, ]


        elif status == 3 and text in agree:
            response_text = 'Начинаем! Загадайте слово.'
            status = 6
            buttons = []

        elif status == 3 and text in disagree:
            response_text = 'Может в другую игру?'
            status = 0
            buttons = [{'title': 'Правила каждой', 'hide': False},
                       {'title': 'Тройная чепуха', 'hide': False},
                       {'title': 'Запрещённая буква', 'hide': False},
                       {'title': 'Аббревиатура', 'hide': False}, ]

        else:
            response_text = 'Прости я тебя не понял. Если хочешь сыграть скажи "Я согласен", если нет то "Не хочу"'
            buttons = [{'title': 'Я согласен', 'hide': False},
                       {'title': 'Не хочу', 'hide': False}, ]

    # main branch
    if status == 0:
        if not text:
            response_text = intro  # from dialogs
            buttons = [{'title': 'Правила каждой', 'hide': False},
                       {'title': 'Тройная чепуха', 'hide': False},
                       {'title': 'Запрещённая буква', 'hide': False},
                       {'title': 'Аббревиатура', 'hide': False}, ]

        elif text == 'правила каждой':
            response_text = rules
            buttons = [{'title': 'Правила каждой', 'hide': False},
                       {'title': 'Тройная чепуха', 'hide': False},
                       {'title': 'Запрещённая буква', 'hide': False},
                       {'title': 'Аббревиатура', 'hide': False}, ]

        elif text == 'аббревиатура':
            status = 1
            response_text = abr_rules
            buttons = [{'title': 'Я согласен', 'hide': False},
                       {'title': 'Не хочу', 'hide': False}, ]

        elif text == 'запрещённая буква':
            status = 2
            response_text = zapr_rules
            buttons = [{'title': 'Я согласен', 'hide': False},
                       {'title': 'Не хочу', 'hide': False}, ]

        elif text == 'тройная чепуха':
            status = 3
            response_text = troynaya_rules
            buttons = [{'title': 'Я согласен', 'hide': False},
                       {'title': 'Не хочу', 'hide': False}, ]

        else:
            response_text = 'Я вас не поняла, повторите пожалуйста.'
            buttons = [{'title': 'Правила каждой', 'hide': False},
                       {'title': 'Тройная чепуха', 'hide': False},
                       {'title': 'Запрещённая буква', 'hide': False},
                       {'title': 'Аббревиатура', 'hide': False}, ]

    resp = {
        'response': {
            'text': response_text,
            'end_session ': end_session,
            'buttons': buttons
        },
        'version': '1.0'
    }
    print(request.json)
    print(status)
    print(text)

    return resp


app.run(host='0.0.0.0', port=5000, debug=True)
