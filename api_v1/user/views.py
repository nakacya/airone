from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User as DjangoUser

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView

from api_v1.auth import AironeTokenAuth
from user.models import User as AironeUser


class AccessTokenAPI(APIView):
    authentication_classes = (AironeTokenAuth, BasicAuthentication, SessionAuthentication,)

    def get(self, request, format=None):
        user = DjangoUser.objects.get(id=request.user.id)

        return Response({'results': str(AironeUser(id=user.id).token)})

    @method_decorator(csrf_protect)
    def put(self, request, format=None):
        """
        This refresh access_token to another one
        """

        user = DjangoUser.objects.get(id=request.user.id)
        token, created = Token.objects.get_or_create(user=user)

        # If the token is not created, this returns it.
        if created:
            return Response({'results': str(token)})

        # This recreates another Token when it has been already existed.
        token.delete()
        return Response({'results': str(Token.objects.create(user=user))})
