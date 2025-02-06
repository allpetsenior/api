from rest_framework.authtoken.models import Token


class TokenRepository():
    def get_token_by_user(self, user):
        return Token.objects.get(user=user)
