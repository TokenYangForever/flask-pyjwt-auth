import jwt, datetime, time
from flask import jsonify, g
from app.users.model import Users
from .. import config
from .. import common

class Auth():
    @staticmethod
    def encode_auth_token(user_id, login_time):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=60000),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def authenticate(self, username, password):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param password:
        :return: json
        """
        userInfo = Users.query.filter_by(username=username).first()
        if (userInfo is None):
            return jsonify(common.falseReturn('', '找不到用户'))
        else:
            if (Users.check_password(Users, userInfo.password, password)):
                try:
                    login_time = int(time.time())
                    print('login_time', login_time)
                    userInfo.login_time = login_time
                    # userInfo.email = "1234@test.com"
                    Users.update(Users, userInfo)
                    token = self.encode_auth_token(userInfo.user_id, login_time)
                    return jsonify(common.trueReturn(token, '登录成功'))
                except Exception as err:
                    return jsonify(common.trueReturn(str(err), '登录失败'))
            else:
                return jsonify(common.falseReturn('', '密码不正确'))

    def identify(self):
        """
        用户鉴权
        :return: list
        """
        user = Users.get(Users, g.user_id)
        if (user is None):
            result = common.falseReturn('', '找不到该用户信息', code=401)
        else:
            if (user.login_time == g.login_time):
                result = common.trueReturn(
                    {
                        "email": user.email,
                    },
                    '请求成功'
                )
            else:
                result = common.falseReturn('', 'Token已更改，请重新登录获取', code=401)
        return result
