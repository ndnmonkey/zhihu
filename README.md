# 仿照知乎部分功能的发布网站
后端部分为`flask`框架；前端部分为`Boostrap`及自撸`CSS`； 数据库部分为`mysql` 。


具有以下功能：

##后端设计
## 1，注册/修改、登陆
### a，注册过程中密码字段加密及验证
  `werkzeug`中`generate_password_hash`的使用，用于数据库密码部分的加盐哈希加密，我博客中有关于加密原理的具体介绍： https://www.cnblogs.com/two-peanuts/p/11143575.html。
### b，登陆
在注册过程中用户输入的密码经过加密后存入数据库，在登陆过程中用户输入的密码也要经过验证处理与数据库进行匹配方能完成登陆过程，这一步通过`werkzeug`中`check_password_hash`来完成。
### c，

## 数据库设计
### a，注册过程中密码字段加密及验证
  `werkzeug`中`generate_password_hash`的使用，用于数据库密码部分的加盐哈希加密，我博客中有关于加密原理的具体介绍： https://www.cnblogs.com/two-peanuts/p/11143575.html。
### b，登陆
在注册过程中用户输入的密码经过加密后存入数据库，在登陆过程中用户输入的密码也要经过验证处理与数据库进行匹配方能完成登陆过程，这一步通过`werkzeug`中`check_password_hash`来完成。
### c，

## 前端设计
### a，注册过程中密码字段加密及验证
  `werkzeug`中`generate_password_hash`的使用，用于数据库密码部分的加盐哈希加密，我博客中有关于加密原理的具体介绍： https://www.cnblogs.com/two-peanuts/p/11143575.html。
### b，登陆
在注册过程中用户输入的密码经过加密后存入数据库，在登陆过程中用户输入的密码也要经过验证处理与数据库进行匹配方能完成登陆过程，这一步通过`werkzeug`中`check_password_hash`来完成。
### c，
