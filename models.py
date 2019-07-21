from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    job = db.Column(db.String(100),nullable=False)
    city=db.Column(db.String(100),nullable=False)
    introduce = db.Column(db.String(100),nullable=False)

    # questions = db.relationship('Question')

    def __init__(self,*args,**kwargs):
        telephone = kwargs.get('telephone')
        username = kwargs.get('username')
        password = kwargs.get('password')
        job = kwargs.get('job')
        city = kwargs.get('city')
        introduce = kwargs.get('introduce')

        self.telephone=telephone
        self.username=username
        self.password = generate_password_hash(password)
        self.job = job
        self.city = city
        self.introduce = introduce

    def check_hash_password(self,raw_password):  #这里的参数是hash过的参数以及原始传入hash
        password = check_password_hash(self.password,raw_password)
        return password  #得到原始用户

class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    #now()获取的是服务器第一次运行的时间
    #now是每次创建一个模型的时候，都获取当前的时间
    # 因为now()是一个值，now是一个函数。
    create_time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    author = db.relationship('User',backref = db.backref('questions'))

class Anwser(db.Model):
    __tablename__ = "anwser"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)

    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # question = db.relationship('Question',backref=db.backref('anwsers'))
    # 如果评论展示的地方需要按照时间顺序来，就需要把上句改为下句。
    question = db.relationship('Question', backref=db.backref('anwsers',order_by=id.desc()))

    author = db.relationship('User', backref=db.backref('anwsers'))
