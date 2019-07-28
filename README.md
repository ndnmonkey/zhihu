# 仿照知乎部分功能的发布网站
后端部分为`flask`框架；前端部分为`Boostrap`及自撸`CSS`； 数据库部分为`mysql` 。


具有以下功能：

##后端设计
## 1，注册/修改、登陆
### a，注册过程中密码字段加密及验证
 注册过程中的普通字段直接写入数据库，密码字段使用 `werkzeug`中`generate_password_hash`进行加盐哈希加密，我博客中有关于加密原理的具体介绍： https://www.cnblogs.com/two-peanuts/p/11143575.html。 最终完成注册功能。注册与修改两个功能使用同一套`HTML`模板，通过`session`来判断用户登录状态利用`Jinja2`完成分类，`session`为空则说明当前没有登录用户，此时通过`Jinja2`的使用进入该`HTML`注册过程，否则进入修改功能。
### b，登陆
在注册过程中用户输入的密码经过加密后存入数据库，在登陆过程中用户输入的密码也要经过验证处理与数据库进行匹配方能完成登陆过程，这一步通过`werkzeug`中`check_password_hash`来完成。
### c，

## 数据库设计
### a，注册过程中密码字段加密及验证
  `werkzeug`中`generate_password_hash`的使用，用于数据库密码部分的加盐哈希加密，我博客中有关于加密原理的具体介绍： https://www.cnblogs.com/two-peanuts/p/11143575.html。
### b，登陆
在注册过程中用户输入的密码经过加密后存入数据库，在登陆过程中用户输入的密码也要经过验证处理与数据库进行匹配方能完成登陆过程，这一步通过`werkzeug`中`check_password_hash`来完成。
### c，翻页，加精，提问(富文本编辑)，多类型关键字搜索，email验证，评论

## 前端设计
### a，注册过程中密码字段加密及验证
  `werkzeug`中`generate_password_hash`的使用，用于数据库密码部分的加盐哈希加密，我博客中有关于加密原理的具体介绍： https://www.cnblogs.com/two-peanuts/p/11143575.html。
### b，登陆
在注册过程中用户输入的密码经过加密后存入数据库，在登陆过程中用户输入的密码也要经过验证处理与数据库进行匹配方能完成登陆过程，这一步通过`werkzeug`中`check_password_hash`来完成。
### c，
