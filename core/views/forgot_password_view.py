import traceback
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from v0.errors.app_error import App_Error
from app.settings import EMAIL_HOST_USER, LINK_FORGOT_PASSWORD
from core.services.get_user_service import get_user_service


@api_view(["GET"])
@permission_classes([])
def forgot_password_view(request):
    try:
        email = request.query_params.get("email")

        finded_user = get_user_service({"email": email})

        if not finded_user["user"]:
            raise App_Error("Email não encontrado", 404)

        html_content = render_to_string(
            "emails/forgot_password.html",
            {'link_forgot_password': LINK_FORGOT_PASSWORD + "/" + email
             }
        )

        text_content = render_to_string(
            "emails/forgot_password.txt",
            {'link_forgot_password': LINK_FORGOT_PASSWORD + "/" + email
             }

        )

        send_mail(
            "Redefina sua senha na AllPetSenior",
            text_content,
            EMAIL_HOST_USER,
            [email],
            html_message=html_content,
        )

        return Response({"ok": True}, 200)

    except App_Error as e:
        traceback.print_exception(e)
        return Response(e.toHttp(), e.status)
    except Exception as e:
        traceback.print_exception(e)
        return Response({"error": {"message": str(e)}}, 500)
