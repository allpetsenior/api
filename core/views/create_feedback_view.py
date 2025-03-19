import traceback

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from core.serializers import FeedbackSerializer
from core.services.create_feedback_service import create_feedback_service
from v0.errors.app_error import App_Error


@api_view(["POST"])
@permission_classes([])
def create_feedback_view(request):
  try:
    data = create_feedback_service({**request.data, 'user': request.user})
    feedback_serializer = FeedbackSerializer(data['feedback'])

    return Response({"feedback": feedback_serializer.data}, 201)

  except App_Error as e:
    traceback.print_exception(e)
    return Response(e.toHttp(), e.status)
  except Exception as e:
    traceback.print_exception(e)
    return Response({"error": {"message": str(e)}}, 500)
