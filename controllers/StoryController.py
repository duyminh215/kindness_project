from flask import Blueprint
from flask import request, session
from ..models import User, UserStory, Image, StoryImage, StoryAction, StoryReaction
import json
from ..utils import return_json, login_required
from ..InvalidUsage import InvalidUsage
from .. import utils
from .. import error_messages
import time
from ..extensions import db
from .. import server_constants

story_api = Blueprint('story_api', __name__)

@story_api.route('/story/create', methods=['POST'])
@login_required
@return_json
def create_story():
    json_data = request.json
    user_session_info = session[server_constants.session_key]

    title = json_data['title']
    if not title:
        raise InvalidUsage(error_messages.empty_user_story_title)

    content = json_data['content']
    if not content:
        raise InvalidUsage(error_messages.empty_user_story_content)

    image_urls = []
    if 'images' in json_data:
        image_urls = json_data['images']

    action_ids = []
    if 'action_ids' in json_data:
        action_ids = json_data['action_ids']

    try:

        user_story = UserStory()
        user_story.title = title
        user_story.content = content
        user_story.user_id = user_session_info['id']
        user_story.status = 0
        user_story.created_time = time.time()

        db.session.add(user_story)
        db.session.flush()

        if image_urls:
            for image_url in image_urls:
                image_item = Image()
                image_item.title = ""
                image_item.description = ""
                image_item.image_link = image_url
                image_item.status = 0
                image_item.created_time = time.time()

                db.session.add(image_item)
                db.session.flush()

                story_image = StoryImage()
                story_image.story_id = user_story.id
                story_image.image_id = image_item.id
                story_image.inserted_time = time.time()

                db.session.add(story_image)
                db.session.flush()

        if action_ids:
            for action_id in action_ids:

                story_action = StoryAction()
                story_action.story_id = user_story.id
                story_action.action_id = action_id
                story_action.created_time = time.time()

                db.session.add(story_action)
                db.session.flush()

        db.session.commit()

        return json.dumps(utils.row2dict(user_story))
    except Exception as e:
        db.session.rollback()
        raise InvalidUsage(error_messages.internal_server_error)


@story_api.route('/story/react', methods=['POST'])
@login_required
@return_json
def react_story():
    json_data = request.json
    user_session_info = session[server_constants.session_key]
    story_id = json_data['story_id']
    reaction_id = json_data['reaction_id']

    # import pdb
    # pdb.set_trace()

    if reaction_id != server_constants.action_like and reaction_id != server_constants.action_dislike:
        raise InvalidUsage(error_messages.reaction_story_not_found)

    user_story = UserStory.query.filter_by(id=story_id).first()
    if not user_story:
        raise InvalidUsage(error_messages.user_story_not_found)
    user_story_dict = utils.row2dict(user_story)


    try:
        story_reaction = StoryReaction()
        story_reaction.story_id = story_id
        story_reaction.reaction_id = reaction_id
        story_reaction.user_id = user_session_info['id']
        story_reaction.reaction_time = time.time()
        story_reaction.status = 0

        db.session.add(story_reaction)
        db.session.flush()

        if reaction_id == server_constants.action_like:
            number_of_like = user_story_dict['number_of_like']
            number_of_like = number_of_like + 1

            user_story.number_of_like = number_of_like

        if reaction_id == server_constants.action_dislike:
            number_of_dislike = user_story_dict['number_of_dislike']
            number_of_dislike = number_of_dislike + 1

            user_story.number_of_dislike = number_of_dislike

        db.session.commit()

        return json.dumps(utils.row2dict(story_reaction))
    except Exception as e:
        print(e)
        db.session.rollback()
        raise InvalidUsage(error_messages.internal_server_error)
