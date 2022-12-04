# taskkill /f /im python.exe
import datetime
import os.path
import sqlite3
from flask import Flask, render_template, flash, redirect, session, request, url_for, abort, g
from forms import LoginForm
from data import FDataBase
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'fdb.db')))
app.permanent_session_lifetime = datetime.timedelta(seconds=60)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/kuku')
def hi():  # put application's code here
    return 'sdfsdf!'


@app.route('/login', methods=['GET', 'POST'])
def login():  # put application's code here
    form = LoginForm()
    # print(form.validate_on_submit())
    if form.validate_on_submit():
        flash(f"Зашел пользователь под логином {form.username.data}, запомнить = {form.remember_me.data}")
        return redirect('/index')

    return render_template('login.html', title='Авторизация пользователя', form=form)


users_passwords = {'1': '1', '2': '2', '3': '3', 'admin': '1234'}


@app.route('/login2', methods=['POST', 'GET'])
def login2():
    if 'userlogged' in session:
        return redirect(url_for('profile', username=session['userlogged']))
    elif request.method == 'POST' and request.form['username'] in users_passwords and request.form['psw'] == \
            users_passwords[request.form['username']]:
        if users_passwords == 3:
            return render_template('admin.html')
        session['userlogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userlogged']))

    return render_template('login_2var.html', title='Авторизация пользователя')


@app.route('/profile/<username>')
def profile(username):
    if 'userlogged' not in session or session['userlogged'] != username:
        abort(401)
    elif 'userlogged' and session['userlogged']:
        return f"<h1> Пользователь {username}"
def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
        return g.link_db
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route('/index')
def index():  # put application's code here
    db = get_db()
    base = FDataBase(db)


    car = {'name': ('bugatty',

                    'https://libertycity.ru/uploads/download/gta5_bugatti/fulls/j4q9k776k31rt5p2jnd2823s63/15043684584016_f61541-1.jpg')}

    return render_template('index.html', name=car['name'][0], foto=car['name'][1], title='1', menu=base.getMenu())


@app.route('/petya')
def petya():  # put application's code here
    return ''' <h2> Александр Твардовский

Василий Теркин. Сборник

Лирика

РОДНОЕ

<br>Дорог израненные спины, </br>
<br>О дальних шумных городах. </br>
    </h2> '''


# @app.route('/user/<username>')
# def user_profile(username):  # put application's code here
#     return f"<h1>Здраствуй дорогой пользователь {username}</h1>"
#
#
# @app.route('/user/<int:post_id>')
# def show_post(post_id):  # put application's code here
#     return f"<h1>Горячая и свежая новость № {post_id}</h1>"


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена')


if __name__ == '__main__':
    app.run(debug=True)
