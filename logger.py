from codecs import open
import time
import os

def hms():
    return time.strftime(u"%H-%M-%S")

def link():
    return os.path.join(os.path.dirname(__file__), 'logs',
                        time.strftime("%m%d.txt"))

def log(text):
    try:
        with open(link(), 'a', encoding='utf-8') as f:
            f.write(text+u'\n')
    except IOError:
        with open(link(), 'w', encoding='utf-8') as f:
            f.write(text+u'\n')
    

def add_req(fr, to):
    log(u"{}: {} (id{}) checked {} (id{})".format(hms(),
                                                 fr['first_name']+u' '+fr['last_name'], str(fr['id']),
                                                 to['first_name']+u' '+to['last_name'], str(to['id'])))

def add_log(user):
    log(u"{}: {} (id{}) logged in".format(hms(), user['first_name'] + u' ' + user['last_name'],
                                         str(user['id'])))
    
