# -*- coding: utf-8 -*-
""" Модуль, добывающий общие интересы двух пользователей VK.COM """

from vk_acc import vlzhr as vk
from groups_accord_determiner import get_groups_accord
from videos_accord_determiner import get_videos_accord


def load_user(vklink):
    return vk.method('users.get', {'user_ids': vklink.split('/')[-1]})[0]

def determine(vklink1="ihavebeenhere", vklink2="id342941908"):
    """ Return {"videos", "groups"} """
    dic = {}
    users = [load_user(vklink1), load_user(vklink2)]
    dic['groups'] = get_groups_accord(users)
    dic['videos'] = get_videos_accord(users)
    return dic
    
    



