from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Tip, User
from core.serializers import TipSerializer
from core.services import get_user_service

from ..services.get_tip_service import get_tip_service


class TipsIndexView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request: Request):
    try:
      tip = get_tip_service({'id': request.user.tip_of_day.id})[
          'data'].first()

      return Response(TipSerializer(tip).data, 200)
    except Exception as e:
      return Response({"error": {"message": str(e)}}, 500)
