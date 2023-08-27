
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from linkup_backend.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
import jwt
from linkup_backend.settings import SIMPLE_JWT
from .serializers import CustomTokenObtainPairSerializer
def create_token(user):
    refresh = CustomTokenObtainPairSerializer.get_token(user)
    return str(refresh.access_token)

def send_verification_email(user):
    token = create_token(user)
    mail_subject = 'Activate your account'
    email_body = f"Hi {user.email} Use like this to activate your account. http:localhost:8000/auth/verify/?token={token}"
    send_mail(mail_subject,email_body, EMAIL_HOST_USER,[user.email])

def verify_token(token):
    payload = jwt.decode(token, SIMPLE_JWT.get("SIGNING_KEY"), SIMPLE_JWT.get("ALGORITHM"))
    return payload
