import string
import random

from django.test import TestCase

# Create your tests here.
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from posts_app.models import User, DishType, CookingSpot, Dish, Post, Comment


@pytest.mark.django_db
def test_create_user():
    random_name = ''.join(random.choices(string.ascii_lowercase, k=8))
    User.objects.create_user(username=random_name, email="test@example.com", password="testpass")
    assert User.objects.filter(username=random_name).exists()

@pytest.mark.django_db
def test_create_dish_type():
    random_type = ''.join(random.choices(string.ascii_lowercase, k=8))
    dtype = DishType.objects.create(name=random_type, description="Ryba słodkowodna", season="Lato")
    assert DishType.objects.filter(name=random_type).exists()

@pytest.mark.django_db
def test_api_get_posts():
    client = APIClient()
    url = reverse("post-list")
    response = client.get(url)
    print(url)
    print(response)
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_cooking_spot():
    random_lake = ''.join(random.choices(string.ascii_lowercase, k=8))
    spot = CookingSpot.objects.create(name=random_lake, location="Dom", description="Najlepsze miejsce do gotowania")
    assert CookingSpot.objects.filter(name="Mieszkanie").exists()

@pytest.mark.django_db
def test_create_and_get_comment():
    random_comment = ''.join(random.choices(string.ascii_lowercase, k=8))
    user = User.objects.create_user(username=random_comment, password="testpass")
    post = Post.objects.create(author=user, title="Test", content="Test content")
    comment = Comment.objects.create(post=post, author=user, text="Pyszne!")
    assert Comment.objects.filter(text="Pyszne!").exists()


@pytest.mark.django_db
def test_create_post():
    # Przygotowanie danych
    random_user = ''.join(random.choices(string.ascii_lowercase, k=8))
    user = User.objects.create_user(username=random_user, password='testpass')
    post = Post.objects.create(author=user, title='Stary tytuł', content='Stara treść')

    # Przygotowanie klienta
    client = APIClient()
    client.force_authenticate(user=user)

    url = f'/api/posts_app/{post.id}/'  # endpoint do konkretnego posta
    update_data = {
        'title': 'Nowy tytuł',
        'content': 'Nowa treść'
    }
    response = client.put(url, update_data, format='json')

    # Sprawdzenie rezultatu
    assert response.status_code == 200
    assert response.data['title'] == 'Nowy tytuł'
    assert response.data['content'] == 'Nowa treść'


@pytest.mark.django_db
def test_create_new_post():
    # Przygotowanie danych
    random_user = ''.join(random.choices(string.ascii_lowercase, k=8))
    user = User.objects.create_user(username=random_user, password='testpass')

    # Przygotowanie klienta
    client = APIClient()
    client.force_authenticate(user=user)

    # Dane nowego posta
    post_data = {
        'title': 'Nowy post',
        'content': 'Treść nowego posta'
    }

    # Wysłanie żądania
    url = '/api/posts_app/'
    response = client.post(url, post_data, format='json')

    # Sprawdzenie rezultatu
    assert response.status_code == 201
    assert response.data['title'] == 'Nowy post'
    assert response.data['content'] == 'Treść nowego posta'
    assert response.data['author'] == user.id
    assert Post.objects.filter(title='Nowy post').exists()