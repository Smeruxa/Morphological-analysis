import pymorphy2
import re

def getrazr(object):
    keys = list(razrmest.keys())
    for i in range(len(keys)):
        if keys[i] in object:
            return razrmest[keys[i]]
    return "Личное"

def getrazrdouble(object):
    keys = list(razrmesttwo.keys())
    for i in range(len(keys)):
        if keys[i] in object:
            return razrmesttwo[keys[i]]
    return "Образа действий"

def is_russian(word):
    vfilter = re.compile("[а-яА-Я]+")
    return vfilter.match(word)

def cmain(object):
    for i in range(len(ismain)):
        if ismain[i] in object:
            return "Собственное" 
    return "Нарицательное"

def getpril(object):
    if "Qual" in object:
        return prilset["Qual"]
    elif "Poss" in object:
        return prilset["Poss"]
    else:
        return "Относительное"

def rappend(table, *v):
    for i in range(len(v)):
        table.append(v[i])

def checkprilstep(object):
    return "Превосходная" if 'Supr' in object.tag else "Сравнительная" if 'Cmp2' in object.tag else "Неизвестно"

def getprilpart(name):
    return "Полное" if name == "ADJF" else "Краткое"

def tofirstnumber(object):
    return object.inflect({'sing'})

def tofullform(object):
    return object.inflect({'ADJF'})

def getnumbertype(object):
    return "Порядковое" if 'Anum' in object else "Количественное"

def sobirnumber(object):
    return "Собирательное" if 'Coll' in object else "Целое"

def checknumber(object):
    if object.number != None:
        return number[object.number] + " число"
    else:
        return "Число отсутствует"

def checkgender(object):
    if object.gender != None:
        return gender[object.gender] + " род"
    else:
        return "Род отсутствует"

def unchanched(object):
    return "Неизменяемое" if 'Fixd' in object else "Изменяемое"

def checkexistedcase(object):
    if tofullform(object) != None:
        return case[tofullform(object).tag.case] + " падеж"
    else:
        return "Неизвестный падеж"

def vozvglag(object):
    return "Возвратный" if "Refl" in object else "Невозвратный"