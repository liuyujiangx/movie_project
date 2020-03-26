import datetime
import os
import uuid
import requests, json

from functools import wraps

from werkzeug.utils import secure_filename

from app import db, app
from app.home.forms import RegisteForm, LoginForm, UserForm, CommentForm, Pwd_editForm, SearchForm
from app.models import User, Movie, Comment, Num
from . import home
from werkzeug.security import generate_password_hash, check_password_hash

from flask import render_template, redirect, url_for, flash, request, session


def checkpwd(pwd1, pwd2):
    return check_password_hash(pwd1, pwd2)


# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


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
                print(password)
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
                    pwd=password,
                    face='lyj.jpg'
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
    print(userx.info)
    if form.validate_on_submit():
        data = form.data
        user_count = User.query.filter_by(name=data['username']).count()
        if name == data['username']:
            user_count = user_count - 1
        if user_count == 1:
            flash("昵称已经存在", "err")
        else:
            face = request.files.get('face')
            face.filename = secure_filename(face.filename)
            if not os.path.exists(app.config["UP_DIR"]):
                os.makedirs(app.config["UP_DIR"])
                os.chmod(app.config["UP_DIR"], "rw")
            face_name = change_filename(face.filename)
            face.save(app.config["UP_DIR"] + face_name)
            userx.name = data['username']
            userx.email = data['email']
            userx.phone = data['phone']
            userx.info = data['info']
            userx.face = face_name
            db.session.add(userx)
            db.session.commit()
            session['home'] = data['username']
            flash("保存成功", "ok")
    return render_template("home/user.html", userx=userx, form=form)


@home.route("/pwd/", methods=['post', 'get'])
@home_login_req
def pwd():
    form = Pwd_editForm()
    if form.validate_on_submit():
        data = form.data
        old_pwd1 = data['old_password']
        user = User.query.filter_by(name=session['home']).first()
        new_pwd = data['new_password']
        print(new_pwd)
        if checkpwd(user.pwd, old_pwd1):
            new_pwd = generate_password_hash(new_pwd)
            user.pwd = new_pwd
            db.session.add(user)
            db.session.commit()
            flash("操作成功", 'ok')
        else:
            flash("密码输入错误", 'err')
    return render_template("home/pwd.html", form=form)


@home.route("/comments/<int:page>/")
@home_login_req
def comments(page=None):
    user_id = User.query.filter_by(name=session['home']).first().id
    if page is None:
        page = 1
    page_data = Comment.query.filter_by(user_id=user_id).order_by(Comment.addtime.desc()).paginate(page=page,
                                                                                                   per_page=5)
    return render_template("home/comments.html", page_data=page_data)


@home.route("/")
def index():
    movie = Movie.query.all()
    num = Num.query.first()
    num.num = num.num + 1
    db.session.add(num)
    db.session.commit()

    return render_template("home/index.html", movie=movie, x="已被访问" + str(num.num) + "次")


@home.route("/search/", methods=['post', 'get'])
def search():
    data = request.form.get('search')
    print(data)
    if data is not None:
        moviex = Movie.query.filter(Movie.title.like("%" + data + "%") if data is not None else "").all()
        moviecount = Movie.query.filter(Movie.title.like("%" + data + "%") if data is not None else "").count()
        return render_template("home/search.html", moviex=moviex, data=data, moviecount=moviecount)
    return redirect('/')


@home.route("/play/<int:id>", methods=['get', 'post'])
@home_login_req
def play(id=None):
    form = CommentForm()
    movie = Movie.query.filter_by(id=id).first()
    user = User.query.filter_by(name=session["home"]).first()
    comments = Comment.query.filter_by(movie_id=id).all()
    commentsnum = Comment.query.filter_by(movie_id=id).count()
    if request.method == "POST":
        if form.validate_on_submit():
            data = form.data
            comment = Comment(
                content=data['comment'],
                movie_id=id,
                user_id=user.id,
            )
            db.session.add(comment)
            db.session.commit()
            return redirect("/play/" + str(movie.id))
    return render_template("home/play.html", movie=movie, form=form, comments=comments, commentsnum=commentsnum,
                           user=user)


@home.route('/mycb')
def mycb():
    data = request.args.to_dict()
    code = data.get('code')
    print(data)
    print(code)
    url = 'https://graph.qq.com/oauth2.0/token'
    body = {'grant_type': 'authorization_code', 'client_id': '101860781',
            'client_secret': '0f5a014e13e7d35fbcca51ecc2ff6745', 'code': code, 'redirect_uri': 'https://yujl.top/mycb'}
    response = requests.get(url, params=body)
    token = response.text
    token_url = '?' + token
    requests.session().close()
    return redirect('/token' + token_url)


@home.route('/token')
def token():
    data = request.args.to_dict()
    open_id = get_openid(data)
    user_info = get_user_info(data, open_id)
    uuid_count = User.query.filter_by(uuid=open_id).count()
    if uuid_count == 1:
        name = User.query.filter_by(uuid=open_id).first()
        session['home'] = name.name
        return redirect('/user')
    else:
        password = generate_password_hash('123456')
        user = User(
            name=user_info.get('nickname'),
            uuid=open_id,
            pwd = password,
            face=user_info.get('figureurl_1')
        )
        db.session.add(user)
        db.session.commit()
        session['home'] = user_info.get('nickname')
        return redirect('/user')


@home.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"), 404


def get_openid(data):
    url = 'https://graph.qq.com/oauth2.0/me'
    body = {'access_token': data.get('access_token')}
    response = requests.get(url, params=body)
    open_id = json.loads(response.text[10:-4])
    print(open_id)
    open_id = open_id.get('openid')
    requests.session().close()
    return open_id


def get_user_info(data, open_id):
    url1 = 'https://graph.qq.com/user/get_user_info'
    body1 = {'access_token': data.get('access_token'), 'oauth_consumer_key': '101860781', 'openid': open_id}
    response1 = requests.get(url1, params=body1)
    user_info = response1.json()
    print(user_info)
    requests.session().close()
    return user_info
