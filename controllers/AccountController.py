from flask import Blueprint
from flask import request, session
from ..models import User
import json
from ..utils import return_json
from ..InvalidUsage import InvalidUsage
from .. import utils
from .. import error_messages

account_api = Blueprint('account_api', __name__)

@account_api.route('/login/', methods=['POST'])
@return_json
def login():
    json_data = request.json
    phone = json_data['phone']
    password = json_data['password']
    existed_user_phone_result = User.query.filter_by(phone='phone').first()
    if existed_user_phone_result is None:
        raise InvalidUsage(error_messages.phone_not_found)
    
    existed_user = utils.row2dict(existed_user_phone_result)
    if  existed_user['password'] != password:
        raise InvalidUsage(error_messages.password_not_match)
    if  existed_user['password'] == password:
        session['user_session'] = existed_user

    return json.dumps(existed_user)


@account_api.route('/signup/', methods=['POST'])
@return_json
def signup():
    json_data = request.json
    phone = json_data['phone']
    full_name = json_data['full_name']
    password = json_data['password']
    



@account_api.route('/logout')
@return_json
def logout():
    # remove the username from the session if it's there
    session.pop('user_session', None)
    return 'Bạn đã logout rồi'
