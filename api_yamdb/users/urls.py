from django.urls import path

from users.views import SignUp, UsersViewSet


urlpatterns_auth_v1 = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('v1/auth/token/', SignUp.as_view(), name='signup'),
]

