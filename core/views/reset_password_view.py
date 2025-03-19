import traceback
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from core.services.reset_password_service import reset_user_password_service
from v0.errors.app_error import App_Error


def validate(data):
    if "email" not in data:
        raise App_Error("Email é obrigatório", 400)
    if "password" not in data:
        raise App_Error("Senha é obrigatório", 400)


@api_view(["PUT"])
@permission_classes([])
def reset_password_view(request):
    try:
        validate(request.data)

        email = request.data.get("email")
        password = request.data.get("password")

        print(f"LOG RESET_PASSWORD EMAIL {email}")

        reset_user_password_service({"email": email}, {"password": password})

        return Response({"ok": True}, 200)

    except App_Error as e:
        traceback.print_exception(e)
        return Response(e.toHttp(), e.status)
    except Exception as e:
        traceback.print_exception(e)
        return Response({"error": {"message": str(e)}}, 500)
