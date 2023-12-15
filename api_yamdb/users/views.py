from random import randint
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, viewsets
import jwt
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from django.shortcuts import get_object_or_404
from users.models import User
from django.core.mail import send_mail

from users.serializers import AuthSerializer, TokenSerializer, UsersSerializer
from users.permissions import IsAdmin


class SignUp(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        auth_serializer = AuthSerializer(data=request.data)
        if auth_serializer.is_valid():
            auth_serializer.save()
            user = auth_serializer.save() # не уверена, что сохранение в бд является объектом
            #user, status = User.objects.get_or_create(**auth_serializer.validated_data)
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
        if token_serializer.is_valid(raise_exception=True):
            try:
                user = get_object_or_404(
                    User,
                    username=token_serializer.validated_data['username']
                )
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if token_serializer.validated_data['confirmation_code'] == user.confirmation_code:
                token = jwt.encode(AuthSerializer, token_serializer['confirmation_code'], algorithm='HS256')
                return Response(
                    {'token': token},
                    status=status.HTTP_201_CREATED
                )
            return Response(
                token_serializer.errors,
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            token_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )






class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    lookup_field = "username"

    def perform_create(self, serializer):
        serializer.save(is_email_confirmed=True)


class MeViewSet(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                GenericViewSet):
    serializer_class = UsersSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.request.user.id)
