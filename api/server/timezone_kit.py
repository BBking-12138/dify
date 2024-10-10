import os
import time

from flask import Flask


def prepare_timezone(app: Flask):
    os.environ["TZ"] = "UTC"
    # windows platform not support tzset
    if hasattr(time, "tzset"):
        time.tzset()
