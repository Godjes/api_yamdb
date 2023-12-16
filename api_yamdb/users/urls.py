from django.urls import path

from users.views import SignUp, GetToken


urlpatterns_auth_v1 = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('token/', GetToken.as_view(), name='get_token'),
]

