from rest_framework.response import Response


def basic_response(status, message, data):
    return Response({"status": status, "message": message, "data": data})
