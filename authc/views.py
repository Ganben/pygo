from django.shortcuts import render
#

from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import permissions, viewsets, status
from .models import Account
from .permissions import IsAccountOwner
from .serializers import AccountSerializer

from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


# Create your views here.
#TODO : rewrite to urls defined

class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsAccountOwner(),)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)

            return HttpResponse(serializer.validated_data, status=201)

        return HttpResponse({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=400)


@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
def authc(request):
    seri = AccountSerializer
    queryset =  Account.objects.all()
    lookup_field = 'username'
    if request.methode == 'GET':
        return Response()

    elif request.methode == 'POST':
        return Response({'received data': request.data})

