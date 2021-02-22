import jwt
import json

from django.http        import JsonResponse
from user.models        import User
from my_settings        import SECRET_KEY, AL

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token    = request.headers['Authorization']
            payload         = jwt.decode(access_token, SECRET_KEY, algorithms=AL)
            user            = User.objects.get(id=payload['user_id'])
            request.user    = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status=400)
        except user.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=400)
        return func(self, request, *args, **kwargs)

    return wrapper
