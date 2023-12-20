from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet)
from users.views import GetToken, MeViewSet, SignUp, UsersViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'categories', CategoryViewSet, basename='category')
router_v1.register(r'genres', GenreViewSet, basename='genre')
router_v1.register(r'titles', TitleViewSet, basename='title')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router_v1.register(
    r'users', UsersViewSet, basename='users'
)

urlpatterns_auth = [
    path('auth/signup/', SignUp.as_view(), name='signup'),
    path('auth/token/', GetToken.as_view(), name='get_token'),
]
urlpatterns_v1 = [
    path(
        'users/me/',
        MeViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}),
        name='users_me'
    ),
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(urlpatterns_v1)),
    path('v1/', include(urlpatterns_auth)),
]
