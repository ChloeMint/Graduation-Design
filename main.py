from database import *
from flask import send_from_directory, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # 配置jwt加密密钥
jwt = JWTManager(app)


def create_response(status, msg, code=200, data=None):  # 封装响应信息
    response = {
        "status": status,
        "code": code,
        "msg": msg,
        "data": data,
    }
    return response


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


@app.route("/register", methods=["POST"])  # 注册用户
def register_user():
    try:
        arg = request.json
        if arg["account"] != "" and arg["password"] != "" and arg["username"] != "":

            if 4 > len(arg["account"]) or len(arg["account"]) > 8:
                return jsonify(create_response("failed", "账号长度必须要为4~8位", 400))
            elif 10 > len(arg["password"]) or len(arg["password"]) > 16:
                return jsonify(create_response("failed", "密码长度必须要为10~16位", 400))
            elif 1 > len(arg["username"]) or len(arg["username"]) > 10:
                return jsonify(create_response("failed", "用户名长度必须为1~10位", 400))
            else:

                res = db.session.query(User).filter(User.account == arg["account"]).all()
                if len(res) != 0:
                    return jsonify(create_response("failed", "账号名称已存在", 400))
                else:
                    user = User(
                        account=arg["account"],
                        username=arg["username"],
                    )
                    user.set_password(arg["password"])
                    db.session.add(user)
                    db.session.commit()
                    return jsonify(create_response("success", "注册用户成功"))
        else:
            return jsonify(create_response("failed", "缺少必要参数", 400))
    except Exception as e:
        return jsonify(create_response("error", str(e), 500))
