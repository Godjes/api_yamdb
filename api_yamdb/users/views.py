from random import randint
import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from django.shortcuts import get_object_or_404
from users.models import User

from users.serializers import AuthSerializer, TokenSerializer


class SignUp(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        auth_serializer = AuthSerializer(data=request.data)
        if auth_serializer.is_valid():
            user = auth_serializer.save()
            user.confirmation_code = randint(10000, 99999)
            auth_serializer.save()

            # ОТПРАВЛЯЕМ ПИСЬМО НА ПОЧТУ

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






class UsersViewSet():
    ...


class UsernameViewSet():
    ...


class MeViewSet():
    ...
