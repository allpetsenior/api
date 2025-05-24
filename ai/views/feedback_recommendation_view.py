import traceback

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from v0.errors.app_error import App_Error
from ai.services.create_feedback_recommendation_service import create_feedback_recommendation_service
from ai.services.get_feedback_by_recommendation_id_service import get_feedback_by_recommendation_id


class FeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, recommendation_id):
        try:
            feedback = request.data.get("feedback")

            exists_recommendation = get_feedback_by_recommendation_id(
                recommendation_id)

            if exists_recommendation:
                return Response(None, 200)

            create_feedback_recommendation_service(
                {**feedback, "recommendation_id": recommendation_id})

            return Response(None, 201)

        except App_Error as e:
            traceback.print_exception(e)
            return Response(e.toHttp(), e.status)
        except Exception as e:
            traceback.print_exception(e)
            return Response({"error": {"message": str(e)}}, 500)
