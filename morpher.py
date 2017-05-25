# -*- coding: utf-8 -*-
import requests
import re

link = 'http://goldlit.ru/component/slog?words='

def clean(text):
    li = text.split()
    new = []
    for n in li:
        if not ('.com' in n or 'http' in n or 'www' in n or len(n) == 1):
            new.append(n)
    return u' '.join(new)

def get_imps(text):
    text = clean(text)
    text = requests.get(link+text).text
    nouns = re.findall(u' форма</strong>: ([а-яА-Я\-]+)<br/><strong>Часть речи</strong>: существительное<br/>', text)
    verbs = re.findall(u'форма</strong>: ([а-яА-Я\-]+)<br/><strong>Часть речи</strong>: глагол', text)
    eng = re.findall(u'<strong>Неизвестное слово: ([a-zа-яA-ZА-Я\-\#]+)</strong>', text)
    li = [n.lower() for n in nouns+verbs+eng]
    dic = {}
    for n in li:
        dic[n] = dic.get(n, 0) + 1
    return dic
    



