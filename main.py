import random
from datetime import timedelta

from ronglian_sms_sdk import SmsSDK

from database import *
from flask import send_from_directory, request, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename  # 上传文件需要的库
import os

app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # 配置jwt加密密钥
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=5)  # 配置token过期时间
app.secret_key = "meaning"  # 配置session密钥
jwt = JWTManager(app)
# sdk = SmsSDK("ACCOUNT SID","AUTHTOKEN","APPID")
sdk = SmsSDK("2c94811c8cd4da0a018df3b5eebe2aad", "e076a8ae3883418185c930633e80efc2", "2c94811c8cd4da0a018df3b5f0412ab4")
app.config['UPLOAD_FOLDER'] = 'image'   # 配置上传文件的文件夹,只有这样的相对路径可以识别


# 确保上传文件夹存在
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def create_response(status, msg, code=200, data=[]):  # 封装响应信息
    response = {
        "status": status,
        "code": code,
        "msg": msg,
        "data": data,
        "count": len(data)
    }
    return response


def get_verification_code():  # 生成验证码
    return "".join(random.choices("0123456789", k=4))


@app.route("/sendMessage", methods=["POST"])  # 发送验证码
def send_sms():
    try:
        if "phone" not in request.json:
            return jsonify(create_response("failed", "缺少手机号参数"), 400)
        code = get_verification_code()
        phone = request.json["phone"]
        if phone == "":
            return jsonify(create_response("failed", "您需要输入手机号才能获得验证码", 400))
        if len(phone) != 11:
            return jsonify(create_response("failed", "手机号码必须为11位", 400))
        session[phone] = code
        # sdk.sendMessage("1", phone, (code, 5))    # 之后需要解开注释，才能将验证码发到手机上
        print(f"验证码：{code}")
        return jsonify(create_response("ok", "短信发送成功"))
    except Exception as e:
        return jsonify(create_response("error", str(e), 500))


@app.route("/users")  # 获取所有用户
def get_all_user():
    try:
        users = db.session.query(User).all()
        userList = [user.to_dict() for user in users]
        res = create_response("ok", "获取用户列表成功", data=userList)
        return jsonify(res)
    except Exception as e:
        res = create_response("error", str(e), 500)
        return jsonify(res)


@app.route("/image/<path:avatar_file>")  # 查看图片的接口
def get_avatar(avatar_file):
    return send_from_directory("image", avatar_file)


@app.route("/login", methods=["POST"])  # 登录接口，返回token
def login():
    try:
        if "phone" not in request.json:
            return jsonify(create_response("failed", "缺少手机号参数"), 400)
        if "password" not in request.json:
            return jsonify(create_response("failed", "缺少密码参数"), 400)

        phone = request.json["phone"]  # 手机号
        password = request.json["password"]

        if phone == "" or password == "":
            return jsonify(create_response("failed", "手机号或密码为空", 400))

        users = db.session.query(User).filter(User.phone == phone).all()
        get_user_res = len(users)
        if get_user_res == 0:
            return jsonify(create_response("failed", "账号不存在", 400))

        if users[0].check_password(password):
            access_token = create_access_token(identity=users[0])  # Authorization : Bearer <Token>
            return jsonify(create_response("success", "登录成功", data="Bearer " + access_token))  # JWT的token认证格式
        else:
            return jsonify(create_response("failed", "登录失败，账号或密码错误", 400))
    except Exception as e:
        return jsonify(create_response("error", str(e), 500))


@app.route("/register", methods=["POST"])  # 注册用户,但是没有做定时清除验证码的操作
def register_user():
    try:
        arg = request.json

        if "phone" not in arg:
            return jsonify(create_response("failed", "缺少手机号参数"), 400)
        if "password" not in arg:
            return jsonify(create_response("failed", "缺少密码参数"), 400)
        if "username" not in arg:
            return jsonify(create_response("failed", "缺少用户名参数"), 400)
        if "code" not in arg:
            return jsonify(create_response("failed", "缺少验证码参数"), 400)

        if arg["phone"] != "" and arg["password"] != "" and arg["username"] != "" and arg["code"] != "":
            if len(arg["phone"]) != 11:
                return jsonify(create_response("failed", "手机号长度必须要为11位", 400))
            elif 10 > len(arg["password"]) or len(arg["password"]) > 16:
                return jsonify(create_response("failed", "密码长度必须要为10~16位", 400))
            elif 1 > len(arg["username"]) or len(arg["username"]) > 10:
                return jsonify(create_response("failed", "用户名长度必须为1~10位", 400))
            else:
                res = db.session.query(User).filter(User.phone == arg["phone"]).all()
                if len(res) != 0:
                    return jsonify(create_response("failed", "该手机号已注册", 400))
                elif session[arg["phone"]] != arg["code"]:
                    return jsonify(create_response("failed", "验证码错误", 400))
                else:
                    user = User(
                        phone=arg["phone"],
                        username=arg["username"],
                    )
                    user.set_password(arg["password"])
                    db.session.add(user)
                    db.session.commit()
                    session.pop(arg["phone"], None)  # 注册成功后清除验证码
                    return jsonify(create_response("success", "注册用户成功"))
        else:
            return jsonify(create_response("failed", "手机号，密码，用户名，验证码其中有空值", 400))
    except Exception as e:
        return jsonify(create_response("error", str(e), 500))


@app.route("/forgetPassword", methods=["POST"])  # 忘记密码
def forget_password():
    try:
        if "phone" not in request.json:
            return jsonify(create_response("failed", "缺少手机号参数", 400))
        if "password" not in request.json:
            return jsonify(create_response("failed", "缺少密码参数", 400))
        if "code" not in request.json:
            return jsonify(create_response("failed", "缺少验证码数", 400))

        phone = request.json["phone"]
        password = request.json["password"]
        code = request.json["code"]

        if phone == "" or password == "" or code == "":
            return jsonify(create_response("failed", "手机号，密码，验证码其中有空值", 400))

        if 10 > len(password) or len(password) > 16:
            return jsonify(create_response("failed", "密码长度必须要为10~16位", 400))

        if session[phone] == code:
            users = db.session.query(User).filter(User.phone == phone).all()
            if len(users) != 0:
                users[0].set_password(password)
                db.session.commit()
                session.pop(phone, None)
                return jsonify(create_response("ok", "密码修改成功"))
            else:
                return jsonify(create_response("failed", "没有对应的手机账号信息，请重新输入", 400))
        else:
            return jsonify(create_response("failed", "验证码错误", 400))
    except Exception as e:
        return jsonify(create_response("error", str(e), 500))


# 从 user 对象中提取出 ID，这个 ID 将被用作 JWT 的 sub 声明。这样，在后续的请求中，服务器可以通过这个 sub 声明来识别是哪个用户发送的请求。
@jwt.user_identity_loader  # 登录时的access_token = create_access_token(identity=users[0]) ，会将identify传递给该方法，由它的返回值生成token
def load_user(user):
    return user.id


# 关于用户的个人操作
@app.route("/user/getPersonalInfo")  # 获取个人信息
@jwt_required()
def get_personal_info():
    current_user_id = get_jwt_identity()
    user = db.session.query(User).filter(User.id == current_user_id).first()
    return jsonify(create_response("ok", "获取成功", data=user.to_dict()))


@app.route("/user/changePhoneNumber", methods=["POST"])  # 修改手机号
@jwt_required()
def change_phone_number():
    try:
        if "phone" not in request.json:
            return jsonify(create_response("failed", "缺少手机号参数", 400))
        if "code" not in request.json:
            return jsonify(create_response("failed", "缺少验证码参数", 400))

        phone = request.json["phone"]
        code = request.json["code"]
        if phone == "" or code == "":
            return jsonify(create_response("failed", "手机号或验证码为空", 400))
        if len(phone) != 11:
            return jsonify(create_response("failed", "手机号必须为11位数字", 400))
        if session[phone] != code:
            return jsonify(create_response("failed", "验证码错误", 400))

        current_user_id = get_jwt_identity()
        user = db.session.query(User).filter(User.id == current_user_id).first()
        if user.phone == phone:
            return jsonify(create_response("failed", "手机号和原账号手机号一致", 400))

        phone_res = db.session.query(User).filter(User.phone == phone).all()
        if len(phone_res) != 0:
            return jsonify(create_response("failed", "该手机号对应账号已存在", 400))

        user.phone = phone
        db.session.commit()
        session.pop(phone, None)
        return jsonify(create_response("ok", "手机号修改成功"))
    except Exception as e:
        return jsonify(create_response("error", str(e), 500))


@app.route("/user/changePassword", methods=["POST"])    # 修改账号的密码
@jwt_required()
def change_password():
    try:
        if "password" not in request.json:
            return jsonify(create_response("failed", "缺少新密码参数", 400))
        new_password = request.json["password"]
        if new_password == "":
            return jsonify(create_response("failed", "设置的密码为空", 400))
        if 10 > len(new_password) or len(new_password) > 16:
            return jsonify(create_response("failed", "密码长度必须要为10~16位", 400))
        current_user_id = get_jwt_identity()
        user = db.session.query(User).filter(User.id == current_user_id).first()
        if user.check_password(new_password):
            return jsonify(create_response("failed", "新密码和原密码一致", 400))
        user.set_password(new_password)
        db.session.commit()
        return jsonify(create_response("ok", "修改密码成功"))
    except Exception as e:
        return jsonify(create_response("error", str(e), 500))


@app.route("/user/changeUsername", methods=["POST"])
@jwt_required()
def change_username():
    try:
        if "username" not in request.json:  # 这句意思是在请求中连 username这个请求参数的名字也没有
            return jsonify(create_response("failed", "缺少用户名参数", 400))
        new_username = request.json["username"]
        if new_username == "":
            return jsonify(create_response("failed", "用户名为空", 400))
        if 1 > len(new_username) or len(new_username) > 10:
            return jsonify(create_response("failed", "用户名长度必须要为1~10位", 400))
        current_user_id = get_jwt_identity()
        user = db.session.query(User).filter(User.id == current_user_id).first()
        if user.username == new_username:
            return jsonify(create_response("failed", "新用户名和原用户名一致", 400))
        user.username = new_username
        db.session.commit()
        return jsonify(create_response("success", "修改用户名成功"))
    except Exception as e:
        return jsonify(create_response("error", str(e), 500))


@app.route("/user/changeAvatar", methods=["POST"])  # 上传并修改用户头像
@jwt_required()
def change_avatar():
    try:
        # # 检查是否有文件在请求中
        if 'file' not in request.files:
            return jsonify(create_response("failed", "no file part", 400))
        file = request.files['file']
        # 如果用户没有选择文件，浏览器也提交了一个空文件部分
        if file.filename == '':
            return jsonify(create_response("failed", "您没有选择图片", 400))

        if file:
            # 使用secure_filename确保文件名安全
            filename = secure_filename(file.filename)

            # 保存文件到UPLOAD_FOLDER指定的文件夹
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # 更新数据库中的头像路径
            user_id = get_jwt_identity()
            user = db.session.query(User).filter(User.id == user_id).first()
            user.avatar = os.path.join('/image', filename)
            db.session.commit()
            return jsonify(create_response("success", "上传成功"))
    except Exception as e:
        return jsonify(create_response("error", str(e), 500))
