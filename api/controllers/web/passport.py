import uuid

from flask import request
from flask_restful import Resource
from werkzeug.exceptions import NotFound, Unauthorized

from controllers.web import api
from controllers.web.error import WebSSOTokenInvalidError
from extensions.ext_database import db
from libs.passport import PassportService
from models.model import App, EndUser, Site
from services.enterprise.enterprise_feature_service import EnterpriseFeatureService


class PassportResource(Resource):
    """Base resource for passport."""
    def get(self):
        # Enterprise feature: SSO enforced for web
        end_user_session_id = ''
        enterprise_features = EnterpriseFeatureService.get_enterprise_features()
        if enterprise_features.sso_enforced_for_web:
            web_sso_token = request.headers.get('X-Web-SSO-Token')
            if not web_sso_token:
                raise WebSSOTokenInvalidError()
            try:
                web_sso_token_decode = PassportService().verify(web_sso_token)
                end_user_session_id = web_sso_token_decode.get('end_user_session_id')
            except Unauthorized:
                raise WebSSOTokenInvalidError()

        app_code = request.headers.get('X-App-Code')
        if app_code is None:
            raise Unauthorized('X-App-Code header is missing.')

        # get site from db and check if it is normal
        site = db.session.query(Site).filter(
            Site.code == app_code,
            Site.status == 'normal'
        ).first()
        if not site:
            raise NotFound()
        # get app from db and check if it is normal and enable_site
        app_model = db.session.query(App).filter(App.id == site.app_id).first()
        if not app_model or app_model.status != 'normal' or not app_model.enable_site:
            raise NotFound()
        
        end_user = EndUser(
            tenant_id=app_model.tenant_id,
            app_id=app_model.id,
            type='browser',
            is_anonymous=True,
            session_id=generate_session_id(),
        )

        if enterprise_features.sso_enforced_for_web:
            end_user.session_id = end_user_session_id

        db.session.add(end_user)
        db.session.commit()

        payload = {
            "iss": site.app_id,
            'sub': 'Web API Passport',
            'app_id': site.app_id,
            'app_code': app_code,
            'end_user_id': end_user.id,
        }

        tk = PassportService().issue(payload)

        return {
            'access_token': tk,
        }


api.add_resource(PassportResource, '/passport')


def generate_session_id():
    """
    Generate a unique session ID.
    """
    while True:
        session_id = str(uuid.uuid4())
        existing_count = db.session.query(EndUser) \
            .filter(EndUser.session_id == session_id).count()
        if existing_count == 0:
            return session_id
