from flask import Flask

from commands import register_commands
from configs import dify_config
from events import event_handlers  # noqa: F401
from libs.threading import apply_threading_patch
from models import account, dataset, model, source, task, tool, tools, web  # noqa: F401
from server.blueprints_kit import register_blueprints
from server.config_kit import prepare_flask_configs
from server.extensions_kit import initialize_extensions
from server.logger_kit import prepare_logging, prepare_warnings
from server.module_kit import preload_modules
from server.security_kit import prepare_secret_key


def create_app() -> Flask:
    dify_app = Flask(__name__)

    preload_modules(dify_app)
    prepare_flask_configs(dify_app)
    prepare_secret_key(dify_app)
    prepare_warnings(dify_app)
    prepare_logging(dify_app)
    initialize_extensions(dify_app)
    register_blueprints(dify_app)
    register_commands(dify_app)

    return dify_app


# create app
app = create_app()
celery = app.extensions["celery"]

if __name__ == "__main__":
    if dify_config.DEBUG:
        apply_threading_patch()

    if dify_config.TESTING:
        print("App is running in TESTING mode")

    app.run(host="0.0.0.0", port=5001)
