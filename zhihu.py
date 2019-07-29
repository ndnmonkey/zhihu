from flask import Flask,render_template,request,redirect,url_for,session,g,flash
from exts import db
from models import User,Question,Anwser
import config
from decorators import login_required
from sqlalchemy import or_
from flask_mail import Mail, Message
import random
from emai_content import code_to_html

# from flask_paginate import Pagination,get_page_parameter
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail = Mail(app)

#设置验证池
vercoede_pool = []

#产生email验证码
def generate_verification_code():
    while True:
        emai_key = str(random.random() * 1000000).split(".")[0]
        if emai_key[0] != 0:
            return emai_key

@app.route('/')
def index():
    # 原始代码
    # context = {
    #     'questions':Question.query.order_by('create_time').all()   #注意all()
    # }
    # # print(context)
    # return render_template('index.html',**context)   #**的使用
    # print(request.args.get('page'))

    #分页代码
    # print(request.args.get('page',1))
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 4))
    # 上面两行千万别丢了
    # page = 1
    # per_page = 3

    paginate = Question.query.order_by(db.desc(Question.create_time)).paginate(page, per_page, error_out=False)
    #这行代码首先根据“db.desc(Question.create_time)“按照创建时间拍个序号，
    #然后“.paginate(page, per_page, error_out=False)”就成，没啥特殊操作。
    questions = paginate.items
    # 将项目与paginate对应

    question_max_id = Question.query.order_by(db.desc(Question.id)).first().id

    context = {
        'paginate': paginate,
        'questions': questions,
        'question_max_id': question_max_id
        #这里我加入了一个最大序号，是为了将最新的条目加“new”标记。
    }

    return render_template('index.html', **context)  # **的使用。


@app.route('/vertificate/',methods=["POST","GET"])
def vertificate():
    if request.method == "GET":
        #最多刷新1次,因为每刷新一次都会发一条邮件，所以限制发送次数。

        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        # print(user.email,type(user.email))
        recipients = user.email

        if len(vercoede_pool) < 1:
            msg = Message(subject='Hello user!',  # 邮件主题
                          sender="1257266527@qq.com",  # 需要使用默认发送者则不用填
                          recipients=[user.email])  # 接受邮箱，可以多个
            # 产生6位首位不为0的验证码
            verification_code = generate_verification_code()
            print("get:",verification_code)
            vercoede_pool.append(verification_code)

            # 将验证码放入html中，当成邮件内容发送出去
            # 邮件内容会以文本和html两种格式呈现，而你能看到哪种格式取决于你的邮件客户端。
            msg.body = code_to_html(verification_code)
            msg.html = code_to_html(verification_code)
            mail.send(msg)
        return render_template('vertificate.html')

    else:
        vcoede = request.form.get("vcode")
        if vcoede == vercoede_pool[-1]:  #最新发送的代码才有效，所以是[-1]。
            # print(vcoede)
            if len(vercoede_pool) >= 1:
                vercoede_pool.pop() #输入值与最新验证码一样才能pop
            return  redirect(url_for('regist')) #render_template('regist.html')
        else:
            # flash("验证码错误！")
            return '验证码错误 ！'

#这里没能解决搜索中文的功能
#**现在解决了，原因在于我把创建时间也放进去了。
@app.route('/search/')
def search():
    q = request.args.get('q')

    #这句是当搜索的是作者名字的时候的用法
    au_id = User.query.filter(User.username.contains(q)).first()

    #若找不到搜索的用户名字时候（au_id），就返回question标题和内容；找到名字就返回名字。
    if not au_id:
        questions = Question.query.filter(or_(Question.title.contains(q), Question.content.contains(q)))
    else:
        questions = Question.query.filter(Question.author_id.contains(au_id.id))

    return render_template('search.html',questions=questions)


@app.route('/login/',methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone).first()
        # print(user.check_hash_password(password))
        if user and user.check_hash_password(password):
            session["user_id"] = user.id
            session.permanent = True
            # return render_template('index.html')
            return redirect(url_for('index'))   #这句话能让用户登录后直接跳到首页。上句不能。
        else:
            flash("电话或密码不正确！")
            return redirect(url_for('login'))

#注册和修改的作用
@app.route('/regist/',methods=["POST","GET"])
def regist():
    if request.method == "GET":
        return render_template('regist.html')
    else:
        user_id = session.get('user_id')
        if not user_id:
            telephone = request.form.get('telephone')
            username = request.form.get('username')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
            city = request.form.get('city')
            introduce = request.form.get('introduce')
            job = request.form.get('job')
            email =request.form.get('email')

            user = User.query.filter(User.telephone == telephone).first()  #这里之前用的是"[0]",显示的是返回list溢出了。
            if user:
                return "该手机已被注册！"
            else:
                if password1 != password2:
                    return "两次密码不一致！"
                else:
                    user = User(telephone = telephone,username = username,password= password1,city=city,
                                introduce=introduce,job=job,email=email)
                    db.session.add(user)
                    db.session.commit()
                    print(email)
                    return redirect(url_for('login'))
        else:
            telephone = request.form.get('telephone')
            username = request.form.get('username')
            password1 = request.form.get('password1')
            # print(password1)
            password2 = request.form.get('password2')
            city = request.form.get('city')
            introduce = request.form.get('introduce')
            job = request.form.get('job')

            user = User.query.filter(User.id == user_id).first()
            user.telephone = telephone
            user.username = username
            # user.password1 = password1
            # user.password2 = password2
            # user.password1 = generate_password_hash(password1)
            # print(user.password1)
            # user.password2 = generate_password_hash(password2)
            user.city = city
            user.introduce = introduce
            user.job = job
            db.session.commit()
            return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    # session.pop('user_id')  #1
    # del session['user_id']    #2
    session.clear()           #3三种方法都能注销
    return redirect(url_for('login'))   #这里我用render_template就不行，用redirect就可以。
#因为在logout视图下渲染login的模板是不下的，只能用重定向。

# @app.route('/question/',methods=["POST","GET"])
# @login_required
# def question():
#     if request.method == "GET":
#         return render_template('question.html')
#     else:
#         title = request.form.get('title')
#         content = request.form.get('content')
#         question = Question(title=title,content=content)
#         user_id = session.get('user_id')
#         question.author = User.query.filter(User.id == user_id).first()
#         db.session.add(question)
#         db.session.commit()
#         return redirect(url_for('index'))

@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    #如果是post方法就返回tinymce生成html代码，否则渲染editor.html
    if request.method=='POST':
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        user_id = session.get('user_id')
        question.author = User.query.filter(User.id == user_id).first()
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('question.html')


@app.route('/detail/<question_id>/')
def detail(question_id):
    #该问题的评论数目
    question_anws_num = Anwser.query.filter(Anwser.question_id == question_id).count()

    question_model = Question.query.filter(Question.id == question_id).first()
    # context = {
    #     "details":question_model
    # }
    return render_template('detail.html',question=question_model,question_anws_num=question_anws_num)


@app.route('/add_anwser/',methods=['POST'])
@login_required
def add_anwser():
    content = request.form.get('anwser_content')
    question_id = request.form.get('question_id')

    anwser = Anwser(content=content)

    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    anwser.author = user

    question = Question.query.filter(Question.id == question_id).first()
    anwser.question = question

    db.session.add(anwser)
    db.session.commit()

    return redirect(url_for('detail',question_id=question_id))

    # return render_template('detail.html')?

@app.route('/user_info/')
def user_info():
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()

    #该用户写过的文章数目
    user_ques_num = Question.query.filter(Question.author_id == user_id).count()
    # print(user_ques_num)

    user_id = user_id
    user_name = user.username
    user_telephone = user.telephone
    user_ques = user.questions
    user_job = user.job
    user_city = user.city
    user_introduce  = user.introduce
    user_infomation = {
        'user_id':user_id,
        'user_name':user_name,
        'user_telephone':user_telephone,
        'user_ques':user_ques,
        'user_job':user_job,
        'user_city':user_city,
        'user_introduce':user_introduce,
        'user_ques_num':user_ques_num
    }
    return render_template('user_info.html',**user_infomation)

@app.route('/other_user_info/<anwser_name>/')
def other_user_info(anwser_name):
    # print(anwser_name)
    user = User.query.filter(User.username == anwser_name).first()
    # print(user.telephone)
    #该用户写过的文章数目
    user_ques_num = Question.query.filter(Question.author_id == user.id).count()
    # print(user_ques_num)

    user_name = user.username
    user_telephone = user.telephone
    user_ques = user.questions
    user_job = user.job
    user_city = user.city
    user_introduce  = user.introduce
    user_infomation = {
        'user_name':user_name,
        'user_telephone':user_telephone,
        'user_ques':user_ques,
        'user_job':user_job,
        'user_city':user_city,
        'user_introduce':user_introduce,
        'user_ques_num':user_ques_num
    }
    return render_template('other_user_info.html',**user_infomation)


@app.route('/upload/')
def upload():
        # print(request.args.get('page'))
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 2))

        paginate = Question.query.order_by(db.desc(Question.create_time)).paginate(page, per_page, error_out=False)
        questions = paginate.items

        question_max_id = Question.query.order_by(db.desc(Question.id)).first().id

        context = {
            'paginate':paginate,
            'questions': questions,
            'question_max_id':question_max_id
        }

        return render_template('upload.html', **context)  # **的使用

#在个人资料页删除自己写的文章
@app.route('/deletequ/<question_id>')
def deletequ(question_id):
    question =Question.query.filter(Question.id ==question_id).first()
    if question:
        try:
            db.session.delete(question)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("删除失败！")
            db.session.rollback()
    else:
        return "找不到要删除的问题！"
    return redirect(url_for('user_info'))

#在detail页删除自己的评论
@app.route('/deletean/<anwserid>')
def deletean(anwserid):
    anwser =Anwser.query.filter(Anwser.id ==anwserid).first()
    question_id=anwser.question_id

    question_anws_num = Anwser.query.filter(Anwser.question_id == question_id).count()

    question_model = Question.query.filter(Question.id == question_id).first()
    #是自己的评论才能删除
    user_id = session.get("user_id")
    if user_id ==  anwser.author_id:
        if anwser:
            try:
                db.session.delete(anwser)
                db.session.commit()
            except Exception as e:
                print(e)
                flash("删除失败！")
                db.session.rollback()
        else:
            return "找不到要删除评论！"
    else:
        flash("您不是评论者，没有权限删除该评论！")

    return redirect(url_for('detail' ,question_id=question_id,question=question_model,question_anws_num=question_anws_num))


@app.route('/change_info/')
def change_info():
    redirect(url_for('index'))

@app.context_processor
def my_context_processor():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {"user":user}
    return {}   #注意，因为这个装饰器只能返回字典，所以即使没有这个用户也要返回空字典。

# 1.上下文处理器应该返回一个字典，字典中的key会被模板中当成变量来渲染
# 2.上下文处理器返回的字典，在所有页面中都是可以使用的
# 3.被这个装饰器修饰的钩子函数，必须要返回一个字典，即使为空也要返回。

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)