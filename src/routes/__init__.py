from loguru import logger
from src.routes import generate


def register_routes(app):

    # for check connection
    @app.route("/ping")
    def ping():
        return "PONG!"

    # Register generate sub-module
    logger.info("Register 'generate' module...")
    app.register_blueprint(generate.module, url_prefix="/generate")

    # TODO: Other sub-modules can be registered here
