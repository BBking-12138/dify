from flask import Flask


def preload_modules(app: Flask):
    from events import event_handlers  # noqa: F401
    from models import account, dataset, model, source, task, tool, tools, web  # noqa: F401
