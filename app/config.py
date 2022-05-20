DB_USER = 'root'
DB_PASSWORD = '~Qscvgy234!!'
DB_HOST = '139.155.76.178'
DB_DB = 'data'

DEBUG = True
PORT = 3333
HOST = "139.155.76.178"
SECRET_KEY = "test key --modify me"

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_DB
