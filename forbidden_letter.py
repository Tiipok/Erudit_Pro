import random
from referens import *

global user_ans
i = 0
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

        if i == 2:
            if forb_let not in user_ans:
                response_text = f'{forb_let_questions[i]}'
                user_ans = input()

        if i == 3:
            if forb_let in user_ans:
                response_text = f'{forb_let_questions[i]}'
                user_ans = input()

        if i == 4:
            if forb_let in user_ans:
                response_text = f'{forb_let_questions[i]}'
                user_ans = input()