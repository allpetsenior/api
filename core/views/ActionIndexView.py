from datetime import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.services.create_action_service import create_action_service


class ActionIndexView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request: Request):
    try:
      data = request.data
      user = request.user

      create_action_service({
        **data,
        'user': user,
        'created_at': datetime.now(),
        'ip': request.META.get('REMOTE_ADDR'),
      })

      return Response({'data': True}, 200)
    except Exception as e:
      return Response({"error": {"message": str(e)}}, 500)
