from random import choice
from referens import alph, numeration #{'a': 1, ...}, [[beg, end], ...]
import csv
def make_sentence(sls):

    with open("Dict.csv", 'r', encoding="utf8") as file:
        csvreader = csv.reader(file)
        lines = list(csvreader)

    ans = []
    for i in range(len(sls)): #reconstruction
        letter = sls[i]
        letter = letter.lower()
        if letter == 'ё': letter = 'е'
        if letter not in alph: return f'Я не нашел слов на букву: {letter}'
        a = numeration[alph[letter]]

        out_word = choice(lines[a[0] : a[1]])[0]
        if out_word in ans:
            limit = 0
            while out_word in ans:
                out_word = choice(lines[a[0] : a[1]])[0]
                limit += 1
                if limit == 1000: return 'Слишком много символов'

        for k in ('!', '?', '.'): #new filter
            out_word = out_word.strip(k)
        ans.append(out_word.strip())

    return ' '.join(ans)
