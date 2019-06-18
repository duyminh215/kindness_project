from flask import Blueprint
from flask import request, session
import json
from ..models import ClientSetting, ServerSetting
from .. import utils
from ..utils import return_json

resource_api = Blueprint('resource_api_', __name__)

@resource_api.route('/client/settings')
@return_json
def list_all_client_settings():
    client_settings_result = ClientSetting.query.all()
    settings = []
    for row in client_settings_result:
        settings.append(utils.row2dict(row))
    return json.dumps(settings)