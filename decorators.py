from functools import wraps
from flask import session,redirect,url_for

#登陆限制装饰器,只有登陆了才能发布问答
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)   #注意要return
        else:
            return redirect(url_for('login'))
    return wrapper