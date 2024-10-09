from flask import Flask

from configs import dify_config


def prepare_secret_key(dify_app: Flask):
    dify_app.secret_key = dify_config.SECRET_KEY
