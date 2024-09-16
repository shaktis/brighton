import logging.config

from flask import Flask

import brighton.settings as settings

logger = logging.getLogger(__name__)


def create_app():
    """Application factory

    """
    # configure logging
    logging.config.dictConfig(settings.LOGGING_CONFIG)

    # create app
    app = Flask("brighton")
    app.config.from_object('brighton.settings')

    # register routes
    import brighton.controller
    app.register_blueprint(brighton.controller.blueprint)

    # run 1-time code
    with app.app_context():
        logger.info("Executing server startup tasks...")
        from brighton.services import StoreService
        StoreService.print_store_count_by_state()
        StoreService.create_stores_list_html_view()
    return app
