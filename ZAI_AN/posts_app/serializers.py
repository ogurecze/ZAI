from rest_framework import serializers
from .models import Post, Comment, DishType, CookingSpot, Dish, Profile
from .schema import User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author',)        
    
   

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

class DishTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishType
        fields = '__all__'

class CookingSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookingSpot
        fields = '__all__'
class DishSerializer(serializers.ModelSerializer):
    spot_details = CookingSpotSerializer(source='spot', read_only=True)
    class Meta:
        model = Dish
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
        read_only_fields = ['id']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Hasła muszą być takie same")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        Profile.objects.create(id=user.id, user=user)
        return user
    
class DishTypeAggregationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    avg_weight = serializers.FloatField()    