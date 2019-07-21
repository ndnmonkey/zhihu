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
DATABASE = "zlktqa_demo1"

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS =False


