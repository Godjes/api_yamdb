from django.urls import path

from users.views import SignUp


urlpatterns_auth_v1 = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('token/', SignUp.as_view(), name='signup'),
]

# возможно тут должны быть роутеры, не знаю
urlpatterns_users_v1 = [
    path('me/', SignUp.as_view(), name='signup'),
    path('<username>/', SignUp.as_view(), name='signup'),
    path('', SignUp.as_view(), name='signup'),
]
