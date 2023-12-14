from django.urls import include, path
from rest_framework import routers

from api.views import TitleViewSet, GenreViewSet, CategoryViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'categories', CategoryViewSet, basename='category')
router_v1.register(r'genres', GenreViewSet, basename='genre')
router_v1.register(r'titles', TitleViewSet, basename='title')

urlpatterns = [
    path('v1/', include(router_v1.urls))
]
