from flask import Blueprint
from flask import request, session
from ..models import User, Following
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

    push_token = request.headers.get(header_constant.push_token)
    unique_device_id = request.headers.get(header_constant.unique_device_id)

    existed_account.push_token = push_token
    existed_account.device_id = unique_device_id

    same_device_users = User.query.filter_by(device_id=unique_device_id).all()
    if same_device_users:
        for user in same_device_users:
            user.device_id = ""

    db.session.commit()

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
    try:
        user = User()
        user.full_name = full_name
        user.created_time = time.time()
        user.updated_time = time.time()
        user.push_token = push_token
        user.device_id = unique_device_id
        user.password = password
        if utils.is_valid_email(input):
            user.email = input
        else:
            user.phone = input

        db.session.add(user)
        db.session.commit()
        return json.dumps(utils.row2dict(user))
    except Exception as e:
        db.session.rollback()
        raise InvalidUsage(error_messages.internal_server_error)


@account_api.route('/user/info')
@login_required
@return_json
def get_user_info():
    user_session_info = session[server_constants.session_key]
    user_info_result = User.query.filter_by(id=user_session_info['id']).first()
    user_info = utils.row2dict(user_info_result)
    return json.dumps(user_info)


@account_api.route('/user/follow', methods=['POST'])
@login_required
@return_json
def follow_user():
    user_session_info = session[server_constants.session_key]
    user_info_result = User.query.filter_by(id=user_session_info['id']).first()

    json_data = request.json
    follower_id = json_data['follower_id']

    follower_user = User.query.filter_by(id=follower_id).first()
    if not follower_user:
        raise InvalidUsage(error_messages.follower_not_found)

    user_info = utils.row2dict(user_info_result)
    follower_user = utils.row2dict(follower_user)
    if user_info['id'] == follower_user['id']:
        raise InvalidUsage(error_messages.following_yourself)

    existed_following = Following().query\
        .filter_by(user_id=user_session_info['id'])\
        .filter_by(following_user_id=follower_id).first()

    if existed_following:
        return json.dumps(user_info)

    follow_status = server_constants.following_status_done
    if int(follower_user['is_confirm_follower']) == server_constants.is_confirm_following_yes:
        follow_status = server_constants.following_status_requesting

    following = Following()
    following.user_id = user_session_info['id']
    following.following_user_id = follower_user['id']
    following.inserted_time = time.time()
    following.status = follow_status
    following.updated_time = time.time()

    db.session.add(following)
    db.session.commit()

    return json.dumps(user_info)


@account_api.route('/logout')
@login_required
@return_json
def logout():
    # remove the username from the session if it's there
    session.pop(server_constants.session_key, None)
    return json.dumps(error_messages.logout_success)
