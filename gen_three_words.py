import csv
from random import randint
from referens import alph, numeration


def gen_three_words(letter):
    with open("Dict.csv", 'r', encoding="utf8") as file:
        csvreader = csv.reader(file)
        lines = list(csvreader)
        letter = letter.lower()
        if letter == 'ё': letter = 'е'
        if letter not in alph: return f'Я не нашел слов на букву: {letter}'
        a = numeration[alph[letter]]

        first = randint(a[0], a[1])

        second = randint(a[0], a[1])
        while second == first: second = randint(a[0], a[1])

        third = randint(a[0], a[1])
        while third == second: third = randint(a[0], a[1])

        first = lines[first][0]
        second = lines[second][0]
        third = lines[third][0]

        return [first, second, third]

print(gen_three_words('Б'))