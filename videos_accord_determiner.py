from vk_acc import vk
from tokenizer import tokenize
import time
from glob import glob
import os
from codecs import open
from json import load, dump

def get_uibs(ui):
    # get users backsave
    li = glob(os.path.join(os.path.dirname(__file__), 'backsaves', 'videos', '*.txt'))
    ui, fname = str(ui), False
    for n in li:
        if ui == os.path.split(n)[-1].split(u'.')[0]:
            fname = n
    if not fname:
        return False
    return load(open(fname, 'rb', encoding='utf-8'))
    
def add_uibs(ui, text):
    path = os.path.join(os.path.dirname(__file__), 'backsaves', 'videos', '{}.txt'.format(str(ui)))
    dic = {'date': time.time(), 'videos': text}
    dump(dic, open(path, 'wb', encoding='utf-8'))

def get_uvideo_lemmas(ui):
    backsave = get_uibs(ui)
    if (not backsave is False) and backsave['date'] + 1800 > time.time():
        text = backsave['videos']
        print u'took videos from backsave'
    else:
        videos = vk.method('video.get', {'owner_id': ui, 'count': 200})['items']
        text = u''
        for video in videos:
            text += video['title'] + u' ' + video['description'] + u' '
        add_uibs(ui, text)
    return tokenize(text)

def get_videos_accord(users, need_best=False):
    lemmas1 = get_uvideo_lemmas(users[0]['id'])
    lemmas2 = get_uvideo_lemmas(users[1]['id'])
    mutual_lemmas = []
    for n in lemmas1:
        if n in lemmas2:
            mutual_lemmas.append(n)
    mean_count = float(min([len(lemmas1), len(lemmas2)]))
    if mean_count == 0:
        answer = None
    else:
        answer = (1 - (1 - (len(mutual_lemmas) / mean_count)) ** 4)
    if need_best:
        dic = []
        for n in lemmas1:
            if n in lemmas2:
                dic.append({'lemma': n, 'rate': lemmas1[n]+lemmas2[n]})
        dic.sort(key = lambda x: 0-x['rate'])
        return answer, dic
    return answer
