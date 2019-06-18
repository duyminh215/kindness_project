from flask import Blueprint
from flask import request, session
import json
from ..utils import return_json

account_api = Blueprint('account_api', __name__)

@account_api.route('/login/', methods=['POST'])
@return_json
def login():
    json_data = request.json
    phone = json_data['phone']
    password = json_data['password']

    if phone == '0981713034' and password == '826dabf6e74e583ffbfccb2c7cab747d':
        session['phone'] = json_data
        return 'Bạn đã đăng nhập thành công'

    return json.dumps(json_data)

@account_api.route('/session/test')
@return_json
def test_session():
    if 'phone' in session:
        return 'Bạn đã login rồi'
    return 'Bạn chưa login'

@account_api.route('/logout')
@return_json
def logout():
    # remove the username from the session if it's there
    session.pop('phone', None)
    return 'Bạn đã logout rồi'
