from vk_acc import vk
import time
from glob import glob
import os
from codecs import open
from json import load, dump


def get_uibs(ui):
    # get users backsave
    li = glob(os.path.join(os.path.dirname(__file__), 'backsaves', 'groups', '*.txt'))
    ui, fname = str(ui), False
    for n in li:
        if ui == os.path.split(n)[-1].split(u'.')[0]:
            fname = n
    if not fname:
        return False
    return load(open(fname, 'rb', encoding='utf-8'))
    
def add_uibs(ui, groups):
    path = os.path.join(os.path.dirname(__file__), 'backsaves', 'groups', '{}.txt'.format(str(ui)))
    dic = {'date': time.time(), 'groups': groups}
    dump(dic, open(path, 'wb', encoding='utf-8'))

def get_groups(ui):
    backsave = get_uibs(ui)
    if (not backsave is False) and backsave['date'] + 18000 > time.time():
        groups = backsave['groups']
        print u'took groups from backsave'
    else:
        groups = vk.method('groups.get', {'user_id': ui, 'count': 1000, 'extended': 1})
        add_uibs(ui, groups)
    return groups

def get_groups_accord(users):
    groups1 = get_groups(users[0]['id'])
    groups2 = get_groups(users[1]['id'])
    mutual_groups = []
    mean_count = float(min(groups1['count'], groups2['count']))
    for n in groups1['items']:
        if n['id'] in [m['id'] for m in groups2['items']]:
            mutual_groups.append(n)
    try:
        return {"count": 1 - (1 - (len(mutual_groups) / mean_count)) ** 8, "li": [m['name'] for m in mutual_groups]}
    except ZeroDivisionError:
        return {'count': 0, 'li': []}





