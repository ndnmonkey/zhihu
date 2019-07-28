#dialect+driver://username:password@host:port/database
import os
SECRET_KEY = os.urandom(24)
DEBUG = True

DIALECT = "mysql"
DRIVER = "mysqldb"
USERNAME = "root"
PASSWORD = "1234"
HOST = "127.0.0.1"
PORT = "3306"
DATABASE = "zhihu"

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS =False


MAIL_DEBUG = True             # 开启debug，便于调试看信息
MAIL_SUPPRESS_SEND = False    # 发送邮件，为True则不发送
MAIL_SERVER = 'smtp.qq.com'   # 邮箱服务器
MAIL_PORT = 465               # 端口
MAIL_USE_SSL = True           # 重要，qq邮箱需要使用SSL
MAIL_USE_TLS = False          # 不需要使用TLS
MAIL_USERNAME = '1257266527@qq.com'  # 填邮箱
MAIL_PASSWORD = 'nhjsxghuxqfzjbfg'      # 填授权码，一定注意这里
MAIL_DEFAULT_SENDER = '1257266527@qq.com'  # 填邮箱，默认发送者