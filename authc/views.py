from django.shortcuts import render


from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import permissions, viewsets
from .models import Account
from .permissions import IsAccountOwner
from .serializers import AccountSerializer

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