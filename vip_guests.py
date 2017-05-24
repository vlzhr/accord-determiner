from codecs import open
import os
from glob import glob
from json import loads, dumps

def ulink(ui):
    return os.path.join(os.path.dirname(__file__), 'vips', str(ui)+'.txt')

def get_vipuis():
    return [os.path.basename(n).split(".")[0] for n in glob(ulink("*"))]

def get_vips(ui):
    try:
        with open(ulink(ui), 'r', encoding='utf-8') as f:
            dic = f.read()
        return loads(dic)
    except IOError:
        return {}

def renew_vips(ui, content=False):
    if content is False:
        os.remove(ulink(ui))
    else:
        with open(ulink(ui), 'w', encoding='utf-8') as f:
            f.write(dumps(content))

def update_vip(ui, to, val):
    try:
        dic = get_vips(ui)
        dic[int(to)] = val
        renew_vips(ui, dic)
    except IOError:
        renew_vips(ui, {int(to): val})
    try:
        dic = get_vips(to)
        dic[int(ui)] = val
        renew_vips(to, dic)
    except IOError:
        renew_vips(to, {int(ui): val})

def del_vip(ui, to):
    dic = get_vips(ui)
    del dic[str(to)]
    renew_vips(ui, dic)
    dic = get_vips(to)
    del dic[str(ui)]
    renew_vips(to, dic)
            

        
