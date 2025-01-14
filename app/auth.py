from functools import wraps
from flask import request, jsonify, current_app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        import ipdb
        ipdb.set_trace()

        if 'token' in request.args:
            token = request.args['token']

        if not token or token != current_app.config['SECRET_KEY']:
            return jsonify({'message': 'Token inválido ou ausente!'}), 401

        return f(*args, **kwargs)
    return decorated
