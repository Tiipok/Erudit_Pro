import random
from referens import *
from dialogs import *

global user_ans
i = 0
j = 0
forb_let = input()
if forb_let.lower() in alphabet:
    if status in game:
        if i == 0:
            response_text = f'{forb_let_questions[i]}'
            user_ans = input()

        if i == 1:
            if forb_let not in user_ans:
                response_text = f'{forb_let_questions[i]}'
                user_ans = input()
            else:
                response_text = 'О, нет. Кажется, вы назвали запрещённую букву. Начнём с начала?'
                j += 1

        if i == 2:
            if forb_let not in user_ans:
                response_text = f'{forb_let_questions[i]}'
                user_ans = input()
            else:
                response_text = 'О, нет. Кажется, вы назвали запрещённую букву. Начнём с начала?'
                j += 1

        if i == 3:
            if forb_let in user_ans:
                response_text = f'{forb_let_questions[i]}'
                user_ans = input()
            else:
                response_text = 'О, нет. Кажется, вы назвали запрещённую букву. Начнём с начала?'
                j += 1

        if i == 4:
            if forb_let in user_ans:
                response_text = f'{forb_let_questions[i]}'
                user_ans = input()
            else:
                response_text = 'О, нет. Кажется, вы назвали запрещённую букву. Начнём с начала?'
                j += 1

        if i == 5:
            if forb_let in user_ans:
                response_text = f'{forb_let_questions[i]}'
                user_ans = input()
            else:
                response_text = 'О, нет. Кажется, вы назвали запрещённую букву. Начнём с начала?'
                j += 1

        if i == 6:
            if forb_let in user_ans:
                response_text = f'{forb_let_questions[i]}'
                user_ans = input()
            else:
                response_text = 'О, нет. Кажется, вы назвали запрещённую букву. Начнём с начала?'
                j += 1

        if i == 7:
            if forb_let in user_ans:
                response_text = f'{forb_let_questions[i]}'
                user_ans = input()
            else:
                response_text = 'О, нет. Кажется, вы назвали запрещённую букву. Начнём с начала?'
                j += 1

        if i == 8:
            if forb_let in user_ans:
                response_text = f'{forb_let_questions[i]}'
                user_ans = input()
            else:
                response_text = 'О, нет. Кажется, вы назвали запрещённую букву. Начнём с начала?'
                j += 1

        if i == 9:
            if forb_let in user_ans:
                response_text = f'{forb_let_questions[i]}'
                user_ans = input()
            else:
                response_text = 'О, нет. Кажется, вы назвали запрещённую букву. Начнём с начала?'
                j += 1

        if i == 10:
            if forb_let in user_ans:
                response_text = f'{forb_let_questions[i]}'
                user_ans = input()
            else:
                response_text = 'О, нет. Кажется, вы назвали запрещённую букву. Начнём с начала?'
                j += 1

        if i == 11:
            if forb_let in user_ans:
                response_text = f'{forb_let_questions[i]}'
                user_ans = input()
            else:
                response_text = 'О, нет. Кажется, вы назвали запрещённую букву. Начнём с начала?'
                j += 1

        if i == 12:
            if forb_let in user_ans:
                response_text = f'{forb_let_questions[i]}'
                user_ans = input()
            else:
                response_text = 'О, нет. Кажется, вы назвали запрещённую букву. Начнём с начала?'
                j += 1

        if i == 13:
            if forb_let in user_ans:
                response_text = f'{forb_let_questions[i]}'
                user_ans = input()
            else:
                response_text = 'О, нет. Кажется, вы назвали запрещённую букву. Начнём с начала?'
                j += 1

        if i == 14:
            if forb_let in user_ans and j == 0:
               response_text = 'Поздравляю! Вы победили.'
            else:
                response_text = 'О, нет. Кажется, вы назвали запрещённую букву. Начнём с начала?'
                j += 1


        i += 1