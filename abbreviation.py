import csv
from random import choice
import referens
def make_sentence(list1):
    in_word, ans = input(), [] #input

    abet, index = referens.alph, referens.numeration #{'a': 1, ...}, [[beg, end], ...]
    sls = list(map(str.lower, list(in_word)))

    for i in range(len(sls)): #reconstruction
        if sls[i] == 'ё':
            sls[i] = 'е'

    for s in sls:
        out = choice(list1[abet[s]:abet[chr(ord(s)+1)] + 1]) #list

        del list1[list1.index(out)]

    return ' '.join(ans)

