import random
from dialogs import *

forb_let = input()
if forb_let.lower() in alph:
    response_text = f'Хорошо. Я задаю вам вопросы, вы отвечаете на них быстро, не называя букву "{forb_let.upper()}". Готовы?'
    if text in agree:
        response_text = f'{forb_let_questions[0]}'
        user_ans = input()
        if forb_let in user_ans:
            response_text = 'О, нет. Кажется, вы назвали запрещённую букву. Начнём с начала?'
            if text in agree or disagree:
                in_game = 1
            else:
                in_game = 0
        else:
            response_text = f'Вы хорошо справляетесь. {forb_let_questions[1]}'
            user_ans = input()
            if forb_let in user_ans:
                response_text = 'О, нет. Кажется, вы назвали запрещённую букву. Начнём с начала?'
                if text in agree or disagree:
                    in_game = 1
                else:
                    in_game = 0
            else:
                response_text = f'У вас отлично получается. {forb_let_questions[2]}'
                user_ans = input()
                if forb_let in user_ans:
                    response_text = 'О, нет. Кажется, вы назвали запрещённую букву. Начнём с начала?'
                    if text in agree or disagree:
                        in_game = 1
                    else:
                        in_game = 0
                else:
                    response_text = f'Вы отличный игрок. {forb_let_questions[3]}'
                    user_ans = input()
                    if forb_let in user_ans:
                        response_text = 'О, нет. Кажется, вы назвали запрещённую букву. Начнём с начала?'
                        if text in agree or disagree:
                            in_game = 1
                        else:
                            in_game = 0
                    else:
                        response_text = f'Хорошая работа. {forb_let_questions[4]}'
                        user_ans = input()
                        if forb_let in user_ans:
                            response_text = 'О, нет. Кажется, вы назвали запрещённую букву. Начнём с начала?'
                            if text in agree or disagree:
                                in_game = 1
                            else:
                                in_game = 0
                        else:
                            response_text = 'Вы победили! Начнём с начала?'
                            if text in agree or disagree:
                                in_game = 1
                            else:
                                in_game = 0
    elif text in disagree:
        in_game = 1
    else:
        in_game = 0
else:
    response_text = 'В русском алфавите нет такой буквы.'
