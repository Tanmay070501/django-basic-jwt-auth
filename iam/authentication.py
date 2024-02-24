from rest_framework.authentication import BaseAuthentication
from .models import User
from api.utils import generate_error_response
from jwt import ExpiredSignatureError, InvalidTokenError
from rest_framework import status
from .utils import verify_token
from rest_framework.exceptions import APIException
#from .exception import CustomAuthFailed
#from iam.exception import CustomAuthFailed
class CustomAuthentication(BaseAuthentication):
    '''
        custom authentication class for DRF and JWT
        https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py
    '''

    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return None
        try:
            # header = 'Bearer xxxxxxxxxxxxxxxxxxxxxxxx'
            header = authorization_header.split(' ')[0]
            if header != 'Bearer':
                raise CustomAuthFailed("Invalid Token prefix",status.HTTP_400_BAD_REQUEST)
            access_token = authorization_header.split(' ')[1]
            payload = verify_token(access_token)
            user = User.objects.filter(user_id=payload['user_id']).first()
            if user is None:
                raise CustomAuthFailed("User not found",status.HTTP_404_NOT_FOUND)
            return (user, None)
        except IndexError:
            raise CustomAuthFailed("Token missing",status.HTTP_400_BAD_REQUEST)
        except ExpiredSignatureError:
            raise CustomAuthFailed("Token has expired",status.HTTP_406_NOT_ACCEPTABLE)
        except InvalidTokenError:
            raise CustomAuthFailed('Invalid token',status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise CustomAuthFailed(f"{e}")

class CustomAuthFailed(APIException):
    """
    raises API exceptions with custom messages and custom status codes
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'error'
    def __init__(self, detail, status_code=None):
        self.detail = {"message":detail}
        if status_code is not None:
            self.status_code = status_code