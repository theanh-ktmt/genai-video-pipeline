import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from flask import Flask
from flask_cors import CORS
from loguru import logger
from dotenv import load_dotenv
from src.utils.server_args import ARGS
from src.routes import register_routes

# initialize Flask app
app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


def main():
    # load API key from .env file
    load_dotenv()

    # register API routes
    logger.info("Registering API routes...")
    register_routes(app)

    # launch the app
    logger.success(f"App is running on port {ARGS.port}...")
    app.run(host=ARGS.host, port=ARGS.port, threaded=True)


# Run
main()
