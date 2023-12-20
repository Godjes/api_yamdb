from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import EMAIL_ADDRESS
from users.models import User
from users.permissions import IsAdmin
from users.serializers import (AuthSerializer, MeSerializer, TokenSerializer,
                               UsersSerializer)


class SignUp(APIView):
    """Класс, отвечающий за регистрацию пользователей."""
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        try:
            user = User.objects.get(username=request.data.get('username'),
                                    email=request.data.get('email'))
        except User.DoesNotExist:
            user = None

        auth_serializer = AuthSerializer(data=request.data, instance=user)

        if auth_serializer.is_valid(raise_exception=True):
            user = auth_serializer.save()
            # user.confirmation_code = randint(10000, 99999)
            confirmation_code = default_token_generator.make_token(user)
            auth_serializer.save()
            email = auth_serializer.validated_data.get('email')

            send_mail(
                subject='Your confirmation code',
                message=f'{confirmation_code} - confirmation code',
                from_email=EMAIL_ADDRESS,
                recipient_list=[f'{email}'],
                fail_silently=False,
            )

            return Response(auth_serializer.data)

        return Response({'field_name': auth_serializer.errors})


class GetToken(APIView):
    """Класс, отвечающий за получение токена аутентификации."""
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

            try:
                if default_token_generator.check_token(
                    user,
                    request.data.get('confirmation_code')
                ):
                    token = RefreshToken.for_user(user)
                    return Response(
                        {'token': str(token.access_token)}
                    )
            except AttributeError:
                return Response(
                    {'error': 'Invalid confirmation code structure'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except ValueError:
                return Response(
                    {'error': 'Invalid confirmation code'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            token_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UsersViewSet(viewsets.ModelViewSet):
    """Класс, отвечающий за работу с пользователями."""
    serializer_class = UsersSerializer
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = ('username')
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']


class MeViewSet(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                GenericViewSet):
    """Класс, отвечающий за работу с текущим пользователем."""
    serializer_class = MeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.request.user.id)
