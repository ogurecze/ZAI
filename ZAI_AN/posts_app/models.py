from django.db import models
from django.contrib.auth.models import AbstractUser

# Choices
COOKING_METHOD = [
    ('Prodziż', 'Pieczone'),
    ('Smarzone', 'Gotowane'),
    ('Parzone', 'Surowe'),
]

# Użytkownik
class User(AbstractUser):
    class Meta:
        verbose_name = 'Użytkownik'
        verbose_name_plural = 'Użytkownicy'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profile'


    def __str__(self):
        return f"{self.user.username}  "



# Miejsce
class CookingSpot(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name = 'Miejsce'
        verbose_name_plural = 'Miejsca'

    def __str__(self):
        return f"{self.name} ({self.location})"


# Rodzaj dania
class DishType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Rodzaj dania'
        verbose_name_plural = 'Rodzaje dań'

    def __str__(self):
        return f"{self.name}"

# Post na blogu
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts_app')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='posts_app/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    Dishes = models.ManyToManyField(
        'Dish',  # Relacja post -> Dish, jeden post może mieć wiele potraw
        related_name='post_Dishes',  # Zmieniamy related_name na 'post_Dishes'
        blank=True  # Nie jest wymagane posiadanie połowów
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Wpis na blogu'
        verbose_name_plural = 'Wpisy na blogu'

    def __str__(self):
        return f"{self.title} ({self.author})"


# Danie
class Dish(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    dtype = models.ForeignKey(DishType, on_delete=models.CASCADE, null=False)
    cooking_method = models.CharField(max_length=30, choices=COOKING_METHOD, null=False, default='')
    spot = models.ForeignKey(CookingSpot, on_delete=models.SET_NULL, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    photo = models.ImageField(upload_to='Dishes/', blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Danie'
        verbose_name_plural = 'Dania'

    def __str__(self):
        return f"{self.species.name} {self.weight}kg ({', '.join([post.title for post in self.posts.all()])})"


# Komentarz
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Komentarz'
        verbose_name_plural = 'Komentarze'
    def __str__(self):
        return f"{self.post.title} {self.author} ({self.text}))"
