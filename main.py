import random

from ronglian_sms_sdk import SmsSDK

from database import *
from flask import send_from_directory, request, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # 配置jwt加密密钥
app.secret_key = "meaning"  # 配置session密钥
jwt = JWTManager(app)
# sdk = SmsSDK("ACCOUNT SID","AUTHTOKEN","APPID")
sdk = SmsSDK("2c94811c8cd4da0a018df3b5eebe2aad", "e076a8ae3883418185c930633e80efc2", "2c94811c8cd4da0a018df3b5f0412ab4")


def create_response(status, msg, code=200, data=None):  # 封装响应信息
    response = {
        "status": status,
        "code": code,
        "msg": msg,
        "data": data,
    }
    return response


def get_verification_code():  # 生成验证码
    return "".join(random.choices("0123456789", k=4))


@app.route("/sendMessage", methods=["POST"])  # 发送验证码
def send_sms():
    try:
        code = get_verification_code()
        phone = request.json["phone"]
        if phone == "":
            return jsonify(create_response("failed", "您需要输入手机号才能获得验证码", 400))
        session[phone] = code
        sdk.sendMessage("1", phone, (code, 5))
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
        account = request.json["account"]
        password = request.json["password"]

        if account == "" or password == "":
            return jsonify(create_response("failed", "账号或密码为空", 400))

        users = db.session.query(User).filter(User.account == account).all()
        get_user_res = len(users)
        if get_user_res == 0:
            return jsonify(create_response("failed", "账号不存在", 400))

        if users[0].check_password(password):
            access_token = create_access_token(identity=account)
            return jsonify(create_response("success", "登录成功", data=access_token))
        else:
            return jsonify(create_response("failed", "登录失败，账号密码错误", 400))
    except Exception as e:
        return jsonify(create_response("error", str(e), 500))


@app.route("/register", methods=["POST"])  # 注册用户,但是没有做定时清除验证码的操作
def register_user():
    try:
        arg = request.json
        if arg["account"] != "" and arg["password"] != "" and arg["username"] != "" and arg["phone"] != "" and arg[
            "code"] != "":

            if 4 > len(arg["account"]) or len(arg["account"]) > 8:
                return jsonify(create_response("failed", "账号长度必须要为4~8位", 400))
            elif 10 > len(arg["password"]) or len(arg["password"]) > 16:
                return jsonify(create_response("failed", "密码长度必须要为10~16位", 400))
            elif 1 > len(arg["username"]) or len(arg["username"]) > 10:
                return jsonify(create_response("failed", "用户名长度必须为1~10位", 400))
            elif len(arg["phone"]) != 11:
                return jsonify(create_response("failed", "手机号码长度必须是11位", 400))
            else:
                res = db.session.query(User).filter(User.account == arg["account"]).all()
                if len(res) != 0:
                    return jsonify(create_response("failed", "账号名称已存在", 400))
                elif session[arg["phone"]] != arg["code"]:
                    return jsonify(create_response("failed", "验证码错误", 400))
                else:
                    user = User(
                        account=arg["account"],
                        username=arg["username"],
                        phone=arg["phone"]
                    )
                    user.set_password(arg["password"])
                    db.session.add(user)
                    db.session.commit()
                    session.pop(arg["phone"], None)     # 注册成功后清除验证码
                    return jsonify(create_response("success", "注册用户成功"))

        else:
            return jsonify(create_response("failed", "缺少必要参数", 400))
    except Exception as e:
        return jsonify(create_response("error", str(e), 500))
