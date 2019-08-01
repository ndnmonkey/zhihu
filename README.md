# 仿照知乎部分功能的信息发布网站
后端部分为`flask`框架；前端部分为`Boostrap`及自撸`CSS`； 数据库部分为`mysql` ，辅助工具`Navicat`。项目约700行`python`代码及前端代码若干。
以下是具体介绍：
## 一、后端设计
## 1,基于爬虫的搜索功能
> 在本项目的`发现`页中，我们通过获取项目页面中的关键字并将关键字通过爬虫(加入机制)爬取相关信息，将爬取的信息返回到`发现`页中。
>
> 首先爬取西刺上的代理服务器组成代理池，每次从代理池中获取任意服务器`IP`并配置到“发现的关键字爬取中，爬取到网页名称及其网址，并通过网址对处理网址缺失部分使其成为有效网址。
>
## 2,注册/修改、登陆、注销
### a，注册过程中密码字段加密及验证
>  注册过程中的普通字段直接写入数据库，密码字段使用 `werkzeug`中`generate_password_hash`进行加盐哈希加密，我博客中有关于加密原理的具体介绍： https://www.cnblogs.com/two-peanuts/p/11143575.html。 最终完成注册功能。
>
> 注册与修改两个功能使用同一套`HTML`模板，通过`session`来判断用户登录状态利用`Jinja2`完成分类，`session`为空则说明当前没有登录用户，此时通过`Jinja2`的使用进入该`HTML`注册过程，否则进入修改功能。
>
> 在信息修改中，我们把已登录用户的信息提前写到表单中，避免用户全部重新输入，用户直接在此基础上修改并提交即可。处于安全性的考虑，在进入修改功能前需要利用`email`验证码来验证用户是否为本人授权，这里使用的是 `flask_mail`。验证码通过自定义函数'generate_verification_code'来生成，同时，邮件正文部分分为`HTML`(出于邮件内容美观考虑)和普通文本。通过`Python`中`str`类型的合并将生成后的验证码放入`HTML`中。
>

### b，登陆
> 在注册过程中用户输入的密码经过加密后存入数据库，在登陆过程中用户输入的密码也要经过验证处理与数据库进行匹配方能完成登陆过程，这一步通过`werkzeug`中`check_password_hash`来完成。
>

### c，注销
> 用户在登陆状态时浏览器会保持其`session` 信息，通过`session`的清除就能完成用户的注销。同时通过`session`状态的判别来完成导航栏用户名的显示与否，同样用到了`Jinja2`的语法。
>

## 3，分页与翻页 
> 通过表单函数`paginate`的使用来完成分页。包括当前页面以及每页显示的个数这两个基本参数的设置，当然也包含分页溢出的处理方法。这此过程中注意一下几点：
1，参数设置(具体可参考博客)。
2，项目与`paginate`对应操作(通过`paginate.items`实现)。
在翻页中，我们使用`paginate`中各参数完成翻页，这里我们加入了一个小细节，当前页第一页时不能前翻、当前页在最后一不能后翻，这里通过当前页的判断实现，也通过`Bootstrap`进行了一定的装饰。具体参数如下表：
>
| 参数      | 含义     | 参数            | 含义            |
| :------ | :------- | :------------- | :-------------- |
| paginate.prev_num  | 上页 | paginate.next_num | 下页 |
| paginate.page       | 当前页      | paginate.pages | 总页数 |
| paginate.iter_pages()       | 迭代对象      | paginate.total |  条目总数 |
>
**注意:**迭代对象`paginate.iter_pages()`在中间页面中的翻页需要用`for`到循环，而`paginate.pages`不是可迭代对象，所以只能用`paginate.iter_pages()`。
>
## 4，加精
> 在加精功能中我们使用了`Bootstrap`中的标签。逻辑设计上我们本想打算利用在提问过程中的创建时间使最近发提出的问题通过标签加精，但是本系统的维护全由我一人，在测试中很难完成用户并发提问操作，因此我利用问题表中`id`号最新的条目进行加精，后期我会设置为通过时间加精。
>
## 5，装饰器及上下文处理器
> 1，首先谈谈装饰器，装饰器的很大一个特点是参数和返回值都是一个函数，通过装饰器能把在运行函数前或者后完成一些其他操作，比如登陆限制(先检查用户是否为登陆状态，再决定页面跳转。我们在下一条会讲到登陆限制)，关于谈装饰器详见我的博客：https://www.cnblogs.com/two-peanuts/p/10955274.html。
>
> 2，再谈谈上下文处理器`content_processor`，我们通过`session`判断用户登录状态，如果用户为登陆状态，则通过下文处理器`content_processor`完成当前登陆用户状态的输出，在模板中通过字典`key`与`value`对应完成在`HTML`页面中的变量渲染，以下是代码实现：。
>
```python
@app.context_processor
def my_context_processor():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {"user":user}
    return {}   
```
>
**注意:** 因为这个装饰器只能返回字典，所以即使没有这个用户也要返回空字典。
>

## 6，登录限制
> 作为信息发布网站，忠实用户流量以及用户区分是非常必要的，一个网站中不可能登陆用户和游客拥有一样的权限。因此，我们通过装饰器完成登陆监测，当监测客户端为游客状态时则不赋予其发布信息的功能。在这里是否游客为游客状态是同样通过`session`来判断，结合第4点中装饰器，参看具体代码见下。
>
```python
#登陆限制装饰器,只有登陆了才能发布问答
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)   #注意要return
        else:
            return redirect(url_for('login'))
    return wrapper
```
## 7，提问
>在登陆监测后若发现游客为登陆状态，则有提问的功能，功能上和表单注册所用的技术一样，但是在文本的上传中，我们添加了带样式的可编辑文本提交功能，当然，这里的样式在目前的版本中仅限于文本颜色、字号等设置，后期会加入图片上传(由于这里图片文件在数据库中的存取我还没弄懂，因此暂时搁置这个功能，但是单纯的图片上传我已经了解)。富文本编辑实际也是对于`JavaScript`的使用。
>
## 8，多类型关键字搜索
>在搜索栏中，我们把显示在主页的重要信息都作为可搜索关键字，包括问题表中标题和内容字段、用户表中用户名字段，这些关键字通过一个搜索框来实现，这里得益于类型判断(代码如下)，当我们查到用户时，会根据搜索框中用户名查询这个用户的所有问题，如果查不到用户则通过`sqlalchemy`中关键字 `or_`进行联合查询。后期会加上模糊查询。
>
```python
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
```
## 9，评论
> 首先改页面有个评论数统计功能，这里通过查询该问题下答案数目的统计`question_anws_num`来实现，实际是一个联表查询。
>
> 其次在设计上进行了权限管理，任何已登录用户均可进行权限管理，但是删除评论的权限只有评论这本人，这里先根据`anwserid`查询到该回答的作者，经过`session`判断作者与登录用户是否为同一人，是则有删除评论权限，否则没有。
>
## 10，个人信息管理
> 第1点中的修改部分设计信息的修改，不在赘述，值得一提的是我们在信息管理页面基本把该用户的所有信息都显示出来，且用户有权修改个人注册信息及删除问题信息(后期会加上修改功能)。
>
> 在已登录用户状态下，用户除了有权删除自己在该平台的评论，同样有权删除自己提出的问题，这里我没有进行用户状态的判断，因为只有登陆状态的用户才能进入该页面(处于安全方面的考虑应该进行判断的，因为`URL`后缀可以被未登录状态用户自行更改)，同样是对该问题的存在性检验，最后通过数据库操作进行删除。处于代码健壮性考虑我添加了异常处理机制，在出问题的情况下撤销问题删除操作，进行数据库回卷。
>
```python
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
```
## 11，其他用户信息
> 这里的用户信息和已等用户信息的页面几乎一致(本打算通过`session`检验将其合二为一的)，除了删除问题操作。在页面中任何涉及用户名(包括已登录用户)，都可以根据其名字点击进入相应的用户信息界面，这里同样适用了模板，所以任何用户均能查询。
>
## 12，状态检测下页面跳转
> 这里根据装饰器进行这些操作，在未登录状态下不能进行提问。
>
##  二、数据库设计
## 1，数据迁移操作
> 首先，为什么要进行数据迁移操作？因为在项目建设过程中，很多数据库字段会修改，表与表之间的连接也会修改，如果不同数据块迁移操作，那我们每次修改只能通过 `drop`和`create`进行表删除再建立。数据库迁移操作通过 `migrate`和`upgrade`就可完成上述操作，优点在于省事且安全，关于数据库迁移操作，我博客中有相关原理介绍： https://www.cnblogs.com/two-peanuts/p/10733863.html
>

## 2，表设计
> 我们对该系统设计了三张表，分别是 `User`、`Question`和`Anwser`，相互间的关系为：
>
>
| 两表      | 连接关系     | 
| :------ | :------- | 
| User--Question  | User.id--Question.ahthor_id | 
|  Anwser--Question       | Anwser.questionid--Question.id     | 
| Anwser--Question       |  Anwser.ahthor_id--Question--id      |
>
>**注意** 这里`Question`和`Anwser`中均有`ahthor_id`字段。
>
> 那么我们如何进行具体外键操作呢？我们有形如下面的操作：
>
```python
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    author = db.relationship('User',backref = db.backref('questions'))
```
## 3，各表字段设计
> 在第二点以及注册阶段基本也已讲过了，需要强调的是这里的加密功能也是在表单字段设计中的，所以贴一下示例代码：
>
```python   
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    job = db.Column(db.String(100),nullable=False)
    city=db.Column(db.String(100),nullable=False)
    introduce = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False)
    # questions = db.relationship('Question')

    def __init__(self,*args,**kwargs):
        telephone = kwargs.get('telephone')
        username = kwargs.get('username')
        password = kwargs.get('password')
        job = kwargs.get('job')
        city = kwargs.get('city')
        introduce = kwargs.get('introduce')
        email = kwargs.get('email')

        self.telephone=telephone
        self.username=username
        self.password = generate_password_hash(password)
        self.job = job
        self.city = city
        self.introduce = introduce
        self.email=email

    def check_hash_password(self,raw_password):  #这里的参数是hash过的参数以及原始传入hash
        password = check_password_hash(self.password,raw_password)
        return password  #返回bool
```

## 三、前端设计
> 前端部分就只有`HTML`和少量`CSS`，其他样式也是用`Bootstrap`，所以不再细说，后期会在部分表单操作、刷新操作中加入`Ajax`以增强系统性能。
>
