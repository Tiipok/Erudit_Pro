import csv
from random import randint
from referens import alph, numeration

def gen_three_words(letter):
    l = numeration
    with open("Dict.csv", 'r', encoding="utf8") as file:
        csvreader = csv.reader(file)
        lines = list(csvreader)

        a = l[alph[letter]]

        first = randint(a[0], a[1])

        second = randint(a[0], a[1])
        while second == first:
            second = randint(a[0], a[1])

        third = randint(a[0], a[1])
        while third == second:
            third = randint(a[0], a[1])

        first = lines[first][0]
        second = lines[second][0]
        third = lines[third][0]

        print(first, second, third)

        return [first, second, third]

