import csv


def check(word):
    with open('Dict.csv', 'r', encoding="utf8") as csv_file:

        csv_read = csv.reader(csv_file, delimiter=',')

        for row in csv_read:
            if word in row: return row[1]

        else:
            return False
