from flask import Blueprint
from flask import request, session
from ..models import KindnessFeed, User, UserStory, Image, StoryImage, StoryAction, StoryReaction, StoryComment
import json
from sqlalchemy import desc
from sqlalchemy.orm import load_only
from ..utils import return_json, login_required
from ..InvalidUsage import InvalidUsage
from .. import utils
from .. import error_messages
import time
from ..extensions import db
from .. import server_constants
from .. import feed_item_types

feed_api = Blueprint('feed_api', __name__)


@feed_api.route('/feed/get')
@login_required
@return_json
def get_feed():
    page = 1
    if 'page' in request.args:
        page = int(request.args.get('page'))

    length = server_constants.number_of_feed_item_per_page
    start_number = (page - 1) * length
    to_number = start_number + length

    user_session_info = session[server_constants.session_key]
    user_id = user_session_info['id']

    feed_items_result = KindnessFeed.query.\
        filter_by(user_id=user_id).order_by(desc(KindnessFeed.inserted_time)).slice(start_number, to_number)

    number_of_feed_items = KindnessFeed.query.filter_by(user_id=user_id).count()

    story_ids = []
    comment_ids = []
    react_ids = []
    source_user_ids = []
    feed_items = []

    for item in feed_items_result:
        feed_item = utils.row2dict(item)

        feed_items.append(feed_item)

        if feed_item['item_type'] == feed_item_types.type_create_story or\
                feed_item['item_type'] == feed_item_types.type_suggest_story:
            story_ids.append(feed_item['item_id'])

        if feed_item['item_type'] == feed_item_types.type_comment_story:
            comment_ids.append(feed_item['item_id'])

        if feed_item['item_type'] == feed_item_types.type_react_story:
            react_ids.append(feed_item['item_id'])

    story_comments_result = StoryComment.query.filter(StoryComment.id.in_(comment_ids))
    story_comments_dict = {}
    for item in story_comments_result:
        comment_item = utils.row2dict(item)
        story_comments_dict[comment_item['id']] = comment_item

        story_ids.append(comment_item['story_id'])
        source_user_ids.append(comment_item['user_id'])

    story_reactions_result = StoryReaction.query.filter(StoryReaction.id.in_(react_ids))
    story_reactions_dict = {}
    for item in story_reactions_result:
        reaction_item = utils.row2dict(item)
        story_reactions_dict[reaction_item['id']] = reaction_item

        story_ids.append(reaction_item['story_id'])
        source_user_ids.append(reaction_item['user_id'])

    stories_result = UserStory.query.filter(UserStory.id.in_(story_ids))
    stories_dict = {}
    for item in stories_result:
        story_item = utils.row2dict(item)
        stories_dict[story_item['id']] = story_item
        source_user_ids.append(story_item['user_id'])

    users_dict = {}
    users_result = User.query.with_entities(User.id, User.full_name, User.avatar).filter(User.id.in_(source_user_ids))
    for item in users_result:
        user_item = utils.user_array_to_dict(item)
        users_dict[user_item['id']] = user_item
        print(users_dict)

    feeds_data = []
    for item in feed_items:
        if item['item_type'] == feed_item_types.type_create_story or \
                item['item_type'] == feed_item_types.type_suggest_story:
            story_item = stories_dict[item['item_id']]
            creator_of_story = users_dict[story_item['user_id']]
            feed_data = {'story': story_item, 'creator': creator_of_story, 'data_type': item['item_type']}

        if item['item_type'] == feed_item_types.type_react_story:
            reaction_item = story_reactions_dict[item['item_id']]
            story_item = stories_dict[reaction_item['story_id']]
            creator_of_story = users_dict[story_item['user_id']]
            reaction_user = users_dict[reaction_item['user_id']]

            feed_data = {'story': story_item, 'creator': creator_of_story, 'data_type': item['item_type'],
                         'reaction': reaction_item, 'reaction_user': reaction_user}

        if item['item_type'] == feed_item_types.type_comment_story:
            comment_item = story_comments_dict[item['item_id']]
            story_item = stories_dict[comment_item['story_id']]
            creator_of_story = users_dict[story_item['user_id']]
            commented_user = users_dict[comment_item['user_id']]

            feed_data = {'story': story_item, 'creator': creator_of_story, 'data_type': item['item_type'],
                         'comment': comment_item, 'commented_user': commented_user}

        feeds_data.append(feed_data)

    response = {'feeds': feeds_data, 'number_of_item': number_of_feed_items}
    return json.dumps(response)
