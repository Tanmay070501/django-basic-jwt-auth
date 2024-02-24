
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from basic_auth_app.settings import EMAIL_HOST_USER
import jwt
from basic_auth_app.settings import SIMPLE_JWT, BACKEND_BASE_URL
from .serializers import CustomTokenObtainPairSerializer, UserMinDataSerializer
def create_token(user):
    refresh = CustomTokenObtainPairSerializer.get_token(user)
    return str(refresh.access_token)

def generate_verification_token(payload: dict) -> str:
    token = jwt.encode(payload=payload,  key=SIMPLE_JWT.get("SIGNING_KEY"), algorithm='HS256')
    return token

def verify_verification_token(token: str):
    payload = jwt.decode(jwt=token, key=SIMPLE_JWT.get("SIGNING_KEY"), algorithms='HS256')
    return payload

def send_verification_email(user):
    token = generate_verification_token(UserMinDataSerializer(user).data)
    
    mail_subject = 'Activate your account'
    email_body = f"Hi {user.email} Use like this to activate your account. {BACKEND_BASE_URL}/auth/verify/?token={token}"
    send_mail(mail_subject,email_body, EMAIL_HOST_USER, [user.email])

def verify_token(token: str) -> dict:
    payload = jwt.decode(token, SIMPLE_JWT.get("SIGNING_KEY"), SIMPLE_JWT.get("ALGORITHM"))
    return payload
