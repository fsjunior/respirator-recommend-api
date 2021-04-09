from urllib.parse import unquote

from flask.views import MethodView
from flask_smorest import Blueprint

from app.api.business.respirator import RespiratorExtractor
from app.api.schema.respirator import RespiratorQueryArgsSchema, RespiratorSchema
from app.cache import cache
from app.model.respirator import Respirator

api = Blueprint(
    "Respirator API",
    __name__,
    url_prefix="/api/v1/respirator",
    description="In this API you can send the URL of the respirator to be analyzed.",
)


@api.route("")
class RespiratorView(MethodView):
    @classmethod
    @api.arguments(RespiratorQueryArgsSchema, location="query")
    @api.response(RespiratorSchema())
    @cache.memoize(timeout=600)
    def post(cls, respirator_args: dict):
        """List """

        respirator_args["url"] = unquote(respirator_args["url"])

        # Search for a previous cached analysis
        result = Respirator.objects(**respirator_args).first()

        if result is None or (result.respirator_type is not None and result.approval_certificate is None):
            result = RespiratorExtractor(**respirator_args).analyze_website()
            result.save()

        return result
