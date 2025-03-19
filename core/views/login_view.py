import traceback

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from core.services.get_user_service import get_user_service
from core.services.get_token_by_user import get_token_by_user_service
from core.serializers import UserSerializer

from v0.errors.app_error import App_Error


@api_view(["POST"])
@permission_classes([])
def login_view(request):
    try:
        data = get_user_service(
            {"email": request.data["email"]})

        if data["user"] is None:
            return Response({"error": {"message": "Credentials are invalid"}}, 404)

        if data["user"].check_password(request.data["password"]) == False:
            return Response({"error": {"message": "Credentials are invalid"}}, 404)

        token = get_token_by_user_service(data["user"])
        user_serializer = UserSerializer(data["user"])

        return Response({"token": token["data"].key, "user": user_serializer.data}, 201)

    except App_Error as e:
        traceback.print_exception(e)
        return Response(e.toHttp(), e.status)
    except Exception as e:
        traceback.print_exception(e)
        return Response({"error": {"message": str(e)}}, 500)
