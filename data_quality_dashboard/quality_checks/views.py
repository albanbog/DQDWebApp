from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse

@api_view(['GET'])
def basic_check(request):
    data = {
        "message": "This is a simple test API"
    }
    return Response(data)


def index(request):
    return HttpResponse("Welcome to the Data Quality Dashboard!")
