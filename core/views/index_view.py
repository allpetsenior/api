import traceback

from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import AuthEmail
from core.serializers import UserSerializer
from core.services.create_user_service import create_user_service
from core.services.get_tip_service import get_tip_service
from core.services.get_token_by_user import get_token_by_user_service
from core.services.get_user_service import get_user_service
from core.services.update_user_service import update_user_service
from v0.errors.app_error import App_Error


def get_auth_email(email):
    try:
        return AuthEmail.objects.get(email=email)
    except AuthEmail.DoesNotExist:
        return False


class IndexView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            if "id" in request.data:
                request.data['id'] = None

            if not get_auth_email(request.data["email"]):
                raise App_Error("Email não autorizado", 400)

            user_already_exists = get_user_service(
                request.data)

            if user_already_exists["user"] is not None:
                return Response({"error": {"message": "User already exists"}}, 405)

            data = create_user_service(
                {**request.data, 'tip_of_day': get_tip_service({'order': 1})['data'].first()})
            token = get_token_by_user_service(data["user"])
            user_serializer = UserSerializer(data["user"])

            return Response({"token": token["data"].key, "user": user_serializer.data}, 201)

        except App_Error as e:
            traceback.print_exception(e)
            return Response(e.toHttp(), e.status)
        except Exception as e:
            traceback.print_exception(e)
            return Response({"error": {"message": str(e)}}, 500)

    def put(self, request):
        try:
            update_user_service({"id": request.user.id}, request.data)

            return Response(None, 200)

        except App_Error as e:
            traceback.print_exception(e)
            return Response(e.toHttp(), e.status)
        except Exception as e:
            traceback.print_exception(e)
            return Response({"error": {"message": str(e)}}, 500)

    def delete(self, request):
        try:
            request.user.delete()

            return Response(None, 200)

        except App_Error as e:
            traceback.print_exception(e)
            return Response(e.toHttp(), e.status)
        except Exception as e:
            traceback.print_exception(e)
            return Response({"error": {"message": str(e)}}, 500)
