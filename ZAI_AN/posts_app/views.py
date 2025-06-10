from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .models import Post, Comment, DishType, CookingSpot, Dish, Profile, User
from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly, IsProfileAuthorOrReadOnly
from .serializers import (
    PostSerializer, CommentSerializer, DishTypeSerializer,
    CookingSpotSerializer, DishSerializer, ProfileSerializer, UserRegisterSerializer
)
from django.http import JsonResponse


class APIRootView(APIView):
    """
    Widok główny API Root
    """


    def get(self, request, format=None):
        return JsonResponse({
            'posts': reverse('post-list', request=request, format=format),
            'comments': reverse('comment-list', request=request, format=format),
            'species': reverse('species-list', request=request, format=format),
            'spots': reverse('spot-list', request=request, format=format),
            'Dishes': reverse('Dish-list', request=request, format=format),
            'profiles': reverse('profile-list', request=request, format=format),
        })


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = []
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class DishTypeViewSet(viewsets.ModelViewSet):
    queryset = DishType.objects.all()
    serializer_class = DishTypeSerializer
    permission_classes = [IsAdminOrReadOnly]


class CookingSpotViewSet(viewsets.ModelViewSet):
    queryset = CookingSpot.objects.all()
    serializer_class = CookingSpotSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
