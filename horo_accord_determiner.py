# -*- coding: utf-8 -*-
import requests
import re

def get_horo_text(vk, users):#wom=[u"Полина", u"Полины", u"Полине"], man=[u"Владимир", u"Владимира", u"Владимиру"], wom_date="10.12", man_date="3.12", wom_year='1998', man_year='1998'):
    if not ('bdate' in users[0] and 'bdate' in users[1]):
        return u'У пользователя не стоит дата рождения в вк :('

    users.sort(key = lambda x: x[u'sex'])
    wom, wom_date = [users[0]['first_name']], '.'.join(users[0]['bdate'].split('.')[:2])
    man, man_date = [users[1]['first_name']], '.'.join(users[1]['bdate'].split('.')[:2])

    if not (len(users[0]['bdate'].split('.'))==3 and len(users[1]['bdate'].split('.'))==3):
        wom_year, man_year = '1998', '1998'
    else:
        wom_year = users[0]['bdate'].split('.')[2]
        man_year = users[1]['bdate'].split('.')[2]
    
    uis = ','.join([str(n['id']) for n in users])
    for n, case in enumerate(['gen', 'dat']):
        li = vk.method('users.get', {'user_ids': uis, 'fields': 'sex', 'name_case': case})
        li.sort(key = lambda x: x['sex'])
        wom.append(li[0]['first_name'])
        man.append(li[1]['first_name'])
        
    link = 'http://misterius.ru/viewpage.php?page_id=3&date_man={1}.{3}&date_woman={0}.{2}'.format(wom_date, man_date, wom_year, man_year)
    text = requests.get(link).text
    li = re.findall('div class="result_one">([^<]+)<\/div', text)
    text = '<br><br>'.join(li)
    changes = {u'она': wom[0], u'нее': wom[1], u'ей': wom[2],
               u'он': man[0], u'него': man[1], u'ему': man[2], u'нему': man[2],
               u'они': man[0]+u' и '+wom[0]}
    for n in changes.keys() + [k.capitalize() for k in changes]:
        text = re.sub(u'[\n ]({}) '.format(n), u' {} '.format(changes[n.lower()]), u' '+text+u' ')
    return text.strip()
    



    
