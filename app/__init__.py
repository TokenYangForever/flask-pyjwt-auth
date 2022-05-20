from ast import Str
from unittest.mock import patch
from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from . import common
db = SQLAlchemy()

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response

    @app.before_request
    def before_request():
        if (request.path == '/login' or request.path == '/register'):
            return None
        else:
            auth_header = request.headers.get('Authorization')
            if (not auth_header):
                return jsonify(common.falseReturn(msg="未登录", code=401))
            else:
                payload = common.decode_auth_token(auth_header)
                # return payload
                if (isinstance(payload, str)): 
                    return jsonify(common.falseReturn(msg=payload, code=401))
                g.user_id = payload.id
                g.login_time = payload.login_time
            return None

    from app.users.model import db
    db.init_app(app)

    from app.users.api import init_api
    init_api(app)

    return app
