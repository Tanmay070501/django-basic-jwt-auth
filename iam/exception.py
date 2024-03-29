
from rest_framework.views import exception_handler
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {"message": exc.detail}
        response.status_code = exc.status_code
    return response
 