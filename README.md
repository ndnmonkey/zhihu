# 仿照知乎部分功能的信息发布网站
后端部分为`flask`框架；前端部分为`Boostrap`及自撸`CSS`； 数据库部分为`mysql` ，辅助工具`Navicat`。
以下是具体介绍：
## 一、后端设计
## 1,注册/修改、登陆、注销
### a，注册过程中密码字段加密及验证
>  注册过程中的普通字段直接写入数据库，密码字段使用 `werkzeug`中`generate_password_hash`进行加盐哈希加密，我博客中有关于加密原理的具体介绍： https://www.cnblogs.com/two-peanuts/p/11143575.html。 最终完成注册功能。
>
> 注册与修改两个功能使用同一套`HTML`模板，通过`session`来判断用户登录状态利用`Jinja2`完成分类，`session`为空则说明当前没有登录用户，此时通过`Jinja2`的使用进入该`HTML`注册过程，否则进入修改功能。
>
> 处于安全性的考虑，在进入修改功能前需要利用`email`验证码来验证用户是否为本人授权，这里使用的是 `flask_mail`。验证码通过自定义函数'generate_verification_code'来生成，同时，邮件正文部分分为`HTML`(出于邮件内容美观考虑)和普通文本。通过`Python`中`str`类型的合并将生成后的验证码放入`HTML`中。
>

### b，登陆
> 在注册过程中用户输入的密码经过加密后存入数据库，在登陆过程中用户输入的密码也要经过验证处理与数据库进行匹配方能完成登陆过程，这一步通过`werkzeug`中`check_password_hash`来完成。
>

### c，注销
> 用户在登陆状态时浏览器会保持其`session` 信息，通过`session`的清除就能完成用户的注销。同时通过`session`状态的判别来完成导航栏用户名的显示与否，同样用到了`Jinja2`的语法。
>

## 2，分页与翻页 
> 通过表单函数`paginate`的使用来完成分页。包括当前页面以及每页显示的个数这两个基本参数的设置，当然也包含分页溢出的处理方法。这此过程中注意一下几点：
1，参数设置(具体可参考博客)。
2，项目与`paginate`对应操作(通过`paginate.items`实现)。
在翻页中，我们使用`paginate`中各参数完成翻页，也通过`Bootstrap`进行了一定的装饰。具体参数如下表：
>
| 参数      | 含义     | 参数            | 含义            |
| :------ | :------- | :------------- | :-------------- |
| paginate.prev_num  | 上页 | paginate.next_num | 下页 |
| paginate.page       | 当前页      | paginate.pages | 总页数 |
| paginate.iter_pages()       | 迭代对象      | paginate.total |  条目总数 |
>
**注意:**迭代对象`paginate.iter_pages()`在中间页面中的翻页需要用`for`到循环，而`paginate.pages`不是可迭代对象，所以只能用`paginate.iter_pages()`。
>
## 3，加精
> 在加精功能中我们使用了`Bootstrap`中的标签。逻辑设计上我们本想打算利用在提问过程中的创建时间使最近发提出的问题通过标签加精，但是本系统的维护全由我一人，在测试中很难完成用户并发提问操作，因此我利用问题表中`id`号最新的条目进行加精，后期我会设置为通过时间加精。
>
## 4，装饰器及上下文处理器
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

## 5，登录限制
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
## 6，提问
>在登陆监测后若发现游客为登陆状态，则有提问的功能，功能上和表单注册所用的技术一样，但是在文本的上传中，我们添加了带样式的可编辑文本提交功能，当然，这里的样式在目前的版本中仅限于文本颜色、字号等设置，后期会加入图片上传(由于这里图片文件在数据库中的存取我还没弄懂，因此暂时搁置这个功能，但是单纯的图片上传我已经了解)。富文本编辑实际也是对于`JavaScript`的使用。
>
## 7，多类型关键字搜索
## 8，多类型关键字搜索  个人信息管理（修改个人信息，删除问题）
## 9，评论（设计删除）   其他用户信息查看

##  二、数据库设计
## 1，数据迁移操作
  `werkzeug`中`generate_password_hash`的使用，用于数据库密码部分的加盐哈希加密，我博客中有关于加密原理的具体介绍： https://www.cnblogs.com/two-peanuts/p/11143575.html。
## 2，表设计
在注册过程中用户输入的密码经过加密后存入数据库，在登陆过程中用户输入的密码也要经过验证处理与数据库进行匹配方能完成登陆过程，这一步通过`werkzeug`中`check_password_hash`来完成。
## 3，各表字段设计

## 三、前端设计

