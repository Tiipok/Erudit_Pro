from flask import Flask, request
from dialogs import *
from random import randint
from triple_nonsense import *
from Find_Definition import check
from abbreviation import *
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
app = Flask(__name__)

status = 0
letter = ''
counter = 0
questions = []

def make_resp(response_text, end_session, buttons):
    global status
    resp = {
        'response': {
            'text': response_text,
            'end_session ': end_session,
            'buttons': buttons
        },
        'version': '1.0'
    }
    print(resp)
    print(status)
    return resp


@app.route('/', methods=['POST'])
def response():
    end_session = False
    global status
    global letter
    global questions
    global counter

    all_btns = [{'title': 'Правила каждой', 'hide': False},
                       {'title': 'Тройная чепуха', 'hide': False},
                       {'title': 'Запрещённая буква', 'hide': False},
                       {'title': 'Аббревиатура', 'hide': False}, ]
    dec_btns = [{'title': 'Я согласен', 'hide': False},
                        {'title': 'Не хочу', 'hide': False}, ]

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
        return make_resp(response_text, end_session, buttons)
                
    # users bored phrases               
    if text in bored:
        response_text = 'Ну и чем займеся? Поиграем в другие игры или может помолчим?'
        buttons = all_btns
        status = 0
        return make_resp(response_text, end_session, buttons)

    # find def in dict for user    
    if 'что значит' in text:
        s = text.split()
        response_text = f'По толковому словарю Ожигова: {check(s[s.index("значит")+1])}. \nВо что будем играть дальше?'
        buttons = all_btns
        status = 0
        print('hey')

        return make_resp(response_text, end_session, buttons)
    
    if text == 'помощь':
        response_text = 'для выхода из навыка скажи стоп, или название игры для того чтобы зайти в нее'
        status = 0
        buttons = all_btns
        return make_resp(response_text, end_session, buttons)

    if 'что ты умеешь' in text:
        status = 0
        response_text = 'У меня есть три игры для тебя: Первая - «Тройная чепуха», вторая - «Запрещённая буква», третья - «Аббревиатура». Чтобы зайти в игру просто назови ее. Также ты всегда можешь спросить у меня отперделение слов которые не знаешь и я попробую найти их в своем словарике'
        buttons = all_btns
        return  make_resp(response_text, end_session, buttons)

    # main branch
    if status == 0:
        if not text:
            response_text = intro 
            buttons = all_btns

        elif text == 'правила каждой':
            response_text = rules
            buttons = all_btns

        elif text == 'аббревиатура':
            status = 1
            response_text = abr_rules
            buttons = dec_btns

        elif text == 'запрещённая буква':
            status = 2
            response_text = zapr_rules
            buttons = dec_btns

        elif text == 'тройная чепуха':
            status = 3
            response_text = troynaya_rules
            buttons = dec_btns

        else:
            response_text = 'Я вас не поняла, повторите пожалуйста.'
            buttons = all_btns
            
        return make_resp(response_text, end_session, buttons)
        
    # pregame answer
    if status in [1, 2, 3]:

        if status == 1 and text in agree:
            response_text = 'Загадайте слово.'
            status = 4
            buttons = []

        elif status == 1 and text in disagree:
            response_text = 'Может в другую игру?'
            status = 0
            buttons = all_btns


        elif status == 2 and text in agree:
            response_text = 'Какую букву будем избегать?'
            status = 5
            buttons = []

        elif status == 2 and text in disagree:
            response_text = 'Может в другую игру?'
            status = 0
            buttons = all_btns


        elif status == 3 and text in agree:
            response_text = 'Загадайте букву.'
            status = 6
            buttons = []

        elif status == 3 and text in disagree:
            response_text = 'Может в другую игру?'
            status = 0
            buttons = all_btns

        else:
            response_text = 'err'
        
        return make_resp(response_text, end_session, buttons)
    
    # games beg branch       
    if status in [4, 5, 6]:

            letter = text

            if status == 4:
                f = True
                for i in letter:
                    if i not in alph: f = False
                if f:
                    response_text = f'Я начинаю: {make_sentence(letter)}. Твоя очередь'
                    status = 7
                else:
                    response_text= 'В слове есть буква на которую нет слов. Выбери другое слово'
                
            elif status == 5:
                q = forb_let_questions[randint(0,len(forb_let_questions)-1)]
                questions.append(q)
                response_text = f'Я начинаю: {q}'
                status = 8

            elif status == 6:
                if letter in alph:
                    response_text = f'Я начинаю: {Gen_Three_Words(letter)}. Твоя очередь'
                    status = 9
                else:
                    response_text = 'Я не знаю слов на эту букву. Давай другую?'

            return make_resp(response_text, end_session, buttons)
    
    # gameplay branches
    if status in [7, 8, 9]:
        if status == 7:
            if check_sentence(text, letter):
                response_text = f'Интересно. Мой вариант: {make_sentence(letter)}. Твоя очередь'
            else:
                response_text = 'Не похоже на правильное предложение. Продолжим?'
                buttons = dec_btns
                status = 10

        elif status == 8:

            if counter < 10:
                if letter not in text:
                    q = forb_let_questions[randint(0,len(forb_let_questions)-1)]
                    while q in text: q = forb_let_questions[randint(0,len(forb_let_questions)-1)]
                    response_text = str(q)
                    counter += 1
                else:
                    response_text = 'Упс... Видимо вы ощиблисью Хотите попробовать еще?'
                    buttons = dec_btns
                    counter = 0
                    questions = []
                    status = 11

            elif counter == 10:
                response_text = 'Поздравляю вы молодец, говорите явно лучше меня. Хотите сыграть еще?'
                buttons = dec_btns
                counter = 0
                questions = []
                status = 11


        elif status == 9:
            if Check_Three_Words(text, letter):
                    response_text = f'Интересно. Мой вариант: {Gen_Three_Words(letter)}. Твоя очередь'
            else:
                response_text = 'Не похоже на правильное предложение. Продолжим?'
                buttons = dec_btns
                status = 12

        return make_resp(response_text, end_session, buttons)

    # lose branches
    if status in [10, 11, 12]:
        if status == 10:   
            if text in disagree:
                status = 0
                response_text = 'Во что сыграем?'
                buttons = all_btns

            elif text in agree:
                status = 4
                response_text = 'Тогда продолжим. Загадай букву.'
            
            else:
                status = 0
                response_text = 'я не понял, что вы сказали. И вышел из игры, мы можем начать заново или поиграить в другие игры'
                buttons = all_btns
                
        elif status == 11:
            if text in disagree:
                status = 0
                response_text = 'Во что сыграем?'
                buttons = all_btns

            elif text in agree:
                status = 5
                response_text = 'Тогда продолжим. Загадай букву.'
            
            else:
                status = 0
                response_text = 'я не понял, что вы сказали. И вышел из игры, мы можем начать заново или поиграить в другие игры'
                buttons = all_btns

        elif status == 12:
            if text in disagree:
                status = 0
                response_text = 'Во что сыграем?'
                buttons = all_btns

            elif text in agree:
                status = 6
                response_text = 'Тогда продолжим. Загадай букву.'
            
            else:
                status = 0
                response_text = 'я не понял, что вы сказали. И вышел из игры, мы можем начать заново или поиграить в другие игры'
                buttons = all_btns   
        return make_resp(response_text, end_session, buttons)
    


app.run(host='0.0.0.0', port=5000,  ssl_context='adhoc')
