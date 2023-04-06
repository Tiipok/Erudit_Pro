from flask import Flask, request
from dialogs import *
from random import randint, choice
from triple_nonsense import *
from Find_Definition import check
from abbreviation import *
import pymorphy2
import time

status_list = {}
letter_list = {}
counter_dict = {}
questions = {}
answers_dict = {} 

app = Flask(__name__)


def make_resp(response_text, end_session, buttons, audio='', text_to_say=''):
    if not text_to_say:
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
    
    # writing logs (kinda) - our resp 
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
    global counter_dict
    global answers_dict
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

    if user_id not in status_list.keys(): status_list[user_id] = 0
    if new: status_list[user_id] = 0

    # writing logs - user request
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
    if any(word in text for word in EXIT_phrases):
        response_text = 'До свидания! Закрываю навык.'
        end_session = True
        buttons = []
        status_list[user_id] = 0
        return make_resp(response_text, end_session, buttons)


    if text in BORED:
        response_text = 'Мы можем поиграть в одну из игр, которые я знаю. Чтобы узнать больше скажи: Правила всех '
        end_session = False
        buttons = all_btns
        status_list[user_id] = 0
        return make_resp(response_text, end_session, buttons)
    

    # find def in dict for user
    if any(word in text for word in FIND_phrases):
        if status_list[user_id] in [7, 8, 9]:
            buttons = dec_btns
            status_list[user_id] = status_list[user_id] + 3
            for sent in FIND_phrases:
                if sent in text:
                    try:
                        s = text.split()
                        word = s[s.index(sent.split()[-1]) + 1]
                        word = morph.parse(word)[0].normal_form
                        ans = check(word)
                        if ans is False:
                            response_text = 'Мне не удалось найти определение этого слова в толковом словаре Ожегова.\nПродолжим?'
                        else:
                            response_text = f"По толковому словарю Ожегова: {word} - {ans}.\nПродолжим?"
                    except IndexError:
                        response_text = 'Я вас не понял, перефразируйте вопрос или можем продолжть.'

        else:
            buttons = all_btns
            status_list[user_id] = 0
            for sent in FIND_phrases:
                if sent in text:
                    try:
                        s = text.split()
                        word = s[s.index(sent.split()[-1]) + 1]
                        word = morph.parse(word)[0].normal_form
                        ans = check(word)
                        if ans is False:
                            response_text = 'Мне не удалось найти определение этого слова в толковом словаре Ожегова.\nВо что будем играть?'
                        else:
                            response_text = f"По толковому словарю Ожегова: {word} - {ans}.\nВо что будем играть?"
                    except IndexError:
                        response_text = 'Я вас не понял, перефразируйте вопрос или можем начать игру'

        return make_resp(response_text, end_session, buttons)


    # help branch
    if any(word in text for word in HELP):
        response_text = 'для выхода из навыка скажи стоп, или название игры для того чтобы зайти в нее'
        status_list[user_id] = 0
        buttons = all_btns
        return make_resp(response_text, end_session, buttons)

    # abilities
    if any(word in text for word in abilities):
        status_list[user_id] = 0
        response_text = 'У меня есть три игры для тебя: Первая - «Тройная чепуха», вторая - «Запрещённая буква», ' \
                        'третья - «Аббревиатура». Чтобы зайти в игру просто назови ее. Также ты всегда можешь ' \
                        'спросить у меня определение слов, которые не знаешь, и я попробую найти их в своем словарике '
        buttons = all_btns
        return make_resp(response_text, end_session, buttons)


    # main branch
    match status_list[user_id]:

        case 0:
            if new:
                response_text = INTRO
                buttons = all_btns
                return make_resp(response_text, end_session, buttons, intro_sound, INTRO_to_say)
            
            elif any(word in text for word in ALL_names):
                response_text = ALL_rules
                buttons = all_btns
                return make_resp(response_text, end_session, buttons, text_to_say=ALL_rules_to_say)

            elif any(word in text for word in ABBREVIATION_names):
                status_list[user_id] = 1
                response_text = ABBREVIATION_rules
                buttons = dec_btns

            elif any(word in text for word in FORBIDEN_names):
                status_list[user_id] = 2
                response_text = FORBIDEN_rules
                buttons = dec_btns

            elif any(word in text for word in TRIPLE_names):
                status_list[user_id] = 3
                response_text = TRIPLE_rules
                buttons = dec_btns

            elif any(word in text for word in DISAGREE):
                response_text = 'Во что сыграем?'
                buttons = all_btns

            else:
                response_text = 'Я вас не понял, повторите пожалуйста название игры.'
                buttons = all_btns

            return make_resp(response_text, end_session, buttons)


        # pregame answer
        case 1 | 2 | 3:

            if any(word in text for word in AGREE):
                if status_list[user_id] == 1:
                    response_text = 'Загадайте слово.'
                    status_list[user_id] = 4

                elif status_list[user_id] == 2:
                    response_text = 'Какую букву будем избегать?'
                    status_list[user_id] = 5

                elif status_list[user_id] == 3:
                    response_text = 'Загадайте букву.'
                    status_list[user_id] = 6

            elif any(word in text for word in DISAGREE):
                buttons = all_btns
                response_text = 'Может в другую игру?'
                status_list[user_id] = 0

            else:
                response_text = 'Я вас не понял, во что будем играть?'
                buttons = all_btns
                status_list[user_id] = 0

            return make_resp(response_text, end_session, buttons)


        # games beg branch       
        case 4 | 5 | 6:
            
            answers_dict[user_id] = []

            match status_list[user_id]:

                case 4:
                    letter_list[user_id] = text
                    word = text
                    f = True
                    sent = make_sentence(word)
                    answers_dict[user_id].append(sent)

                    for i in word:
                        if i not in alph: f = False
                    if f:
                        response_text = f'Я начинаю: {sent}. Твоя очередь'
                        status_list[user_id] = 7

                    else:
                        response_text = 'В слове есть буква на которую нет слов. Выбери другое слово'

                case 5:
                    letter_list[user_id] = text[-1]
                    q = FORBIDEN_questions[randint(0, len(FORBIDEN_questions) - 1)]
                    questions[user_id] = [q]
                    response_text = f'Я начинаю: {q}'
                    status_list[user_id] = 8

                case 6:
                    letter_list[user_id] = text[-1]
                    letter = text[-1]
                    sent = Gen_Three_Words(letter)
                    answers_dict[user_id].append(sent)

                    if letter in alph:
                        response_text = f'Я начинаю: {sent}. Твоя очередь'
                        status_list[user_id] = 9
                        
                    else:
                        response_text = f'Я не знаю слов на букву: {letter}. Давай другую?'

            return make_resp(response_text, end_session, buttons)


        # gameplay branches
        case 7 | 8 | 9:

            sound = ''

            match status_list[user_id]:

            # abbreviation
                case 7:

                    word = letter_list[user_id]

                    if text not in answers_dict[user_id]:
                        
                        answers_dict[user_id].append(text)

                        if check_sentence(text, word):

                            sent = make_sentence(word)
                            answers_dict[user_id].append(sent)

                            PHRASES_list = ['Мне понравилось! Моя фраза:', 'У тебя отлично получается! Моя фраза:', 'Интересно. Мой вариант:',
                                             'Молодец! Теперь я:', 'Классно, теперь мой ход:', 'Здорово! Моя очередь:', 'Отлично! Идём дальше, моя очередь:',
                                                'Круто! Теперь я:', 'Замечательно! Моя очередь:' ]
                            response_text = f'{choice(PHRASES_list)} {sent}. Твоя очередь'
                            sound = correct_sound

                        else:
                            PHRASES_list = ['Не переживай.', 'Ничего страшного!']
                            response_text = f'Видимо ты ошибся. {choice(PHRASES_list)} Хочешь выберем другое слово?'
                            buttons = dec_btns
                            status_list[user_id] = 10
                            del letter_list[user_id]
                            sound = wrong_sound
                    else:
                        response_text = 'Не жульничай! Эта фраза уже была. Даю тебе ещё шанс.'


                # forbiden letter
                case 8:

                    if user_id not in counter_dict.keys(): counter_dict[user_id] = 0

                    counter = counter_dict[user_id]

                    if counter < 10:

                        letter = letter_list[user_id]
                        if text == '1': text = 'первое'
                        if text == '2': text = 'второе'
                        if text == '3': text = 'третье'


                        if letter not in text:
                            PHRASES_list = ['Вы прекрасно справляетесь. Следующий вопрос:',
                                            'У вас хорошо получается! Следующий вопрос:',
                                            'Так держать! Следующий вопрос:']
                            
                            q = FORBIDEN_questions[randint(0, len(FORBIDEN_questions) - 1)]
                            while q in questions[user_id]: q = FORBIDEN_questions[randint(0, len(FORBIDEN_questions) - 1)]
                            questions[user_id].append(q)
                            response_text = f'{choice(PHRASES_list)} {q}'
                            sound = correct_sound
                            counter_dict[user_id] += 1

                        else:
                            PHRASES_list = ['О, нет. Кажется, вы назвали запрещённую букву. Начнём с начала?',
                                            'Вы назвали запрещённую букву. Не расстраивайтесь. Начнём заново?',
                                            'Я услышал запрещённую букву. Вы проиграли. Давайте начнём с начала?' ]
                            
                            response_text = choice(PHRASES_list)
                            buttons = dec_btns
                            del counter_dict[user_id]
                            del questions[user_id]
                            status_list[user_id] = 11
                            sound = wrong_sound

                    elif counter == 10:

                        response_text = choice(['Поздравляю вы молодец, говорите явно лучше меня. Хотите сыграть еще?', 'Молодец, поздравляю с победой. Хотите сыграть еще?'])
                        buttons = dec_btns
                        del counter_dict[user_id]
                        del questions[user_id]
                        status_list[user_id] = 11
                        sound = correct_sound


                # triple nonsense
                case 9:

                    letter = letter_list[user_id]
                    
                    if text not in answers_dict[user_id]:

                        answers_dict[user_id].append(text)

                        if Check_Three_Words(text, letter):

                            sent = Gen_Three_Words(letter)
                            answers_dict[user_id].append(sent)

                            PHRASES_list = ['Мне понравилось! Моя фраза:', 'У тебя отлично получается! Моя фраза:', 'Интересно. Мой вариант:',
                                             'Молодец! Теперь я:', 'Классно, теперь мой ход:', 'Здорово! Моя очередь:', 'Отлично! Идём дальше, моя очередь:',
                                                'Круто! Теперь я:', 'Замечательно! Моя очередь:' ]

                            response_text = f'{choice(PHRASES_list)} {sent}. Твоя очередь'
                            sound = correct_sound

                        else:
                            PHRASES_list = ['Не переживай.', 'Ничего страшного!']
                            response_text = f'Видимо ты ошибся. {choice(PHRASES_list)} Хочешь выберем другую букву?'
                            buttons = dec_btns
                            status_list[user_id] = 12
                            del letter_list[user_id]
                            sound = wrong_sound

                    else:
                        response_text = 'Не жульничай! Эта фраза уже была. Даю тебе еще шанс.'

            return make_resp(response_text, end_session, buttons, sound)

        # lose branches
        case 10 | 11 | 12:

            answers_dict[user_id] = []

            if any(word in text for word in DISAGREE):
                status_list[user_id] = 0
                response_text = 'Во что сыграем?'
                buttons = all_btns

            elif any(word in text for word in AGREE):
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
                response_text = 'я не понял, что вы сказали. И вышел из игры, мы можем начать заново или поиграть в другие игры. Для продолжения произнесите название игры в которую вы хотите сыграть.'
                buttons = all_btns

    
            return make_resp(response_text, end_session, buttons)
    
    response_text = 'я не понял, что вы сказали. И вышел из игры, мы можем начать заново или поиграть в другие игры. Для продолжения произнесите название игры в которую вы хотите сыграть.'
    buttons = all_btns
    status_list[user_id] = 0

    return make_resp(response_text, end_session, buttons)


if __name__ == '__main__':
    morph = pymorphy2.MorphAnalyzer(lang='ru')
    app.run(host='0.0.0.0', port=5000)
