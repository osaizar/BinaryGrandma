from functools import wraps
from flask import jsonify, request, abort

def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            js = request.json
            if js == None:
                raise Exception
        except:
            return jsonify({"error": "Incorrect request"}), 400
        return f(*args, **kw)
    return wrapper


def validate_token(f):
    @wraps(f)
    def wrapper(*args, **kw):
        return f(*args, **kw)
    return wrapper


def validate_schema(name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                validate(request.json, name)
            except Exception as e:
                return jsonify({"error": e.message}), 400
            return f(*args, **kw)
        return wrapper
    return decorator


def validate(input, name):
    if name == False:
        pass
    else:
        Exception("Ez dago izen hori duen eskemarik")
