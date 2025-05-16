import sqlite3
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.login_form import LoginForm
from data.register import RegisterForm
from data.admin import AdminForm
from data.admin import AddForm
from data.admin import RemoveForm
from data.buy import BuyForm
from data.users import User
from data.items import i_item

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неверный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit() and form.password.data == form.password_again.data:
        ###
        con = sqlite3.connect("db/site_db.sqlite")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM users").fetchall()
        result = result
        con.commit()

        cur = con.cursor()
        custom = (len(result) + 1, form.email.data, form.password.data, '     ')
        result = cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", custom).fetchall()
        for elem in result:
            print(elem)
        con.commit()
        con.close()
        ###
        return redirect("/login")
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/admin')
@login_required
def admin():
    if str(current_user).split()[2] == 'ADMIN' or str(current_user).split()[2] == 'MODER':
        return render_template("admin.html", title='Kartiny')
    else:
        return redirect("/")


@app.route('/admin/permissions', methods=['GET', 'POST'])
@login_required
def perms():
    form = AdminForm()
    if str(current_user).split()[2] == 'ADMIN' or str(current_user).split()[2] == 'MODER':
        if form.validate_on_submit() and form.email.data != str(current_user).split()[1]:
            db_sess = db_session.create_session()
            users = db_sess.query(User).all()
            stop = False
            for name in users:
                if str(name).split()[1] == form.email.data and len(str(name).split()) == 3:
                    if str(name).split()[2] == 'MODER':
                        stop = True
            if not stop:
                ###
                con = sqlite3.connect("db/site_db.sqlite")
                cur = con.cursor()
                if str(form.admin_status.data) == 'ADMIN':
                    ads = 'ADMIN'
                else:
                    ads = '     '
                custom = (ads, form.email.data)
                result = cur.execute("UPDATE users SET admin = ? WHERE email = ?", custom).fetchall()
                for elem in result:
                    print(elem)
                con.commit()
                con.close()
                ###
        return render_template('perms.html', form=form, title='Kartiny')
    else:
        return redirect("/")


@app.route('/admin/orders', methods=['GET', 'POST'])
@login_required
def orders():
    if str(current_user).split()[2] == 'ADMIN' or str(current_user).split()[2] == 'MODER':
        s = []
        ###
        con = sqlite3.connect("db/site_db.sqlite")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM orders").fetchall()
        for elem in result:
            s.append(elem)
        con.commit()
        ###
        return render_template('orders.html', hm=s, title='Kartiny')
    else:
        return redirect("/")


@app.route('/admin/products')
@login_required
def products():
    if str(current_user).split()[2] == 'ADMIN' or str(current_user).split()[2] == 'MODER':
        return render_template("products.html", title='Kartiny')
    else:
        return redirect("/")


@app.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
def products_add():
    form = AddForm()
    if str(current_user).split()[2] == 'ADMIN' or str(current_user).split()[2] == 'MODER':
        if form.validate_on_submit():
            ###
            con = sqlite3.connect("db/site_db.sqlite")
            cur = con.cursor()
            result = cur.execute("SELECT * FROM items").fetchall()
            result = result
            con.commit()

            cur = con.cursor()
            custom = (len(result) + 1, form.name.data, form.more.data, form.price.data, form.img.data, form.link.data)
            result = cur.execute("INSERT INTO items VALUES (?, ?, ?, ?, ?, ?)", custom).fetchall()
            for elem in result:
                print(elem)
            con.commit()
            con.close()
            ###
        return render_template("add.html", form=form, title='Kartiny')
    else:
        return redirect("/")


@app.route('/admin/products/remove', methods=['GET', 'POST'])
@login_required
def products_remove():
    form = RemoveForm()
    if str(current_user).split()[2] == 'ADMIN' or str(current_user).split()[2] == 'MODER':
        if form.validate_on_submit():
            ###
            con = sqlite3.connect("db/site_db.sqlite")
            cur = con.cursor()
            custom = (form.name.data)
            result = cur.execute("DELETE FROM items WHERE name=?", [form.name.data]).fetchall()
            for elem in result:
                print(elem)
            con.commit()
            con.close()
            ###
        return render_template("remove.html", form=form, title='Kartiny')
    else:
        return redirect("/")


@app.route("/")
def index():
    s = []
    ###
    con = sqlite3.connect("db/site_db.sqlite")
    cur = con.cursor()
    result = cur.execute("SELECT * FROM items").fetchall()
    for elem in result:
        s.append(elem)

    name = []
    description = []
    price = []
    img = []
    pid = []

    for i in range(len(s)):
        for j in range(len(s[i])):
            if j == 1:
                name.append(s[i][j])
            elif j == 2:
                description.append(s[i][j])
            elif j == 3:
                price.append(s[i][j])
            elif j == 4:
                img.append(s[i][j])
            elif j == 5:
                pid.append('buy/' + s[i][j])
    con.commit()
    con.close()
    ###
    return render_template("index.html", len_hm=len(img), names=name, ds=description, prices=price, hm=img, id=pid, title='Kartiny')


@app.route('/buy')
@login_required
def buy0():
    return redirect('/')


@app.route('/buy/<item>', methods=['GET', 'POST'])
@login_required
def buy(item):
    form = BuyForm()
    db_sess = db_session.create_session()
    items = db_sess.query(i_item).all()
    painting = ''
    price = ''
    p_img = ''
    for name in items:
        ss = str(name).split('&')
        if ss[5] == '/'+item:
            painting = ss[1]
            price = ss[3]
            p_img = '../' + ss[4]
    if painting == '':
        return redirect('/')
    if form.validate_on_submit() and form.email.data == str(current_user).split()[1]:
        ###
        con = sqlite3.connect("db/site_db.sqlite")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM orders").fetchall()
        result = result
        con.commit()

        cur = con.cursor()
        custom = (len(result) + 1, form.email.data, form.phone.data, painting, price, 0)
        result = cur.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)", custom).fetchall()
        for elem in result:
            print(elem)
        con.commit()
        con.close()
        ###
        return render_template("buy.html", title='Kartiny', message='Заказ успешно оформлен, для того, чтобы его оплатить, переведите указанную сумму на карту по номеру +7 000 555-55-11', form=form, painting=painting, price=price, p_img=p_img)
    else:
        return render_template("buy.html", title='Kartiny', form=form, painting=painting, price=price, p_img=p_img)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/site_db.sqlite")
    app.run()


if __name__ == '__main__':
    main()
