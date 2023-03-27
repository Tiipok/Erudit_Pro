import csv
from random import randint
def gen_three_words(letter):
    #а б в г д е ж з и й к л м н о п р с т у ф х ц ч ш щ э ю я    нет ы ь ъ ё==еtest
    letters = {'a':0 }

    l = [[0, 1095], [1096, 3372], [3373, 7475], [7476, 9153], [9154, 11547], [11548, 11780], [11781, 12292], [12293, 15275], [15276, 16720], [16721, 16730], [16731, 20570], [20571, 21869], [21870, 24175], [24176, 27719], [27720, 32216], [32217, 42707], [42708, 46344], [46345, 52631], [52632, 54939], [54940, 56695], [56696, 57535], [57536, 58306], [58307, 58660], [58661, 59527], [59528, 60389], [60390, 60540], [60541, 61112], [61113, 61196],[61197,61442]]
    with open("Dict.csv", 'r') as file:
        csvreader = csv.reader(file)
        lines = list(csvreader)
        
        a = l[a]

        first = randint(a[0],a[1])
            
        second = randint(a[0],a[1])
        while second == first: 
            second = randint(a[0],a[1])

        third = randint(a[0],a[1])
        while third == second: 
            third = randint(a[0],a[1])
        
            
        first = lines[first][0]
        second = lines[second][0]
        third = lines[third][0]
        
        print(first, second, third)

        return[first,second,third]
        
