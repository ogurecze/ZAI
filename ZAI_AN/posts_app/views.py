from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post, Comment, DishType, CookingSpot, Dish, Profile, User
from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly, IsProfileAuthorOrReadOnly
from .serializers import (
    PostSerializer, CommentSerializer, DishTypeSerializer,
    CookingSpotSerializer, DishSerializer, ProfileSerializer, UserRegisterSerializer, DishTypeAggregationSerializer
)
from django.http import JsonResponse
from django.db.models import Avg, Count


class APIRootView(APIView):
    """
    Widok główny API Root
    """


    def get(self, request, format=None):
        return JsonResponse({
            'posts': reverse('post-list', request=request, format=format),
            'comments': reverse('comment-list', request=request, format=format),
            'dish-type': reverse('dish-type', request=request, format=format),
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


class DishTypeAggregationView(generics.ListAPIView):
    serializer_class = DishTypeAggregationSerializer

    def get_queryset(self):
        return DishType.objects.annotate(avg_weight=Avg('dish__weight')).values('id', 'name', 'avg_weight')

class CookingSpotStatsView(APIView):
    """
    View showing statistics for cooking spots:
    - Number of dishes prepared
    - Average weight of dishes
    - Most common cooking method
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        spots_stats = CookingSpot.objects.annotate(
            dishes_count=Count('dish'),
            avg_dish_weight=Avg('dish__weight'),
            total_authors=Count('dish__author', distinct=True)
        ).values(
            'id',
            'name',
            'location',
            'dishes_count',
            'avg_dish_weight',
            'total_authors'
        )

        return Response(spots_stats)    