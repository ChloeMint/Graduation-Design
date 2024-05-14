from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, json
from sqlalchemy import DateTime
from werkzeug.security import generate_password_hash, check_password_hash
import pytz  # 这个库是将默认的UTC时间转换成ISO 8601格式

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "hhx2005426"

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(40), nullable=False, unique=True)  # 账号,唯一，用手机号登录
    password_hash = db.Column(db.String(128), nullable=False)  # 密码
    username = db.Column(db.String(40), nullable=False)  # 用户名称
    avatar = db.Column(db.String(255), default="/image/default_avatar.png")  # 用户头像
    introduction = db.Column(db.String(20), default="无")  # 用户简介
    background = db.Column(db.String(255), default="/image/meBackground.jpg")
    is_delete = db.Column(db.Boolean, default=False)

    # notes = db.relationship('Note', backref='user')
    # dongtai = db.relationship('DongTai', backref='user')

    def set_password(self, password):
        """Sets the password field to the hashed password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the hashed password."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'phone': self.phone,
            'username': self.username,
            'avatar': self.avatar,
            'introduction': self.introduction,
            'background': self.background
            # 'notes': [note.to_dict() for note in self.notes],
            # 'dongtai': [dongtai.to_dict() for dongtai in self.dongtai]
        }


class Baike(db.Model):
    __tablename__ = "baike"
    id = db.Column(db.Integer, primary_key=True)
    plant_name = db.Column(db.String(30), nullable=False)  # 植物中文名称
    plant_english_name = db.Column(db.String(30))  # 植物英文名称
    imageList = db.Column(db.Text)  # 用于存储json字符串
    introduction = db.Column(db.Text, nullable=False)  # 植物简要介绍
    care_knowledge = db.Column(db.Text)  # 养护知识
    area = db.Column(db.Text, nullable=False)  # 分布地区
    plantCulture = db.Column(db.Text, nullable=False)  # 植物文化
    legendStory = db.Column(db.Text, nullable=False)  # 传说故事

    def add_image(self, image_url):
        if not self.imageList:
            self.imageList = json.dumps([image_url])  # 列表转字符串'["1.jpg"]'
        else:
            self.imageList = json.dumps(json.loads(self.imageList) + [image_url])

    def get_images(self):
        return json.loads(
            self.imageList) if self.imageList else []  # 字符串转字符串列表["1.jpg"],为了保证取出来的类型还是字符串数组，需要在to_dict()中使用该方法

    def to_dict(self):
        return {
            'id': self.id,
            'plant_name': self.plant_name,
            'plant_english_name': self.plant_english_name,
            'imageList': self.get_images(),
            # 这里本来是直接用self.imageList但是不知道为什么明明存进去是不带\的一个数组图片url，但是在获得数据的时候每张图片的url前面都会有[\image.jpg\]这种奇怪的现象
            'introduction': self.introduction,
            'care_knowledge': self.care_knowledge,
            'area': self.area,
            'plantCulture': self.plantCulture,
            'legendStory': self.legendStory
        }


class DongTai(db.Model):
    __tablename__ = "dongtai"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    publish_time = db.Column(DateTime, default=datetime.utcnow)  # 发布时间
    like_num = db.Column(db.Integer, nullable=False, default=0)  # 点赞数
    article_text = db.Column(db.Text)  # 文章内容
    imageList = db.Column(db.Text)  # 用于存储json字符串
    videoUrl = db.Column(db.Text)  # 用于存储视频
    comments = db.relationship('Comment', backref='dongtai')  # 链接评论
    user = db.relationship('User', backref='dongtai')
    like = db.relationship('Like', backref="dongtai")

    def add_image(self, image_url):
        if not self.imageList:
            self.imageList = json.dumps([image_url])
        else:
            self.imageList = json.dumps(json.loads(self.imageList) + [image_url])

    def get_images(self):
        return json.loads(self.imageList) if self.imageList else []

    def add_video(self, video_url):
        self.videoUrl = video_url

    def get_video_url(self):
        return self.videoUrl

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'publish_time': self.publish_time,
            'like_num': self.like_num,
            'article_text': self.article_text,
            'imageList': self.get_images(),
            'videoUrl': self.get_video_url(),
            'comments': [comment.to_dict() for comment in self.comments],
            'user': self.user.to_dict(),
            'like': [like.to_dict() for like in self.like]
        }


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('dongtai.id'), nullable=False)
    comment_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment_text = db.Column(db.Text)
    user = db.relationship('User', backref='comment')  # 链接用户

    def to_dict(self):
        return {
            'id': self.id,
            'article_id': self.article_id,
            'comment_user_id': self.comment_user_id,
            'comment_text': self.comment_text,
            'user': self.user.to_dict()
        }


class Note(db.Model):
    __tablename__ = "note"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content
        }


class Like(db.Model):  # 所有用户点赞表
    __tablename__ = "like"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('dongtai.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'article_id': self.article_id
        }


class Code(db.Model):
    __tablename__ = "code"
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(40), nullable=False, unique=True)  # 账号,唯一，用手机号登录
    code = db.Column(db.String(4))

    def to_dict(self):
        return {
            'id': self.id,
            'phone': self.phone,
            'code': self.code
        }


class ApplicationBug(db.Model):
    __tablename__ = "ApplicationBug"
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(10))
    content = db.Column(db.Text)
    publish_time = db.Column(DateTime, default=datetime.utcnow())  # 发布时间


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
