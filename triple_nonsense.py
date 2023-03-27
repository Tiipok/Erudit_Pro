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
        
        return ' '.join(x for x in [first, second, third])
<<<<<<< HEAD

print(Gen_Three_Words('а'))
=======
>>>>>>> bdc22b16badc55fdf50a876579f1756bf68960a9
