from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import TipSerializer

from ..services.get_tips_service import get_tips_service


class TipsIndexView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request: Request):
    try:
      tips = get_tips_service({'order__lte': request.user.tip_of_day.order})[
          'data'].all()

      return Response(TipSerializer(tips, many=True).data, 200)
    except Exception as e:
      return Response({"error": {"message": str(e)}}, 500)
