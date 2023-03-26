from flask import Flask, request
from dialogs import *
from random import randint

app = Flask(__name__)

in_game = 0  # 0 - no game, 1 4 - troynaya chepuha, 2 5 - zapresh buk, 3 6 - abbrev


@app.route('/', methods=['POST'])
def resp():
    global in_game
    end_session = False
    buttons = []

    text = request.json.get('request', ()).get('command')
    response_text = ''

    if in_game > 3:  # gaming
        for word in exit_phrases:
            if word in text:
                in_game = 0
                print('exit game')

        if in_game == 4:
            response_text = str(randint(0, 10))
            print(4)

        if in_game == 5:
            response_text = str(randint(0, 10))
            print(5)

        if in_game == 6:
            response_text = str(randint(0, 10))
            print(6)

    if in_game < 4:
        if in_game > 0:
            if in_game == 1 and text in agree:  # entering and exiting games
                response_text = 'Начинаем! Загадайте букву.'
                in_game = 4
            elif in_game == 1 and text in disagree:
                response_text = 'Хорошо! Закрываю навык "Эрудит".'
                end_session = True

            elif in_game == 2 and text in agree:
                response_text = 'Какую букву будем избегать?'
                in_game = 5
            elif in_game == 2 and text in disagree:
                response_text = 'Хорошо! Закрываю навык "Эрудит".'
                end_session = True

            elif in_game == 3 and text in agree:
                response_text = 'Начинаем! Загадайте слово.'
                in_game = 6
            elif in_game == 3 and text in disagree:
                response_text = 'Хорошо! Закрываю навык "Эрудит".'
                end_session = True

            else:
                in_game = 0

        if in_game == 0:
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
                in_game = 3
                response_text = abr_rules
                buttons = [{'title': 'Я согласен', 'hide': False},
                           {'title': 'Не хочу', 'hide': False}, ]

            elif text == 'запрещённая буква':
                in_game = 2
                response_text = zapr_rules
                buttons = [{'title': 'Я согласен', 'hide': False},
                           {'title': 'Не хочу', 'hide': False}, ]

            elif text == 'тройная чепуха':
                in_game = 1
                response_text = troynaya_rules
                buttons = [{'title': 'Я согласен', 'hide': False},
                           {'title': 'Не хочу', 'hide': False}, ]
            else:
                response_text = 'Я вас не поняла, повторите пожалуйста.'
                buttons = [{'title': 'Правила каждой', 'hide': False},
                           {'title': 'Тройная чепуха', 'hide': False},
                           {'title': 'Запрещённая буква', 'hide': False},
                           {'title': 'Аббревиатура', 'hide': False}, ]

    if text in exit_phrases:
        response_text = 'До свидания!'
        end_session = True
        buttons = []

    response = {
        'response': {
            'text': response_text,
            'end_session ': end_session,
            'buttons': buttons
        },
        'version': '1.0'
    }

    print(request.json)
    print(text)
    print('status', in_game)

    return response


app.run(host='0.0.0.0', port=5000, debug=True)
