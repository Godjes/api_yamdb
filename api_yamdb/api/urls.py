from django.urls import include, path
from rest_framework import routers
from api.views import TitleViewSet, GenreViewSet, CategoryViewSet, CommentViewSet, ReviewViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'categories', CategoryViewSet, basename='category')
router_v1.register(r'genres', GenreViewSet, basename='genre')
router_v1.register(r'titles', TitleViewSet, basename='title')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comments'
)
urlpatterns = [
    path('v1/', include(router_v1.urls))

