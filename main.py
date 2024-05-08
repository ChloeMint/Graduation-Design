import random
from datetime import timedelta

from ronglian_sms_sdk import SmsSDK
from sqlalchemy import or_

from database import *
from flask import send_from_directory, request, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename  # 上传文件需要的库
from flask_sqlalchemy import pagination
import os

app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # 配置jwt加密密钥
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=5)  # 配置token过期时间
app.secret_key = "meaning"  # 配置session密钥
jwt = JWTManager(app)
# sdk = SmsSDK("ACCOUNT SID","AUTHTOKEN","APPID")
sdk = SmsSDK("2c94811c8cd4da0a018df3b5eebe2aad", "e076a8ae3883418185c930633e80efc2", "2c94811c8cd4da0a018df3b5f0412ab4")
app.config['UPLOAD_FOLDER'] = 'image'  # 配置上传文件的文件夹,只有这样的相对路径可以识别
app.config['UPLOAD_VIDEO'] = 'videos'

# 确保上传文件夹存在
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['UPLOAD_VIDEO']):
    os.makedirs(app.config['UPLOAD_VIDEO'])


def create_list_response(status, msg, code=200, data=[]):  # 封装响应信息
    response = {
        "status": status,
        "code": code,
        "msg": msg,
        "data": data,
        "count": len(data)
    }
    return response


def create_simple_response(status, msg, code=200, data=None):  # 封装响应信息
    response = {
        "status": status,
        "code": code,
        "msg": msg,
        "data": data,
    }
    return response


def get_pagination_info(page, pages, total, per_page):
    return {
        'current_page': page,
        'total_pages': pages,
        'total_items': total,
        'per_page': per_page
    }


def get_verification_code():  # 生成验证码
    return "".join(random.choices("0123456789", k=4))


# 用户相关接口
@app.route("/sendMessage", methods=["POST"])  # 发送验证码
def send_sms():
    try:
        if "phone" not in request.json:
            return jsonify(create_simple_response("failed", "缺少手机号参数"), 400)
        code = get_verification_code()
        phone = request.json["phone"]
        if phone == "":
            return jsonify(create_simple_response("failed", "您需要输入手机号才能获得验证码", 400))
        if len(phone) != 11:
            return jsonify(create_simple_response("failed", "手机号码必须为11位", 400))

        session[phone] = code
        phone_code = db.session.query(Code).filter(Code.phone == phone).first()
        if phone_code is None:
            new_phone_code = Code(phone=phone, code=code)
            db.session.add(new_phone_code)
            db.session.commit()
        else:
            phone_code.code = code
            db.session.commit()

        # sdk.sendMessage("1", phone, (code, 5))    # 之后需要解开注释，才能将验证码发到手机上
        print(f"验证码：{code}")
        return jsonify(create_simple_response("ok", "短信发送成功"))
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/users")  # 获取所有用户
def get_all_user():
    try:
        users = db.session.query(User).all()
        userList = [user.to_dict() for user in users]
        res = create_list_response("ok", "获取用户列表成功", data=userList)
        return jsonify(res)
    except Exception as e:
        res = create_simple_response("error", str(e), 500)
        return jsonify(res)


@app.route("/image/<path:avatar_file>")  # 查看图片的接口
def get_avatar(avatar_file):
    return send_from_directory("image", avatar_file)


@app.route("/image/<path:user_id>/<path:avatar_file>")  # 优化后查看图片的接口
def get_user_avatar(user_id, avatar_file):
    return send_from_directory("image/" + user_id + "/", avatar_file)


@app.route("/videos/<path:video_file>")
def get_video_url(video_file):
    return send_from_directory("videos", video_file)


@app.route("/videos/<path:user_id>/<path:video_file>")  # 优化后查看图片的接口
def get_user_video_url(user_id, video_file):
    return send_from_directory("videos/" + user_id + "/", video_file)


@app.route("/login", methods=["POST"])  # 登录接口，返回token
def login():
    try:
        if "phone" not in request.json:
            return jsonify(create_simple_response("failed", "缺少手机号参数"), 400)
        if "password" not in request.json:
            return jsonify(create_simple_response("failed", "缺少密码参数"), 400)

        phone = request.json["phone"]  # 手机号
        password = request.json["password"]

        if phone == "" or password == "":
            return jsonify(create_simple_response("failed", "手机号或密码为空", 400))

        users = db.session.query(User).filter(User.phone == phone).all()
        get_user_res = len(users)
        if get_user_res == 0:
            return jsonify(create_simple_response("failed", "账号不存在", 400))

        if users[0].check_password(password):
            access_token = create_access_token(identity=users[0])  # Authorization : Bearer <Token>
            return jsonify(
                create_simple_response("success", "登录成功", data="Bearer " + access_token))  # JWT的token认证格式
        else:
            return jsonify(create_simple_response("failed", "登录失败，账号或密码错误", 400))
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/register", methods=["POST"])  # 注册用户,但是没有做定时清除验证码的操作
def register_user():
    try:
        arg = request.json

        if "phone" not in arg:
            return jsonify(create_simple_response("failed", "缺少手机号参数"), 400)
        if "password" not in arg:
            return jsonify(create_simple_response("failed", "缺少密码参数"), 400)
        if "username" not in arg:
            return jsonify(create_simple_response("failed", "缺少用户名参数"), 400)
        if "code" not in arg:
            return jsonify(create_simple_response("failed", "缺少验证码参数"), 400)

        if arg["phone"] != "" and arg["password"] != "" and arg["username"] != "" and arg["code"] != "":
            if len(arg["phone"]) != 11:
                return jsonify(create_simple_response("failed", "手机号长度必须要为11位", 400))
            elif 10 > len(arg["password"]) or len(arg["password"]) > 16:
                return jsonify(create_simple_response("failed", "密码长度必须要为10~16位", 400))
            elif 1 > len(arg["username"]) or len(arg["username"]) > 10:
                return jsonify(create_simple_response("failed", "用户名长度必须为1~10位", 400))
            else:
                res = db.session.query(User).filter(User.phone == arg["phone"]).all()
                phone_code = db.session.query(Code).filter(Code.phone == arg["phone"]).first()
                if phone_code is None or phone_code.code is None:
                    return jsonify(create_simple_response("failed", "还未获取验证码", 400))
                if len(res) != 0:
                    return jsonify(create_simple_response("failed", "该手机号已注册", 400))
                elif phone_code.code != arg["code"]:
                    return jsonify(create_simple_response("failed", "验证码错误", 400))
                else:
                    user = User(
                        phone=arg["phone"],
                        username=arg["username"],
                    )
                    user.set_password(arg["password"])
                    db.session.add(user)
                    phone_code.code = None
                    db.session.commit()
                    print(user.id)
                    if not os.path.exists(app.config['UPLOAD_FOLDER'] + "/" + str(user.id)):
                        os.makedirs(app.config['UPLOAD_FOLDER'] + "/" + str(user.id))

                    if not os.path.exists(app.config['UPLOAD_VIDEO'] + "/" + str(user.id)):
                        os.makedirs(app.config['UPLOAD_VIDEO'] + "/" + str(user.id))

                    return jsonify(create_simple_response("success", "注册用户成功"))
        else:
            return jsonify(create_simple_response("failed", "手机号，密码，用户名，验证码其中有空值", 400))
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/forgetPassword", methods=["POST", "PUT"])  # 忘记密码
def forget_password():
    try:
        if "phone" not in request.json:
            return jsonify(create_simple_response("failed", "缺少手机号参数", 400))
        if "password" not in request.json:
            return jsonify(create_simple_response("failed", "缺少密码参数", 400))
        if "code" not in request.json:
            return jsonify(create_simple_response("failed", "缺少验证码数", 400))

        phone = request.json["phone"]
        password = request.json["password"]
        code = request.json["code"]

        if phone == "" or password == "" or code == "":
            return jsonify(create_simple_response("failed", "手机号，密码，验证码其中有空值", 400))

        if 10 > len(password) or len(password) > 16:
            return jsonify(create_simple_response("failed", "密码长度必须要为10~16位", 400))

        phone_code = db.session.query(Code).filter(Code.phone == phone).first()
        if phone_code is None:
            return jsonify(create_simple_response("failed", "未获取验证码", 400))

        if phone_code.code == code:
            users = db.session.query(User).filter(User.phone == phone).all()
            if len(users) != 0:
                users[0].set_password(password)
                phone_code.code = None
                db.session.commit()
                return jsonify(create_simple_response("ok", "密码修改成功"))
            else:
                return jsonify(create_simple_response("failed", "没有对应的手机账号信息，请重新输入", 400))
        else:
            return jsonify(create_simple_response("failed", "验证码错误", 400))
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


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
    return jsonify(create_simple_response("ok", "获取成功", data=user.to_dict()))


@app.route("/user/changePhoneNumber", methods=["POST", "PUT"])  # 修改手机号
@jwt_required()
def change_phone_number():
    try:
        if "phone" not in request.json:
            return jsonify(create_simple_response("failed", "缺少手机号参数", 400))
        if "code" not in request.json:
            return jsonify(create_simple_response("failed", "缺少验证码参数", 400))

        phone = request.json["phone"]
        code = request.json["code"]
        if phone == "" or code == "":
            return jsonify(create_simple_response("failed", "手机号或验证码为空", 400))
        if len(phone) != 11:
            return jsonify(create_simple_response("failed", "手机号必须为11位数字", 400))
        phoneCode = db.session.query(Code).filter(Code.phone == phone).all()
        if len(phoneCode) == 0:
            return jsonify(create_simple_response("failed", "该手机号还未获取验证码", 400))
        else:
            if phoneCode[0].code != code:
                return jsonify(create_simple_response("failed", "验证码错误", 400))

        current_user_id = get_jwt_identity()
        user = db.session.query(User).filter(User.id == current_user_id).first()
        if user.phone == phone:
            return jsonify(create_simple_response("failed", "手机号和原账号手机号一致", 400))

        phone_res = db.session.query(User).filter(User.phone == phone).all()
        if len(phone_res) != 0:
            return jsonify(create_simple_response("failed", "该手机号对应账号已存在", 400))

        user.phone = phone
        db.session.commit()
        session.pop(phone, None)
        return jsonify(create_simple_response("ok", "手机号修改成功"))
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/user/changePassword", methods=["POST", "PUT"])  # 修改账号的密码
@jwt_required()
def change_password():
    try:
        if "password" not in request.json:
            return jsonify(create_simple_response("failed", "缺少新密码参数", 400))
        new_password = request.json["password"]
        if new_password == "":
            return jsonify(create_simple_response("failed", "设置的密码为空", 400))
        if 10 > len(new_password) or len(new_password) > 16:
            return jsonify(create_simple_response("failed", "密码长度必须要为10~16位", 400))
        current_user_id = get_jwt_identity()
        user = db.session.query(User).filter(User.id == current_user_id).first()
        if user.check_password(new_password):
            return jsonify(create_simple_response("failed", "新密码和原密码一致", 400))
        user.set_password(new_password)
        db.session.commit()
        return jsonify(create_simple_response("ok", "修改密码成功"))
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/user/changeUsername", methods=["POST", "PUT"])  # 修改用户名
@jwt_required()
def change_username():
    try:
        if "username" not in request.json:  # 这句意思是在请求中连 username这个请求参数的名字也没有
            return jsonify(create_simple_response("failed", "缺少用户名参数", 400))
        new_username = request.json["username"]
        if new_username == "":
            return jsonify(create_simple_response("failed", "用户名为空", 400))
        if 1 > len(new_username) or len(new_username) > 10:
            return jsonify(create_simple_response("failed", "用户名长度必须要为1~10位", 400))
        current_user_id = get_jwt_identity()
        user = db.session.query(User).filter(User.id == current_user_id).first()
        if user.username == new_username:
            return jsonify(create_simple_response("failed", "新用户名和原用户名一致", 400))
        user.username = new_username
        db.session.commit()
        return jsonify(create_simple_response("success", "修改用户名成功"))
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/user/changeAvatar", methods=["POST", "PUT"])  # 上传并修改用户头像
@jwt_required()
def change_avatar():
    try:
        # # 检查是否有文件在请求中
        if 'file' not in request.files:
            return jsonify(create_simple_response("failed", "no file part", 400))
        file = request.files['file']
        # 如果用户没有选择文件，浏览器也提交了一个空文件部分
        if file.filename == '':
            return jsonify(create_simple_response("failed", "您没有选择图片", 400))

        if file:
            # 使用secure_filename确保文件名安全
            # filename = secure_filename(file.filename)
            end_type = file.filename.split(".")[-1]

            # 更新数据库中的头像路径
            user_id = get_jwt_identity()
            user = db.session.query(User).filter(User.id == user_id).first()

            # 保存文件到UPLOAD_FOLDER指定的文件夹
            version = datetime.now().strftime("%Y%m%d%H%M%S")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + str(user_id) + "/", "avatar" + version + "." + end_type))
            user.avatar = '/image/' + str(user_id) + "/avatar" + version + "." + end_type  # 这行代码实际上是为了改变刚注册时的默认头像
            db.session.commit()
            return jsonify(create_simple_response("success", "上传成功"))
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/user/changeBackground", methods=["POST", "PUT"])  # 上传并修改用户动态背景
@jwt_required()
def change_dongtai_background():
    try:
        # # 检查是否有文件在请求中
        if 'file' not in request.files:
            return jsonify(create_simple_response("failed", "no file part", 400))
        file = request.files['file']
        # 如果用户没有选择文件，浏览器也提交了一个空文件部分
        if file.filename == '':
            return jsonify(create_simple_response("failed", "您没有选择图片", 400))

        if file:
            # 使用secure_filename确保文件名安全
            # filename = secure_filename(file.filename)
            end_type = file.filename.split(".")[-1]

            # 更新数据库中的背景路径
            user_id = get_jwt_identity()
            user = db.session.query(User).filter(User.id == user_id).first()

            # 保存文件到UPLOAD_FOLDER指定的文件夹
            version = datetime.now().strftime("%Y%m%d%H%M%S")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + str(user_id) + "/", "background" + version + "." + end_type))
            user.background = '/image/' + str(user_id) + "/background" + version + "." + end_type  # 这行代码实际上是为了改变刚注册时的默认头像
            db.session.commit()
            return jsonify(create_simple_response("success", "上传成功"))
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/user/changeIntroduce", methods=["PUT", "POST"])
@jwt_required()
def change_introduction():
    if "introduce" not in request.json:
        return jsonify(create_simple_response("failed", "缺少介绍文本参数", 400))
    introduction = request.json["introduce"]
    current_user_id = get_jwt_identity()
    if introduction == "":
        return jsonify(create_simple_response("failed", "您没有输入任何文本"))
    user = db.session.query(User).filter(User.id == current_user_id).first()
    if user.introduction == introduction:
        return jsonify(create_simple_response("failed", "您没有做出任何改变", 400))
    user.introduction = introduction
    db.session.commit()
    return jsonify(create_simple_response("success", "用户简介修改成功"))


# 植物百科相关接口
@app.route("/baike")  # 获取百科列表
def get_all_baike():
    try:
        page = request.args.get("page", 1)  # 获取page页的数据，默认为第一页
        size = request.args.get("size", 4)  # 获取每页数据的数量，默认为4条
        pagination = Baike.query.paginate(page=int(page), per_page=int(size), error_out=False)
        baikes = pagination.items
        data = [baike.to_dict() for baike in baikes]
        # pagination_info = {
        #     'current_page': pagination.page,
        #     'total_pages': pagination.pages,
        #     'total_items': pagination.total,
        #     'per_page': pagination.per_page
        # }
        res = create_list_response("success", "获取列表成功", data=data)
        res["pagination_info"] = get_pagination_info(pagination.page, pagination.pages, pagination.total,
                                                     pagination.per_page)
        return jsonify(res)
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/baike/<int:baike_id>")  # 获取百科详细信息
def get_baike_detail(baike_id):
    try:
        baike = Baike.query.filter(Baike.id == baike_id).first()
        if baike is None:
            return jsonify(create_simple_response("failed", "没有该百科的信息", 400))
        return jsonify(create_simple_response("success", "获取详细信息成功", data=baike.to_dict()))
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/baike/<name>")  # 搜索植物名字，展示对应百科
def search_baike_name(name):
    try:
        baikes = db.session.query(Baike).filter(
            or_(Baike.plant_name.like(f'%{name}%'), Baike.plant_english_name.like(f"%{name}%"))).all()
        if len(baikes) == 0:
            return jsonify(create_simple_response("failed", "未找到该植物信息", 400))
        data = [baike.to_dict() for baike in baikes]
        return jsonify(create_list_response("success", "搜索成功", data=data))
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


# 动态表相关接口
@app.route("/dongtai")  # 获取所有动态
def get_all_dongtai():
    try:
        page = request.args.get("page", 1)  # 获取page页的数据，默认为第一页
        size = request.args.get("size", 10)  # 获取每页数据的数量，默认为10条
        # pagination = DongTai.query.paginate(page=int(page), per_page=int(size), error_out=False)
        pagination = DongTai.query.order_by(DongTai.publish_time.desc()).paginate(page=int(page), per_page=int(size),
                                                                                  error_out=False)  # 动态降序分页
        dongtais = pagination.items
        data = [dongtai.to_dict() for dongtai in dongtais]
        # data.sort(DongTai.publish_time)
        res = create_list_response("success", "获取动态列表成功", data=data)
        res["pagination"] = get_pagination_info(pagination.page, pagination.pages, pagination.total,
                                                pagination.per_page)
        return jsonify(res)
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/dongtai/<int:user_id>")
def get_user_published_dongtai(user_id):
    try:
        page = request.args.get("page", 1)  # 获取page页的数据，默认为第一页
        size = request.args.get("size", 10)  # 获取每页数据的数量，默认为10条
        # pagination = DongTai.query.paginate(page=int(page), per_page=int(size), error_out=False)
        pagination = DongTai.query.filter(DongTai.user_id == user_id).order_by(DongTai.publish_time.desc()).paginate(
            page=int(page), per_page=int(size),
            error_out=False)  # 动态降序分页
        dongtais = pagination.items
        data = [dongtai.to_dict() for dongtai in dongtais]
        # data.sort(DongTai.publish_time)
        res = create_list_response("success", "获取动态列表成功", data=data)
        res["pagination"] = get_pagination_info(pagination.page, pagination.pages, pagination.total,
                                                pagination.per_page)
        return jsonify(res)
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/dongtai/<int:dongtai_id>")  # 获取动态详情
def get_dongtai_detail(dongtai_id):
    try:
        dongtai = DongTai.query.filter(DongTai.id == dongtai_id).first()
        if dongtai is None:
            return jsonify(create_simple_response("failed", "没有该动态的信息", 400))
        return jsonify(create_simple_response("success", "获取动态详情成功", data=dongtai.to_dict()))
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/dongtai/delete/<int:dongtai_id>", methods=["DELETE"])  # 删除用户自己的动态
@jwt_required()
def delete_dongtai(dongtai_id):
    try:
        current_user_id = get_jwt_identity()
        dongtai = db.session.query(DongTai).filter(DongTai.id == dongtai_id).first()

        if dongtai is None:
            return jsonify(create_simple_response("failed", "该动态不存在", 400))

        if dongtai.user_id != current_user_id:
            return jsonify(create_simple_response("failed", "您无权删除该条动态,只有发布用户可以删除", 400))
        else:
            db.session.query(DongTai).filter(DongTai.id == dongtai_id).delete()
            db.session.commit()
            return jsonify(create_simple_response("success", "动态删除成功"))
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/dongtai/publish", methods=["POST"])  # 发布动态
@jwt_required()
def publish_dongtai():
    if 'text' not in request.form and 'files' not in request.files and 'video' not in request.files:
        # 判断文字和图片视频都不存在这种情况
        return jsonify(create_simple_response("failed", "您没有输入任何数据", 400))
    if 'files' in request.files and 'video' in request.files:
        return jsonify(create_simple_response("您只能上传视频或者图片的其中一种", 400))
    else:
        current_user_id = get_jwt_identity()
        dongtai = DongTai(
            user_id=current_user_id
        )
        if 'text' not in request.form and 'video' not in request.files:
            files = request.files.getlist("files")  # 获取请求提交参数都为files参数key的文件，并将其转成列表
            for file in files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + str(current_user_id), filename))
                # dongtai.add_image(os.path.join("/image", filename))
                dongtai.add_image("/image/" + str(current_user_id) + "/" + filename)
        elif 'text' in request.form and 'files' not in request.files and 'video' not in request.files:
            dongtai.article_text = request.form.get("text")
        elif 'text' not in request.form and 'files' not in request.files and 'video' in request.files:
            file = request.files.get('video')
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_VIDEO'] + "/" + str(current_user_id), filename))
            # dongtai.add_video(os.path.join("/videos", filename))
            dongtai.add_video("/videos/" + str(current_user_id) + "/" + filename)
        elif 'text' in request.form and 'video' in request.files and 'files' not in request.files:
            dongtai.article_text = request.form.get("text")
            file = request.files.get('video')
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_VIDEO'] + "/" + str(current_user_id), filename))
            # dongtai.add_video(os.path.join("/videos", filename))
            dongtai.add_video("/videos/" + str(current_user_id) + "/" + filename)
        else:
            dongtai.article_text = request.form.get("text")
            files = request.files.getlist("files")
            for file in files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + str(current_user_id), filename))
                # dongtai.add_image(os.path.join("/image", filename))
                dongtai.add_image("/image/" + str(current_user_id) + "/" + filename)
        db.session.add(dongtai)
        db.session.commit()
        return jsonify(create_simple_response("success", "发布动态成功"))


@app.route("/dongtai/like/<int:dongtai_id>")  # 点赞和取消点赞,动态的喜欢数量也随之会变化
@jwt_required()
def like(dongtai_id):
    try:
        dongtai = DongTai.query.filter(DongTai.id == dongtai_id).first()
        if dongtai is None:
            return jsonify(create_simple_response("failed", "该动态不存在", 400))
        current_user_id = get_jwt_identity()
        li = Like.query.filter(Like.user_id == current_user_id).filter(Like.article_id == dongtai_id).first()
        if li is None:
            like = Like(
                user_id=current_user_id,
                article_id=dongtai_id
            )
            db.session.add(like)
            # dongtai.like_num += 1
            db.session.commit()
            return jsonify(create_simple_response("success", "点赞成功"))
        else:
            Like.query.filter(Like.user_id == current_user_id).filter(Like.article_id == dongtai_id).delete()
            # dongtai.like_num -= 1
            db.session.commit()
            return jsonify(create_simple_response("success", "取消点赞成功", 200))
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/comment/publish/<int:dongtai_id>", methods=["POST"])  # 发布评论
@jwt_required()
def publish_comment(dongtai_id):
    try:
        if "text" not in request.json:
            return jsonify(create_simple_response("failed", "缺少文本参数", 400))
        comment_text = request.json["text"]
        if comment_text == "":
            return jsonify(create_simple_response("failed", "您没有输入任何内容", 400))
        current_user_id = get_jwt_identity()
        comment = Comment(
            article_id=dongtai_id,
            comment_user_id=current_user_id,
            comment_text=comment_text
        )
        db.session.add(comment)
        db.session.commit()
        return jsonify(create_simple_response("success", "添加评论成功"))
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/note")  # 获取所有自己的笔记
@jwt_required()
def get_all_note():
    try:
        current_user_id = get_jwt_identity()
        notes = Note.query.filter(Note.user_id == current_user_id).all()
        data = [note.to_dict() for note in notes]
        return jsonify(create_list_response("success", "获取笔记列表成功", data=data))
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/note/<int:note_id>")  # 获取笔记详细信息
@jwt_required()
def get_note_detail(note_id):
    try:
        note = Note.query.filter(Note.id == note_id).first()
        if note is None:
            return jsonify(create_simple_response("failed", "该笔记不存在", 400))
        current_user_id = get_jwt_identity()
        if note.user_id != current_user_id:
            return jsonify(create_simple_response("failed", "只有该笔记的发布者可以查看该笔记", 400))
        return jsonify(create_simple_response("success", "获取笔记成功", data=note.to_dict()))
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/note/createNote", methods=["POST"])
@jwt_required()
def create_note():
    try:
        if "title" not in request.json:
            return jsonify(create_simple_response("failed", "缺少标题参数", 400))
        if "content" not in request.json:
            return jsonify(create_simple_response("failed", "缺少内容参数", 400))
        title = request.json["title"]
        content = request.json["content"]
        if title == "" or content == "":
            return jsonify(create_simple_response("failed", "标题或内容为空", 400))
        else:
            current_user_id = get_jwt_identity()
            note = Note(
                user_id=current_user_id,
                title=title,
                content=content
            )
            db.session.add(note)
            db.session.commit()
            return jsonify(create_simple_response("success", "新建笔记成功"))
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/note/editing/<int:note_id>", methods=["POST", "PUT"])
@jwt_required()
def editing_note(note_id):
    try:
        note = Note.query.filter(Note.id == note_id).first()
        if note is None:
            return jsonify(create_simple_response("failed", "该笔记不存在", 400))
        current_user_id = get_jwt_identity()
        if note.user_id != current_user_id:
            return jsonify(create_simple_response("failed", "只有该笔记的发布者可以编辑", 400))
        if "title" not in request.json:
            return jsonify(create_simple_response("failed", "缺少标题参数", 400))
        if "content" not in request.json:
            return jsonify(create_simple_response("failed", "缺少内容参数", 400))
        title = request.json["title"]
        content = request.json["content"]
        if title == "":
            return jsonify(create_simple_response("failed", "标题不能为空", 400))
        note.title = title
        note.content = content
        db.session.commit()
        return jsonify(create_simple_response("success", "笔记修改成功", 400))
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/note/delete/<int:note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id):
    try:
        note = Note.query.filter(Note.id == note_id).first()
        if note is None:
            return jsonify(create_simple_response("failed", "该笔记不存在", 400))
        current_user_id = get_jwt_identity()
        if note.user_id != current_user_id:
            return jsonify(create_simple_response("failed", "只有笔记的发布者可以删除", 400))
        else:
            Note.query.filter(Note.id == note_id).delete()
            db.session.commit()
            return jsonify(create_simple_response("success", "删除笔记成功"))
    except Exception as e:
        return jsonify(create_simple_response("error", str(e), 500))


@app.route("/testSession", methods=["POST"])
def get_session():
    phone = request.json["phone"]
    print(session[phone])
    return ""
