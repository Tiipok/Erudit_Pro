import csv
from random import choice

def make_sentence(list1):
    abet = {'а': 0,
            'б': 1095,
            'в': 3372,
            'г': 7475,
            'д': 9153,
            'е': 11547,
            'ж': 11780,
            'з': 12292,
            'и': 15275,
            'й': 16720,
            'к': 16730,
            'л': 20570,
            'м': 21869,
            'н': 24175,
            'о': 27719,
            'п': 32216,
            'р': 42707,
            'с': 46344,
            'т': 52631,
            'у': 54939,
            'ф': 56695,
            'х': 57535,
            'ц': 58306,
            'ч': 58660,
            'ш': 59527,
            'щ': 60389,
            'э': 60540,
            'ю': 61111,
            'я': 61196,
            'ѐ': 61441}
    in_word, ans = input(), []
    sls = list(map(str.lower, list(in_word)))

    for s in sls:
        out = choice(list1[abet[s]:abet[chr(ord(s)+1)] + 1]) #list

        del list1[list1.index(out)]
        abet[chr(ord(s)+1)] -= 1

        ans.append(out[0])

    return ' '.join(ans)


with open('Dict.csv', 'r', encoding='utf-8') as csv_file:
    file = csv.reader(csv_file, quotechar='"')
    words = list(file)

print(make_sentence(words))

