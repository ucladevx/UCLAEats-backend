from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Helps with the transformation of user data to/from JSON and other data
    formats
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'major', 
                'minor', 'year', 'self_bio', 'date_created', 'date_updated', 
                'is_active', 'is_admin')

    def create(self, validated_data):
        """
        Create and return a new instance of the User, given validated data
        """
        return User.objects.create_user(**validated_data)

    def update(self, user, validated_data):
        """
        Allow a user to update their 
        first name, last name, major, minor, and year
        """
        user.first_name = validated_data.get("first_name", user.first_name)
        user.last_name = validated_data.get("last_name", user.last_name)
        user.major = validated_data.get("major", user.major)
        user.minor = validated_data.get("minor", user.minor)
        user.year = validated_data.get("year", user.year)
        user.self_bio = validated_data.get("self_bio", user.self_bio)
        user.save()
        return user
