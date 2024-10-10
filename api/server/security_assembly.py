from flask import Flask

from configs import dify_config
from server.basic_assembly import BasicAssembly


class SecurityAssembly(BasicAssembly):
    def prepare_app(self, app: Flask):
        prepare_secret_key(app)


def prepare_secret_key(app: Flask):
    app.secret_key = dify_config.SECRET_KEY
