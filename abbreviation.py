from random import choice
from referens import alph, numeration #{'a': 1, ...}, [[beg, end], ...]
import csv
def make_sentence(in_word):

    with open("Dict.csv", 'r', encoding="utf8") as file:
        csvreader = csv.reader(file)
        lines = list(csvreader)

    sls, ans = list(in_word), []
    for i in range(len(sls)): #reconstruction
        letter = sls[i]
        letter = letter.lower()
        if letter == 'ё': letter = 'е'
        if letter not in alph: return f'Я не нашел слов на букву: {letter}'
        a = numeration[alph[letter]]

        def filter_word(word):
            new_word = ''
            for s in word:
                if s.isalpha():
                    new_word += s

            return new_word

        out_word = choice(lines[a[0]: a[1]])[0]
        if out_word in ans:
            limit = 0
            while out_word in ans:
                out_word = choice(lines[a[0]: a[1]])[0]
                limit += 1
                if limit == 1000: return 'Слишком много символов'
        ans.append(filter_word(out_word).strip())

    return ' '.join(ans)
