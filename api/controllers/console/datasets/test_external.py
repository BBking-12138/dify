from flask_restful import Resource, reqparse

from controllers.console import api
from services.external_knowledge_service import ExternalDatasetService


class TestExternalApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("retrieval_setting", nullable=False, required=True, type=dict, location="json")
        parser.add_argument(
            "query",
            nullable=False,
            required=True,
            type=str,
        )
        parser.add_argument(
            "knowledge_id",
            nullable=False,
            required=True,
            type=str,
        )
        args = parser.parse_args()
        result = ExternalDatasetService.test_external_knowledge_retrieval(
            args["retrieval_setting"], args["query"], args["knowledge_id"]
        )
        return result, 200


api.add_resource(TestExternalApi, "/retrieval")
