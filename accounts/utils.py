from rest_framework.authtoken.models import Token

def get_user_tokens(user):
    token,_=Token.objects.get_or_create(user=user)
    return {
        'token':str(token.key)
    }