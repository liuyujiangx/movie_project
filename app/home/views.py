from functools import wraps

from app import db
from app.home.forms import RegisteForm, LoginForm, UserForm
from app.models import User
from . import home
from werkzeug.security import generate_password_hash, check_password_hash

from flask import render_template, redirect, url_for, flash, request, session


def checkpwd(pwd1, pwd2):
    return check_password_hash(pwd1, pwd2)


def home_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "home" not in session:
            return redirect(url_for("home.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def home_login_req2(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "home" in session:
            return redirect(url_for("home.user", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@home.route("/login/", methods=['get', 'post'])
@home_login_req2
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        username = data["username"]
        password = data["password"]
        pwd = User.query.filter_by(name=username).first()
        num = User.query.filter_by(name=username).count()
        if num == 1:
            if checkpwd(pwd.pwd, password):
                session["home"] = username
                return redirect(request.args.get('next', url_for('home.user')))
            else:
                flash("账号或密码错误", "err")
        else:
            flash("账号或密码错误", "err")
            return redirect(url_for("home.login"))

    return render_template("home/login.html", form=form)


@home.route("/logout/")
def logout():
    session.pop("home", None)
    return redirect(url_for("home.login"))


@home.route("/register/", methods=['post', 'get'])
def register():
    form = RegisteForm()
    if form.validate_on_submit():
        data = form.data
        nickname = data["nickname"]
        email = data["email"]
        phone = data["phone"]
        password = data["password"]
        repassword = data["repassword"]
        if password == repassword:
            namenum = User.query.filter_by(name=nickname).count()
            emailnum = User.query.filter_by(email=email).count()
            phonenum = User.query.filter_by(phone=phone).count()
            if namenum == 1:
                flash("用户已经存在！", "err")
            elif emailnum == 1:
                flash("邮箱已经存在", "err")
            elif phonenum == 1:
                flash("手机已经存在", "err")
            else:
                password = generate_password_hash(password)
                user = User(
                    name=nickname,
                    email=email,
                    phone=phone,
                    pwd=password
                )
                db.session.add(user)
                db.session.commit()
                flash("注册成功！", "ok")
                redirect(url_for("home.user"))
        else:
            flash("两次密码不一致", "err")
    return render_template("home/register.html", form=form)


@home.route("/user/", methods=['post', 'get'])
@home_login_req
def user():
    form = UserForm()
    name = session["home"]
    userx = User.query.filter_by(name=name).first()
    if form.validate_on_submit():
        data = form.data
        user_count = User.query.filter_by(name=data['username']).count()
        if name == data['username']:
            user_count = user_count - 1
        if user_count == 1:
            flash("昵称已经存在", "err")
        else:
            userx.name = data['username']
            userx.email = data['email']
            userx.phone = data['phone']
            userx.info = data['info']
            db.session.add(userx)
            db.session.commit()
            session['home'] = data['username']
            flash("保存成功", "ok")

    return render_template("home/user.html", userx=userx, form=form)


@home.route("/pwd/")
@home_login_req
def pwd():
    return render_template("home/pwd.html")


@home.route("/comments/")
@home_login_req
def comments():
    return render_template("home/comments.html")


@home.route("/loginlog/")
@home_login_req
def loginlog():
    return render_template("home/loginlog.html")


@home.route("/moviecol/")
@home_login_req
def moviecol():
    return render_template("home/moviecol.html")


@home.route("/")
def index():
    return render_template("home/index.html")


@home.route("/animation/")
def animation():
    return render_template("home/animation.html")


@home.route("/search/")
def search():
    return render_template("home/search.html")


@home.route("/play/")
def play():
    return render_template("home/play.html")


@home.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"), 404
