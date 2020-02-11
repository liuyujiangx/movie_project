# coding:utf8
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError


class RegisteForm(FlaskForm):
    nickname = StringField(
        label="昵称",
        validators=[
            DataRequired("请输入昵称！")
        ],
        description="昵称",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "昵称",
            "id": "input_name",

        }

    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱！")
        ],
        description="邮箱",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "邮箱",
            "id": "input_email",

        }

    )
    phone = StringField(
        label="手机",
        validators=[
            DataRequired("请输入手机！")
        ],
        description="手机",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "手机",
            "id": "input_phone",

        }

    )
    password = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "密码",
            "id": "input_password",

        }

    )
    repassword = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("请输入确认密码！")
        ],
        description="确认密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "确认密码",
            "id": "input_repassword",

        }

    )
    register = SubmitField(
        '注册',
        render_kw={
            "class": "btn btn-lg btn-success btn-block",

        }
    )


class LoginForm(FlaskForm):
    password = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码")
        ],
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "密码",
            "id": "input_password"
        }
    )
    username = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号")
        ],
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "用户名",
            "id": "input_contact"
        }
    )
    login = SubmitField(
        '登录',
        render_kw={
            "class": "btn btn-lg btn-success btn-block",

        }
    )


class UserForm(FlaskForm):
    username = StringField(
        label="昵称",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "昵称",
        }
    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱！")
        ],
        description="邮箱",
        render_kw={
            "class": "form-control",
            "placeholder": "邮箱",
            "id": "input_email",

        }

    )
    phone = StringField(
        label="手机",
        validators=[
            DataRequired("请输入手机！")
        ],
        description="手机",
        render_kw={
            "class": "form-control",
            "placeholder": "手机",
            "id": "input_phone",

        }

    )
    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("请输入简介")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "rows": 10
        }
    )
    face = FileField(
        label="头像",
        validators=[
            DataRequired("请上传头像")
        ],
        description="头像",
    )
    submit = SubmitField(
        '保存修改',
        render_kw={
            "class": "btn btn-success",

        }
    )
class CommentForm(FlaskForm):
    comment = TextAreaField(
        label='内容',
        validators=[
            DataRequired("请输入评论内容")
        ],
        description="内容",
        render_kw={
            "id":"input_content"
        }

    )
    submit = SubmitField(
        '提交评论',
        render_kw={
            "class": "btn btn-success",
            "id": "btn-sub"

        }
    )
class Pwd_editForm(FlaskForm):
    old_password = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码")
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "旧密码",
            "id": "input_oldpwd"
        }
    )
    new_password = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码")
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "新密码",
            "id": "input_newpwd"
        }
    )
    submit = SubmitField(
        '修改密码',
        render_kw={
            "class": "btn btn-success",


        }
    )
class SearchForm(FlaskForm):
    search = StringField(
        label="搜索",
        validators=[
            DataRequired("请输入内容！")
        ],
        description="内容",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入电影名！",

        }

    )
    submit = SubmitField(
        '搜索',
        render_kw={
            "class": "btn btn-default",

        }
    )