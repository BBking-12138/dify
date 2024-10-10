from flask import Flask

from configs import dify_config
from events import event_handlers  # noqa: F401
from libs.threading import apply_threading_patch
from models import account, dataset, model, source, task, tool, tools, web  # noqa: F401
from server.blueprints_assembly import BluePrintsAssembly
from server.config_assembly import ConfigAssembly
from server.extensions_assembly import ExtensionsAssembly
from server.logger_assembly import LoggerAssembly
from server.module_assembly import PreloadModuleAssembly
from server.security_assembly import SecurityAssembly
from server.timezone_assembly import TimezoneAssembly


def create_app() -> Flask:
    dify_app = Flask(__name__)

    assemblies = [
        ConfigAssembly,
        TimezoneAssembly,
        LoggerAssembly,
        SecurityAssembly,
        PreloadModuleAssembly,
        ExtensionsAssembly,
        BluePrintsAssembly,
    ]
    for assem in assemblies:
        assem().prepare_app(dify_app)

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
