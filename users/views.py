import json, bcrypt, jwt
import os

from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ValidationError

from .models import User
from my_settings import SECRET_KEY, ALGORITHM

class SigninView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(name=data['name'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message': 'INVALID_USER'}, status=401)

            token = jwt.encode({'user': user.name}, SECRET_KEY, algorithm=ALGORITHM)

            return JsonResponse({
                'message': 'SUCCESS',
                'access_token': token
            }, status=200)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)

        except ValidationError as e:
            return JsonResponse({'message': e.message}, status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
