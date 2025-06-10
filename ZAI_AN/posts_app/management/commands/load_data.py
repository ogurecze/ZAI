from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from posts_app.models import Profile, CookingSpot, DishType, Post, Dish, Comment
from datetime import date

class Command(BaseCommand):
    help = 'Loads initial data into the database'

    def handle(self, *args, **options):
        User = get_user_model()

        # Create users
        user1 = User.objects.create_user(username='john_doe', password='password123', email='john@example.com')
        user2 = User.objects.create_user(username='jane_smith', password='password456', email='jane@example.com')

        # Create profiles
        Profile.objects.create(user=user1, bio='John\'s bio', avatar='')
        Profile.objects.create(user=user2, bio='Jane\'s bio', avatar='')

        # Create cooking spots
        spot1 = CookingSpot.objects.create(author=user1, name='Home Kitchen', location='City A', description='My home cooking spot')
        spot2 = CookingSpot.objects.create(author=user2, name='Outdoor Grill', location='Park B', description='Grilling in the park')

        # Create dish types
        dtype1 = DishType.objects.create(name='Soup', description='Warm and comforting', difficulty='Easy')
        dtype2 = DishType.objects.create(name='Salad', description='Fresh and healthy', difficulty='Medium')

        # Create posts
        post1 = Post.objects.create(author=user1, title='My First Recipe', content='This is my first recipe post.', image='')
        post2 = Post.objects.create(author=user2, title='Grilling Tips', content='Tips for perfect grilling.', image='')

        # Create dishes
        dish1 = Dish.objects.create(author=user1, dtype=dtype1, cooking_method='Gotowane', spot=spot1, weight=0.5, date=date(2024, 1, 15), photo='')
        dish2 = Dish.objects.create(author=user2, dtype=dtype2, cooking_method='Surowe', spot=spot2, weight=0.3, date=date(2024, 1, 20), photo='')

        # Create comments
        Comment.objects.create(post=post1, author=user2, text='Great recipe!')
        Comment.objects.create(post=post2, author=user1, text='Thanks for the tips!')

        # Associate dishes with posts
        post1.Dishes.add(dish1)
        post2.Dishes.add(dish2)

        self.stdout.write(self.style.SUCCESS('Data loaded successfully!'))