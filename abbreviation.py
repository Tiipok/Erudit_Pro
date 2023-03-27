from random import choice
from referens import alph, numeration #{'a': 1, ...}, [[beg, end], ...]
def make_sentence():

    def filter_word(word):
        new_word = ''
        for s in word:
            if s.isalpha():
                new_word += s

        return new_word

    x = open('data_words.txt', encoding='utf-8')
    data = x.readlines() #words
    x.close()

    in_word = input() #input
    sls = list(map(str.lower, list(in_word)))

    for i in range(len(sls)): #reconstruction
        if sls[i] == 'ё':
            sls[i] = 'е'
        elif sls[i] not in alph.keys():
            return f'Я не нашел слов на букву: "{sls[i]}"'

    ans = [] #making sentence
    for s in sls:
        rng = numeration[alph[s]]
        out_word = choice(data[rng[0]: rng[1]])

        if out_word in ans:
            limit = 0
            while out_word in ans:
                out_word = choice(data[rng[0]: rng[1]])

                limit += 1
                if limit == 1000:
                    return 'Слишоком много символов' #чтобы цикл не был бесконечным

        out_word = filter_word(out_word)
        ans.append(out_word.strip())

    return ' '.join(ans)


