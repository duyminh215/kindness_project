from flask import Blueprint
from flask import request, session
from ..models import User, Image, KindnessAction, KindnessActionImage, UserKindnessActivity
import json
from sqlalchemy import desc
from ..utils import return_json, login_required
from ..InvalidUsage import InvalidUsage
from .. import utils
from .. import error_messages
import time
from ..extensions import db
from .. import server_constants

kindness_action_api = Blueprint('kindness_action_api', __name__)

@kindness_action_api.route('/kindness-action/get')
@return_json
def get_kindness_actions():
    search_string = ""
    if 'query' in request.args:
        search_string = str(request.args.get('query'))

    number_of_item = 0

    if not search_string:
        kindness_actions_result = KindnessAction.query.filter_by(status=1).all()
        number_of_item = KindnessAction.query.filter_by(status=1).count()
    else:
        search_string = '%' + search_string + '%'
        kindness_actions_result = KindnessAction.query. \
            filter(KindnessAction.title.like(search_string)). \
            filter_by(status=1).all()
        number_of_item = KindnessAction.query. \
            filter(KindnessAction.title.like(search_string)). \
            filter_by(status=1).count()

    kindness_actions = []
    for kindness_action in kindness_actions_result:
        kindness_action_dict = utils.row2dict(kindness_action)
        kindness_actions.append(kindness_action_dict)

    result = {'number_of_item': number_of_item, 'items': kindness_actions}

    return json.dumps(result)


@kindness_action_api.route('/kindness-action/create', methods=['POST'])
@login_required
@return_json
def create_kindness_actions():
    json_data = request.json
    user_session_info = session[server_constants.session_key]
    action_title = json_data['title']
    action_content = json_data['content']
    action_images = json_data['images']

    if not action_title:
        raise InvalidUsage(error_messages.kindness_action_title_empty)

    try:
        kindness_action = KindnessAction()
        kindness_action.title = action_title
        kindness_action.content = action_content
        kindness_action.content = server_constants.kindness_action_status_inactive
        kindness_action.created_time = time.time()
        db.session.add(kindness_action)
        db.session.flush()

        user_kindness_activity = UserKindnessActivity()
        user_kindness_activity.user_id = user_session_info.id
        user_kindness_activity.kindness_action_id = kindness_action.id
        user_kindness_activity.activity_title = action_title
        user_kindness_activity.activity_content = action_content
        user_kindness_activity.action_time = time.time()
        db.session.add(user_kindness_activity)
        db.session.flush()

        if action_images:
            for image_url in action_images:
                image_item = Image()
                image_item.title = ""
                image_item.description = ""
                image_item.image_link = image_url
                image_item.status = 0
                image_item.created_time = time.time()

                db.session.add(image_item)
                db.session.flush()

                kindness_action_image = KindnessActionImage()
                kindness_action_image.story_id = kindness_action.id
                kindness_action_image.image_id = image_item.id
                kindness_action_image.created_time = time.time()

                db.session.add(kindness_action_image)
                db.session.flush()

        db.session.commit()

        return json.dumps(utils.row2dict(kindness_action))
    except Exception as e:
        db.session.rollback()
        raise InvalidUsage(error_messages.internal_server_error)
