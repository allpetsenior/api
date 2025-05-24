
import traceback
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from analytics.repositories.analytics_repository import AnalyticsRepository
from analytics.services.create_analytic_metadata_service import CreateAnalyticMetadata
from v0.errors.app_error import App_Error

AnalyticsRepo = AnalyticsRepository()
CreateMetadata = CreateAnalyticMetadata(AnalyticsRepo)


class IndexView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        try:
            payload = dict()
            payload["metadata"] = request.data
            payload["user"] = request.user

            CreateMetadata.execute(payload)

            return Response(None, 201)
        except App_Error as e:
            traceback.print_exception(e)
            return Response(e.toHttp(), e.status)
        except Exception as e:
            traceback.print_exception(e)
            return Response({"error": {"message": str(e)}}, 500)
