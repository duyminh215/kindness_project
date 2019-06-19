from flask import Blueprint
from flask import request, session
from ..models import User
import json
from ..utils import return_json, login_required
from ..InvalidUsage import InvalidUsage
from .. import utils
from .. import error_messages
import time
from .. import header_constant
from ..extensions import db
from .. import server_constants

account_api = Blueprint('account_api', __name__)

@account_api.route('/login/', methods=['POST'])
@return_json
def login():
    json_data = request.json
    data_input = json_data['input']
    password = json_data['password']
    if utils.is_valid_email(data_input):
        existed_account = User.query.filter_by(email=data_input).first()
    else:
        existed_account = User.query.filter_by(phone=data_input).first()

    if existed_account is None:
        raise InvalidUsage(error_messages.user_not_found)
    
    existed_user = utils.row2dict(existed_account)
    if existed_user['password'] != password:
        raise InvalidUsage(error_messages.password_not_match)
    if existed_user['password'] == password:
        session[server_constants.session_key] = existed_user

    return json.dumps(existed_user)


@account_api.route('/signup/', methods=['POST'])
@return_json
def signup():
    json_data = request.json
    input = json_data['input']
    full_name = json_data['full_name']
    password = json_data['password']

    if utils.is_valid_email(input):
        existed_account = User.query.filter_by(email=input).first()
        if existed_account:
            raise InvalidUsage(error_messages.existed_email)

    existed_account = User.query.filter_by(phone=input).first()
    if existed_account:
        raise InvalidUsage(error_messages.existed_phone)

    push_token = request.headers.get(header_constant.push_token)
    unique_device_id = request.headers.get(header_constant.unique_device_id)

    user = User()
    user.full_name = full_name
    user.password = password
    user.created_time = time.time()
    user.updated_time = time.time()
    user.push_token = push_token
    user.device_id = unique_device_id
    if utils.is_valid_email(input):
        user.email = input
    else:
        user.phone = input

    db.session.add(user)
    db.session.commit()

    return json.dumps(utils.row2dict(user))

@account_api.route('/user/info')
@login_required
@return_json
def get_user_info():
    user_session_info = session[server_constants.session_key]
    return json.dumps(user_session_info)


@account_api.route('/logout')
@login_required
@return_json
def logout():
    # remove the username from the session if it's there
    session.pop(server_constants.session_key, None)
    return json.dumps(error_messages.logout_success)
