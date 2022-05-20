import jwt
from . import config
def trueReturn(data, msg):
    return {
        "status": True,
        "data": data,
        "msg": msg,
        "code": 200
    }


def falseReturn(data=None, msg='', code=500):
    return {
        "status": False,
        "data": data,
        "msg": msg,
        "code": code
    }

def decode_auth_token(auth_token):
    """
    验证Token
    :param auth_token:
    :return: integer|string
    """
    try:
        # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
        # 取消过期时间验证
        payload = jwt.decode(auth_token, config.SECRET_KEY, algorithms=["HS256"])
        print(str(payload))
        if ('data' in payload and 'id' in payload['data']):
            return payload
        else:
            raise jwt.InvalidTokenError
    except jwt.ExpiredSignatureError:
        return 'Token过期'
    except jwt.InvalidTokenError:
        return '无效Token'
