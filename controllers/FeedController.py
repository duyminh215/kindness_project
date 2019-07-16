from flask import Blueprint
from flask import request, session
from ..models import KindnessFeed, User, UserStory, Image, StoryImage, StoryShare, StoryReaction, StoryComment
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
    sharing_ids = []
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
        if feed_item['item_type'] == feed_item_types.type_share_story:
            sharing_ids.append(feed_item['item_id'])

    story_images_result = StoryImage.query.join(Image, StoryImage.image_id == Image.id)\
        .with_entities(StoryImage.story_id, Image.id, Image.title, Image.description, Image.image_link, Image.created_time, Image.user_id)\
        .filter(StoryImage.story_id.in_(story_ids))

    story_id_and_picture_map = {}

    for story_image in story_images_result:
        story_image = story_image._asdict()
        story_id = str(story_image['story_id'])

        if story_id in story_id_and_picture_map:
            images_array = story_id_and_picture_map[story_id]
            images_array.append(story_image)
            story_id_and_picture_map[story_id] = images_array
        else:
            images_array = []
            images_array.append(story_image)
            story_id_and_picture_map[story_id] = images_array

    share_story_results = StoryShare.query.filter(StoryShare.id.in_(sharing_ids))
    story_share_dict = {}
    for item in share_story_results:
        share_item = utils.row2dict(item)
        story_share_dict[share_item['id']] = share_item

        story_ids.append(share_item['story_id'])
        source_user_ids.append(share_item['user_id'])

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

    feeds_data = []
    for item in feed_items:
        if item['item_type'] == feed_item_types.type_create_story or \
                item['item_type'] == feed_item_types.type_suggest_story:
            story_item = stories_dict[item['item_id']]
            story_images = []
            if item['item_id'] in story_id_and_picture_map:
                story_images = story_id_and_picture_map[item['item_id']]

            creator_of_story = users_dict[story_item['user_id']]
            feed_data = {'story': story_item, 'creator': creator_of_story,
                         'data_type': item['item_type'], 'story_images': story_images}

        if item['item_type'] == feed_item_types.type_react_story:
            reaction_item = story_reactions_dict[item['item_id']]
            story_item = stories_dict[reaction_item['story_id']]
            story_images = []
            if reaction_item['story_id'] in story_id_and_picture_map:
                story_images = story_id_and_picture_map[reaction_item['story_id']]
            creator_of_story = users_dict[story_item['user_id']]
            reaction_user = users_dict[reaction_item['user_id']]

            feed_data = {'story': story_item, 'creator': creator_of_story, 'data_type': item['item_type'],
                         'reaction': reaction_item, 'reaction_user': reaction_user, 'story_images': story_images}

        if item['item_type'] == feed_item_types.type_comment_story:
            comment_item = story_comments_dict[item['item_id']]
            story_item = stories_dict[comment_item['story_id']]
            if comment_item['story_id'] in story_id_and_picture_map:
                story_images = story_id_and_picture_map[comment_item['story_id']]
            creator_of_story = users_dict[story_item['user_id']]
            commented_user = users_dict[comment_item['user_id']]

            feed_data = {'story': story_item, 'creator': creator_of_story, 'data_type': item['item_type'],
                         'comment': comment_item, 'commented_user': commented_user, 'story_images': story_images}

        if item['item_type'] == feed_item_types.type_share_story:
            share_item = story_share_dict[item['item_id']]
            story_item = stories_dict[share_item['story_id']]
            if share_item['story_id'] in story_id_and_picture_map:
                story_images = story_id_and_picture_map[share_item['story_id']]
            creator_of_story = users_dict[story_item['user_id']]
            sharing_user = users_dict[share_item['user_id']]

            feed_data = {'story': story_item, 'creator': creator_of_story, 'data_type': item['item_type'],
                         'sharing': share_item, 'sharing_user': sharing_user, 'story_images': story_images}

        feeds_data.append(feed_data)

    response = {'feeds': feeds_data, 'number_of_item': number_of_feed_items}
    return json.dumps(response)
