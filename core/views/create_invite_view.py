import traceback

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from core.services.create_invite_service import create_invite_service
from core.services.get_invite_service import get_invite_service
from v0.errors.app_error import App_Error


@api_view(["POST"])
@permission_classes([])
def create_invite_view(request):
  try:
    if get_invite_service({'email': request.data.get('email')}).get('invite') is not None:
      return Response({'error': {"message": "Convite já enviado"}}, 400)

    create_invite_service({**request.data, 'user': request.user})
    return Response({"message": "Obrigada pela indicação! Avisaremos ao seu contato assim que o acesso for liberado!"}, 201)

  except App_Error as e:
    traceback.print_exception(e)
    return Response(e.toHttp(), e.status)
  except Exception as e:
    traceback.print_exception(e)
    return Response({"error": {"message": str(e)}}, 500)
