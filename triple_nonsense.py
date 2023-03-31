import csv
from random import choice
from referens import alph, numeration


def Gen_Three_Words(letter):
    with open("Dict.csv", 'r', encoding="utf8") as file:
        csvreader = csv.reader(file)
        lines = list(csvreader)
        letter = letter.lower()

        if letter == 'ё': letter = 'е'
        if letter not in alph: return f'Я не нашел слов на букву: {letter}'

        a = numeration[alph[letter]]

        first = choice(lines[a[0] : a[1]])[0]

        second = choice(lines[a[0] : a[1]])[0]
        while second == first: second = choice(lines[a[0] : a[1]])[0]

        third = choice(lines[a[0] : a[1]])[0]
        while third == second: third = choice(lines[a[0] : a[1]])[0]
        for k in ('!', '?', '.'): #new filter
            first = first.strip(k)
            second = second.strip(k)
            third = third.strip(k)
        return ' '.join(x for x in [first, second, third])

def Check_Three_Words(sent, letter):
    flag = True
    if len(sent.split())!=3:flag = False
    for i in sent.split():
        if i[0] != letter: flag = False
    
    return flag

