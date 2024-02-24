from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from rest_framework import status
from api.utils import generate_error_response, generate_successful_response
from .utils import create_token, send_verification_email, verify_verification_token
#from .serializers import UserSerializer
from jwt import ExpiredSignatureError, InvalidTokenError
# Create your views here.


class Login(APIView):
    def post(self, request):
        try:

            email = request.data.get('email')
            password = request.data.get('password')
            try:
                user = User.objects.get(email = email)
            except User.DoesNotExist:
                return generate_error_response('User not found', status=status.HTTP_404_NOT_FOUND)
            if user.check_password(password):
                if user.email_verified:
                    token = create_token(user)
                    return generate_successful_response(token)
                # email not verified
                send_verification_email(user)
                return generate_error_response('Please verify your email. Check your email for verification.', status=status.HTTP_401_UNAUTHORIZED)
            # wrong creds
            return generate_error_response('Invalid credentials', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return generate_error_response(str(e))
                
        
class Signup(APIView):
    """
    body: 
    
    {
        "email": "abc@yopmail.com",
        "pasword": "verysecretpass"
    }

    success returns:

    {
        message: "Verification email sent"
    }

    """
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            try:
                user = User.objects.get(email = email)
                return generate_error_response('User already exists', status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                user = User.objects.create_user(email=email, password=password)
                user.save()
                send_verification_email(user)
                return generate_successful_response('Verification email sent')
        except Exception as e:
            return generate_error_response(str(e))

class EmailVerification(APIView):
    def get(self, request):
        try:
            token = request.GET.get('token',None)
            if token is None:
                return generate_error_response('Invalid token', status=status.HTTP_400_BAD_REQUEST)
            try:
                payload = verify_verification_token(token)
                user = User.objects.get(user_id=payload['user_id'])
                if user.email_verified == True :  
                    return generate_error_response('User Already Verified', status=status.HTTP_400_BAD_REQUEST) 
                user.email_verified = True
                user.save()
                return generate_successful_response('Verification Done!', status=status.HTTP_200_OK)
            except ExpiredSignatureError:
                return generate_error_response('Token Expired', status=status.HTTP_400_BAD_REQUEST)
            except InvalidTokenError:
                return generate_error_response('Invalid Token', status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return generate_error_response(f"{e}", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return generate_error_response(str(e))