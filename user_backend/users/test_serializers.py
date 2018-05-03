from django.test import TestCase

from users.models import User
from users.serializers import UserSerializer

class TestUserSerializers(TestCase):
    def setUp(self):
        self.user_attributes = {
            "email" : "test@gmail.com",
            "password" : "testpassword",
            "first_name" : "Test",
            "last_name" : "Me",
            "major" : "Testing Studies",
            "minor" : "Unit Testing",
            "year" : 2,
            "self_bio" : "I'm a unit test that should pass",
        }
        self.user = User.objects.create_user(**self.user_attributes)

        self.serializer_data = {
            "email" : "test_serializer@gmail.com",
            "password" : "test_serializer",
            "first_name" : "Test",
            "last_name" : "Serializer",
            "major" : "Testing Serializer",
            "minor" : "Unit Testing",
            "year" : 2,
            "self_bio" : "I'm testing the serializer",
        }

        self.serializer = UserSerializer(data=self.serializer_data)

    def test_fields(self):
        if self.serializer.is_valid():
            data = self.serializer.data
            print(data.keys())
            self.assertEqual(set(data.keys()), set(['id', 'email', 'password',
                'first_name', 'last_name', 'major', 'minor', 'year', 'self_bio',
                'date_created', 'date_updated', 'is_active', 'is_admin']))
        else:
            raise Exception('Serializer not valid.')



