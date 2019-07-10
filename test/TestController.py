from flask import Blueprint
from flask import request, session
from ..models import User, UserStory, Image, StoryImage, StoryAction, StoryReaction, StoryComment
import json
from sqlalchemy import desc
from ..utils import return_json, login_required
from ..InvalidUsage import InvalidUsage
from .. import utils
from .. import error_messages
import time
from ..extensions import db
from .. import server_constants

test_api = Blueprint('test_api', __name__)

@test_api.route('/test/test')
def test():
    print(utils.get_time_yymmddHHMMSSff())
    return utils.get_time_yymmddHHMMSSff()
