from rest_framework.response import Response
from rest_framework.request import Request


def api_response(success: bool = False, status_code: int = 0, message: str = '', data: dict = {}) -> Response:
    response = {'success': success}
    if status_code:
        response.update({'status_code': status_code})
    if message:
        response.update({'message': message})
    if data:
        response.update({'data': data})
    return Response(response)
