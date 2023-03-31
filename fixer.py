import csv
check = [f'{k}...' for k in range(20)]

with open('Dict.csv', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    data = list(csvreader)
    links = {
        'N1': '(первое определение)',
        'N2': '(второе определение)',
        'N3': '(третье определение)',
        'N4': '(четвертое определение)',
        'N5': '(пятое определение)',
        'N6': '(шестое определение)',
        'N7': '(седьмое определение)',
        'N8': '(восьмое определение)',
        'N9': '(девятое определение)',
        'N10': '(десятое определение)',
        'N11': '(одиннадцатое определение)',
        'N12': '(двенадцатое определение)'
    }

    with open('New_dict.csv', 'w', newline='', encoding='utf-8') as new_csvfile:
        csvwriter = csv.writer(new_csvfile)
        new_row = []

        for row in data:
            word, dtion = row
            new_dtion = []

            if not new_row:
                new_row = [word, []]

            for i in dtion.split():
                try:
                    x = links[i]
                    new_dtion.append(x)
                except:
                    if i == '==':
                        new_dtion.append('синоним слова')
                    elif i == '<=':
                        new_dtion.append('от слова')
                    elif i == '=>':
                        new_dtion = [] #удаление
                        break
                    elif 'N' in i and 'No' not in i:
                        new_dtion.append(f'(опред. {i[1:]})')
                    elif i not in ['!', 'Non-st', 'Colloq', 'Lib', 'Spec'] and i not in check:
                        new_dtion.append(i)

            if new_row[0] == word:
                new_row[1].append(' '.join(new_dtion).capitalize())
            else:
                if len(new_row[1]) > 1:
                    for j in range(len(new_row[1])):
                        new_row[1][j] = f'{j+1}) {new_row[1][j]}'
                    csvwriter.writerow([new_row[0], '\n'.join(new_row[1])])
                else:
                    csvwriter.writerow([new_row[0], ' '.join(new_row[1])])

                new_row = []

#N12 is max