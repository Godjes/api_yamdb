from random import randint
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from users.models import User
from django.core.mail import send_mail

from users.serializers import AuthSerializer, TokenSerializer


class SignUp(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        auth_serializer = AuthSerializer(data=request.data)
        if auth_serializer.is_valid():
            auth_serializer.save()
            user = auth_serializer.save() # не уверена, что сохранение в бд является объектом
            #user = User.objects.get(**auth_serializer.validated_data)
            user.confirmation_code = randint(10000, 99999)
            auth_serializer.save()
            email = auth_serializer.validated_data.get('email')

            send_mail(
                subject='Your confirmation code',     
                message= f'{user.confirmation_code} - confirmation code',
                from_email='from@yamdb.com',
                recipient_list=[f'{email}'],
                fail_silently=False,
                ) 

            return Response(auth_serializer.data)

        return Response({'field_name': auth_serializer.errors})


class GetToken(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token_serializer = TokenSerializer(data=request.data)
        if token_serializer.is_valid():
            # RefreshToken
            # проставляем user.is_email_confirmed = True
            return Response() # token

        return Response({'message': token_serializer.errors})


class UsersViewSet():
    ...


class UsernameViewSet():
    ...


class MeViewSet():
    ...
