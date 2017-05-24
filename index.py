# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import requests
from accord_determiner import determine
from json import loads
from vk_acc import vlzhr as vk
from vk_api import ApiError
from vip_guests import get_vipuis, get_vips, update_vip, renew_vips, del_vip
from logger import add_req, add_log

def get_accord(ui1, ui2):
    return determine(ui1, ui2)
    #resp = requests.get('http://ad.vkinst.ru?ui1={}&ui2={}'.format(str(ui1), str(ui2)))
    #return loads(resp.text)['response']

app = Flask(__name__)
app.debug = True
app.secret_key = "j"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/auth")
def auth():
    link = request.args['link']
    return redirect("/"+link.split("/")[-1])

@app.route("/vkauth")
def vkauth():
    ui = request.args['uid']
    return redirect("/id"+str(ui))

@app.route("/<screen_name>")
def desktop(screen_name):
    try:
        user = vk.method('users.get', {'user_ids': screen_name, 'fields': 'sex', 'name_case': 'gen'})[0]
    except ApiError:
        return u"Такой профиль не найден :( <a href='/'>Назад</a>"
    session['user'] = user
    friends = vk.method('friends.get', {'user_id': user['id'], 'fields': 'sex,photo_200'})['items']
    partners = [n for n in friends if (not 'deactivated' in n) and (not n['sex'] == user['sex'])]
    partners.sort(key = lambda x: x['last_name'][0])
    add_log(user)
    return render_template('desktop.html', user=user, li=partners)

@app.route("/get_accord")
def getaccord():
    return jsonify(get_accord(session['user']['id'], request.args['ui']))

@app.route("/admin")
def admin():
    if 'password' in session and session['password'] == 'vova':
        dic = {}
        for ui in get_vipuis():
            dic[ui] = get_vips(ui)
        return render_template("admin.html", dic=dic)
    return "<form action='login'><input name='password'></form>"

@app.route("/add_vip")
def add_vip():
    if not ('password' in session and session['password'] == 'vova'):
        return redirect('/admin')
    update_vip(request.args['ui'], request.args['to'], float(request.args['val']))
    return redirect('/admin')

@app.route("/new_vip")
def new_vip():
    if not ('password' in session and session['password'] == 'vova'):
        return redirect('/admin')
    renew_vips(int(request.args['ui']), {})
    return redirect('/admin')
    
@app.route("/delvip")
def delvip():
    if not ('password' in session and session['password'] == 'vova'):
        return redirect('/admin')
    del_vip(request.args['ui'], request.args['to'])
    return redirect('/admin')

@app.route("/login")
def login():
    session['password'] = request.args['password']
    return redirect('/admin')

@app.route("/logout")
def logout():
    del session['password']
    return redirect("/")

if __name__ == "__main__":
    app.run('127.0.0.1', 80)


    
    
