from random import randint
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import permissions, status
from django.core.mail import send_mail

from users.models import User
from users.serializers import AuthSerializer, TokenSerializer, UsersSerializer
from users.permissions import IsAdmin


class SignUp(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        auth_serializer = AuthSerializer(data=request.data)
        if auth_serializer.is_valid(raise_exception=True):
            auth_serializer.save()
            user = auth_serializer.save()
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
                token = RefreshToken.for_user(user)
                return Response(
                    {'token': str(token.access_token)}
                )
            return Response(
                {'error': 'Invalid confirmation code'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            token_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class PatchAPIView(APIView):

    def update(self, request):

        user = get_object_or_404(User, username=self.request.user.username)
        if request.method == 'PATCH':
            serializer = UsersSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    lookup_field = "username"


class MeViewSet(mixins.RetrieveModelMixin,
                PatchAPIView,
                GenericViewSet):
    serializer_class = UsersSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.request.user.id)
