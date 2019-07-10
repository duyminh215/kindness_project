from flask import Blueprint, request, send_from_directory
import json
from ..models import ClientSetting, ServerSetting, Image
from .. import utils
from ..utils import return_json
from .. import server_constants, error_messages
from ..InvalidUsage import InvalidUsage
import os

resource_api = Blueprint('resource_api_', __name__)


@resource_api.route('/client/settings')
@return_json
def list_all_client_settings():
    client_settings_result = ClientSetting.query.all()
    settings = []
    for row in client_settings_result:
        settings.append(utils.row2dict(row))
    return json.dumps(settings)


@resource_api.route('/image/upload-by-form', methods=['POST'])
@return_json
def upload_images_by_form():

    uploaded_file_paths = []
    uploaded_files = request.files.getlist("images[]")
    for upload_file in uploaded_files:
        upload_file_name = upload_file.filename
        file_name, file_extension = os.path.splitext(upload_file_name)
        if file_name == '':
            raise InvalidUsage(error_messages.invalid_file)
        if file_extension not in server_constants.ALLOWED_EXTENSIONS:
            raise InvalidUsage(error_messages.extension_not_allowed)

        today_folder = server_constants.images_storage_file_path + "/" + utils.get_date_yymmdd()
        current_file_path = today_folder + "/" + server_constants.image_prefix_name + \
                            utils.get_time_yymmddHHMMSSff() + file_extension
        public_file_path = server_constants.public_images_storage_path + "/" + server_constants.image_prefix_name + \
                            utils.get_time_yymmddHHMMSSff() + file_extension
        if not os.path.exists(today_folder):
            os.makedirs(today_folder)
        upload_file.save(current_file_path)

        uploaded_file_paths.append(public_file_path)

    return json.dumps(uploaded_file_paths)


@resource_api.route('/storages/<path:path>')
def send_storage(path):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'storages'), path)




