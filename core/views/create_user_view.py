import traceback

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from core.serializers import UserSerializer
from core.services.create_user_service import create_user_service
from core.services.get_user_service import get_user_service
from core.services.get_token_by_user import get_token_by_user_service

from v0.errors.app_error import App_Error


@api_view(["POST"])
@permission_classes([])
def create_user_view(request):
    try:
        user_already_exists = get_user_service(
            request.data)

        if user_already_exists["user"] is not None:
            return Response({"error": {"message": "User already exists"}}, 405)

        data = create_user_service(request.data)
        token = get_token_by_user_service(data["user"])
        user_serializer = UserSerializer(data["user"])

        return Response({"token": token["data"].key, "user": user_serializer.data}, 201)

    except App_Error as e:
        traceback.print_exception(e)
        return Response(e.toHttp(), e.status)
    except Exception as e:
        traceback.print_exception(e)
        return Response({"error": {"message": str(e)}}, 500)
