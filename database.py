from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, json
from sqlalchemy import DateTime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "hhx2005426"

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(40), nullable=False, unique=True)  # 账号,唯一
    password_hash = db.Column(db.String(128), nullable=False)  # 密码
    username = db.Column(db.String(40), nullable=False)  # 用户名称
    phone = db.Column(db.String(20), nullable=False)    # 用户手机号
    avatar = db.Column(db.String(255))  # 用户头像
    notes = db.relationship('Note', backref='user')

    def set_password(self, password):
        """Sets the password field to the hashed password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the hashed password."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'account': self.account,
            'username': self.username,
            'avatar': self.avatar,
            'phone' : self.phone,
            'notes': [note.to_dict() for note in self.notes]
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
            self.imageList = json.dumps([image_url])
        else:
            self.imageList = json.dumps(json.loads(self.imageList) + [image_url])

    def get_images(self):
        return json.loads(self.imageList) if self.imageList else []

    def to_dict(self):
        return {
            'id': self.id,
            'plant_name': self.plant_name,
            'plant_english_name': self.plant_english_name,
            'imageList': self.imageList,
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
    like = db.Column(db.Enum("True", "False"), nullable=False, default="False")  # 点赞（喜欢）
    like_num = db.Column(db.Integer, nullable=False)  # 点赞数
    article_text = db.Column(db.Text)  # 文章内容
    imageList = db.Column(db.Text)  # 用于存储json字符串
    comments = db.relationship('Comment', backref='dongtai')  # 链接评论

    def add_image(self, image_url):
        if not self.imageList:
            self.imageList = json.dumps([image_url])
        else:
            self.imageList = json.dumps(json.loads(self.imageList) + [image_url])

    def get_images(self):
        return json.loads(self.imageList) if self.imageList else []

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'publish_time': self.publish_time,
            'like': self.like,
            'like_num': self.like_num,
            'article_text': self.article_text,
            'imageList': self.imageList,
            'comments': [comment.to_dict() for comment in self.comments]
        }


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('dongtai.id'), nullable=False)
    comment_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment_text = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'article_id': self.article_id,
            'comment_user_id': self.comment_user_id,
            'comment_text': self.comment_text
        }


class Note(db.Model):
    __tablename__ = "note"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content
        }


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
