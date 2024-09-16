import logging
import os.path

from flask import Blueprint, render_template, send_from_directory, Response, request

from brighton.services import StoreService

logger = logging.getLogger(__name__)
blueprint = Blueprint('stores', __name__, template_folder='templates')


@blueprint.route("/")
def homepage() -> str:
    """
    Homepage view
    :return:
    """
    return render_template("home.html", feed_url=os.getenv('STORES_LIST_URL'))


@blueprint.route("/stores")
def stores_list() -> str:
    """
    View to re-download list of stores and display them as requested by the challenge
    :return:
    """
    stores = StoreService.get_stores(True)
    return render_template("stores.html", stores=stores)


@blueprint.route('/stores.html')
def stores_html_view() -> Response:
    """
    View to display list of stores as requested by the challenge. Pass url param ?force=1 to re-download stores list and
    recreate the view
    :return:
    """
    current_dir = os.path.dirname(__file__)
    force_download = request.args.get('force', '') == '1'
    # if file does not exist or user requests forced re-creation, create it
    view_exists = os.path.exists(os.path.join(current_dir, 'stores.html'))
    logger.info(f"view_exists = {view_exists} force_download = {force_download}")
    if not view_exists or force_download:
        StoreService.create_stores_list_html_view(force_download)
    return send_from_directory(current_dir, 'stores.html')
