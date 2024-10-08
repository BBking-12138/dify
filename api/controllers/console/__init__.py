from flask import Blueprint

from libs.external_api import ExternalApi

from . import admin, apikey, extension, feature, ping, setup, version
from .app import (
    advanced_prompt_template,
    agent,
    annotation,
    app,
    audio,
    completion,
    conversation,
    conversation_variables,
    generator,
    message,
    model_config,
    ops_trace,
    site,
    statistic,
    workflow,
    workflow_app_log,
    workflow_run,
    workflow_statistic,
)
from .auth import activate, data_source_bearer_auth, data_source_oauth, forgot_password, login, oauth
from .billing import billing
from .datasets import (
    data_source,
    datasets,
    datasets_document,
    datasets_segments,
    external,
    file,
    hit_testing,
    test_external,
    website,
)
from .explore import (
    audio,
    completion,
    conversation,
    installed_app,
    message,
    parameter,
    recommended_app,
    saved_message,
    workflow,
)
from .tag import tags
from .workspace import account, load_balancing_config, members, model_providers, models, tool_providers, workspace

bp = Blueprint("console", __name__, url_prefix="/console/api")
api = ExternalApi(bp)

# Import other controllers

# Import app controllers

# Import auth controllers

# Import billing controllers

# Import datasets controllers

# Import explore controllers

# Import tag controllers

# Import workspace controllers
