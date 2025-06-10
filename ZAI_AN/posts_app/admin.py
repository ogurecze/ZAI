from django.contrib import admin

from .models import Post, Profile, Dish, Comment, DishType, CookingSpot
from .models import User

# Register your models here.
admin.site.register(Post)
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Dish)
admin.site.register(Comment)
admin.site.register(DishType)
admin.site.register(CookingSpot)