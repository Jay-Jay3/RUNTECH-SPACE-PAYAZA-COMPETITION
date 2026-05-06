from flask import request, jsonify
from functools import wraps

def unified_data(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 1. Extract JSON or Form data
        if request.is_json:
            data = request.get_json()
        elif request.form:
            data = request.form.to_dict()
        else:
            data = request.args.to_dict() # Optional: include URL params

        # 2. Inject 'data' into the route function's arguments
        return f(data, *args, **kwargs)
    
    return decorated_function
