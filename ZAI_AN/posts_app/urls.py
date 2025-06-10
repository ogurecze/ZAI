from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter, APIRootView
from .views import *

router = DefaultRouter()
router.register(r'posts_app', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'species', DishTypeViewSet, basename='species')
router.register(r'spots', CookingSpotViewSet, basename='spot')
router.register(r'Dishes', DishViewSet, basename='Dish')
router.register(r'profiles', ProfileViewSet, basename='profile')


urlpatterns = [
    path('', include(router.urls)),
    path('', APIRootView.as_view(), name='api'),
]