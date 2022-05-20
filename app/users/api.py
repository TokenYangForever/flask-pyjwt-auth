from flask import jsonify, request
from app.users.model import Users
from app.auth.auths import Auth
from .. import common
from .. import config
import uuid

def init_api(app):
    @app.route('/register', methods=['POST'])
    def register():
        """
        用户注册
        :return: json
        """
        email = request.json['email']
        username = request.json['username']
        password = request.json['password']
        user_id = uuid.uuid5(uuid.NAMESPACE_DNS, config.SECRET_KEY)
        user = Users(email=email, username=username, password=Users.set_password(Users, password), user_id=user_id)
        result = Users.add(Users, user)
        if user.id:
            returnUser = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'login_time': user.login_time,
                'user_id': user.user_id
            }
            return jsonify(common.trueReturn(returnUser, "用户注册成功"))
        else:
            return jsonify(common.falseReturn(result, '用户注册失败'))


    @app.route('/login', methods=['POST'])
    def login():
        """
        用户登录
        :return: json
        """
        username = request.json['username']
        password = request.json['password']
        if (not username or not password):
            return jsonify(common.falseReturn('', '用户名和密码不能为空'))
        else:
            return Auth.authenticate(Auth, username, password)


    @app.route('/userInfo', methods=['GET'])
    def get():
        """
        获取用户信息
        :return: json
        """
        return jsonify(Auth.identify(Auth))
