# -*- coding: utf-8 -*-
""" Модуль, добывающий общие интересы двух пользователей VK.COM """

from vk_api import ApiError
from vk_acc import vlzhr as vk
from groups_accord_determiner import get_groups_accord
from videos_accord_determiner import get_videos_accord
from horo_accord_determiner import get_horo_text
from logger import add_req, add_log
from vip_guests import get_vips

def load_user(vklink):
    try:
        return vk.method('users.get', {'fields': 'sex,bdate', 'user_ids': vklink.split('/')[-1]})[0]
    except AttributeError:
        return vk.method('users.get', {'fields': 'sex,bdate', 'user_ids': vklink})[0]

def determine(user, vklink2="id342941908"):
    """ Return {"videos", "groups"} """
    dic = {}
    try:
        users = [user, load_user(vklink2)]
        dic['groups'] = get_groups_accord(users)
        dic['videos'] = get_videos_accord(users, True)
    except ApiError:
        return {'general': 0, 'videos': {'count': 0, 'dic': {}},
                'groups': {'count': 0, 'li': []}, 'horo': {'text': u'Пользователь удален. Видимо, не судьба..'}}

    dic['user'] = users[1]
    add_req(users[0], users[1])
    
    dic['horo'] = {'text': get_horo_text(vk, users)}

    vip_val = get_vips(users[0]['id']).get(str(users[1]['id']), 0)
    if vip_val == 0:
        dic['general'] = (dic['groups']['count']*2 + dic['videos']['count']) / 3
    else:
        dic['general'] = vip_val
    return dic


if __name__=="__main__":
    pass
##    dic = {}
##    vlzhr = load_user('ihavebeenhere')
##    friends = vk.method('friends.get', {'count': 1000, 'fields': 'sex', 'user_id': vlzhr['id']})['items']
##    for n in friends:
##        if n['sex'] == 1:
##            ac = determine('ihavebeenhere', 'id'+str(n['id']))
##            dic[n['first_name']+' '+n['last_name']] = ac
##            print n['first_name']+' '+n['last_name']+': '+str(ac['groups']['count'])
##
