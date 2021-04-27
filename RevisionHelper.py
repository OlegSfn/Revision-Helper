import random as rn
import datetime as dt
import re
import ctypes
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


class color:
    purple = '\033[95m'
    cyan = '\033[96m'
    darkcyan = '\033[36m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    bold = '\033[1m'
    underline = '\033[4m'
    end = '\033[0m'


dict = {}
wordsArray = []
answerMode = '1'
gameMode = '1'

#------------------------Settings------------------------#
fileName = 'Words.txt'
sep = '->'
gameModeText = f"""
{color.cyan}Выберите режим игры.{color.end}
1 - Только {color.blue}англ{color.yellow} -> {color.green}рус{color.end} 
2 - Только {color.green}рус{color.yellow} -> {color.blue}англ{color.end}
3 - Все слова: {color.green}рус{color.yellow} -> {color.blue}англ{color.end}, {color.blue}англ{color.yellow} -> {color.green}рус{color.end}
4 - Случайный выбор{color.end}, либо {color.blue}англ{color.yellow} -> {color.green}рус{color.end}, а потом {color.green}рус{color.yellow} -> {color.blue}англ{color.end}
"""
#------------------------Settings------------------------#

def sepWords(words):
    if(re.search(',', words) != None):
        return [x.lower() for x in words.split(',')]
    elif(re.search('/', words) != None):
        return [x.lower for x in words.split('/')]
    elif(re.search(';', words) != None):
        return [x.lower for x in words.split(';')]
    else:
        return words.lower()


def isOneWord(words):
    if(re.search(',', words) == None and re.search('/', words) == None and re.search(';', words) == None):
        return True
    return False



def notAllWordsInAnswer(rightAnswer, userAnswer):
    if(isOneWord(userAnswer) and isOneWord(rightAnswer)):
        return False
    elif(not isOneWord(userAnswer) and isOneWord(rightAnswer)):
        return False
    elif(isOneWord(userAnswer) and not isOneWord(rightAnswer)):
        return True
    else:
        if(len(sepWords(rightAnswer)) < len(sepWords(userAnswer))):
            return True
        return False


def wasUserRight(wordsArray, engWord, rusWord):
    wasUserRight = re.sub(r'\W', '', input(f"{color.cyan}Вы ответили правильно? {color.yellow}-> {color.green}")).lower()
    if(wasUserRight == 'да' or wasUserRight == 'д' or wasUserRight == 'yes' or wasUserRight == 'y'):
        rightAnswer(wordsArray, engWord, rusWord)
    else:
        rn.shuffle(wordsArray)


def checkAnswer(rightAnswer, userAnswer):
    if(answerMode == '1'):
        if (fuzz.token_sort_ratio(userAnswer, rightAnswer) == 100):
            return True
        return False
    elif(isOneWord(userAnswer)):
        if(process.extractOne(userAnswer, sepWords(rightAnswer))[1] == 100):
            return True
        return False
    else:
        for word in sepWords(userAnswer):
            if(process.extractOne(word, sepWords(rightAnswer))[1] != 100):
                return False
        return True


def rightAnswer(wordsArray, engWord, rusWord):
    del wordsArray[0]
    print(f'{color.end}Молодец, вы выучили слово {color.blue + engWord + color.yellow} -> {color.green + rusWord + color.end}')


def rusToEng(wordsArray):
    word = wordsArray[0]
    rusWord = dict.get(word)

    userAnswer = input(f"{color.green + rusWord + color.yellow} -> {color.blue}")
    if(checkAnswer(word, userAnswer)):
        rightAnswer(wordsArray, word, rusWord)    
    else:
        print(f"{color.red}Вы ошиблись :({color.end} Правильным словом было {color.green + word + color.end}")

        if(answerMode == '1' and notAllWordsInAnswer(word, userAnswer)):
            rn.shuffle(wordsArray)
        else:
             wasUserRight(wordsArray, word, rusWord)


def engToRus(wordsArray):
    word = wordsArray[0]
    rusWord = dict.get(word)
    
    userAnswer = input(f"{color.blue + word + color.yellow} -> {color.green}")
    if(checkAnswer(rusWord, userAnswer)):
        rightAnswer(wordsArray, word, rusWord)
    else:
        print(f"{color.red}Вы ошиблись :({color.end} Правильным словом было {color.green + rusWord + color.end}")
        
        if(answerMode == '1' and notAllWordsInAnswer(rusWord, userAnswer)):
            rn.shuffle(wordsArray)
        else:
            wasUserRight(wordsArray, word, rusWord)


def game(wordsArray):
    global gameMode, answerMode
    startTime = dt.datetime.now()
    rn.shuffle(wordsArray)
    wordsCopy = wordsArray.copy()

    while len(wordsArray) > 0:
        if(gameMode == '1'):
            engToRus(wordsArray)
        elif(gameMode == '2'):
            rusToEng(wordsArray)
        elif(gameMode == '3'):
            engToRus(wordsArray)
            rusToEng(wordsArray)
        else:
            if(rn.randint(0,1)):
                engToRus(wordsArray)
            else:
                rusToEng(wordsArray)

    endTime = dt.datetime.now() - startTime
    endTime = endTime.total_seconds()
    print(color.purple + 'Вы справились за ' + '{:,g}'.format(endTime) + 'с' + color.end)

    lastAnsw = re.sub(r'\W', '', input(f"{color.cyan}Вы выучили все слова, хотите повторить или учить новые?{color.yellow} ->{color.end} ")).lower()
    if(lastAnsw == 'да' or lastAnsw == 'д' or lastAnsw == 'yes' or lastAnsw == 'y'):
        gameMode = input(gameModeText)
        answerMode = input("1 - надо написать все значения слова, 2 - засчитывается и одно: ")

        game(wordsCopy)
    else:
        return


def start():
    with open(fileName, 'r', encoding='utf-8') as f:
        for line in f:
            words = line.split(sep)
            dict[words[0]] = re.sub('\n', '', words[1])
            wordsArray.append(words[0])

    global gameMode
    gameMode = input(gameModeText)

    global answerMode
    answerMode = input("1 - надо написать все значения слова, 2 - засчитывается и одно: ")

    game(wordsArray)


start()

#--------------------------Plans--------------------------#
'''

'''
