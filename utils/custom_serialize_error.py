from rest_framework.views import exception_handler

def custom_serialize_error(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(response.data, dict):
            missing_fields = [key for key in response.data.keys()]
            response.data = {
                "message": f"{' and '.join(missing_fields)} are missing"
            }

    return response
