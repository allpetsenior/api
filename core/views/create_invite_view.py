import traceback

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from core.serializers import InviteSerializer
from core.services.create_invite_service import create_invite_service
from v0.errors.app_error import App_Error


@api_view(["POST"])
@permission_classes([])
def create_invite_view(request):
  try:
    data = create_invite_service({**request.data, 'user': request.user})
    invite_serializer = InviteSerializer(data['invite'])

    return Response({"invite": invite_serializer.data}, 201)

  except App_Error as e:
    traceback.print_exception(e)
    return Response(e.toHttp(), e.status)
  except Exception as e:
    traceback.print_exception(e)
    return Response({"error": {"message": str(e)}}, 500)
