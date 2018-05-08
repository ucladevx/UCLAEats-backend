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

        self.serializer = UserSerializer(data=self.user_attributes)
        if self.serializer.is_valid():
            user = self.serializer.save()
            self.user = User.objects.get(email=self.user_attributes['email'])

    def test_field_names(self):
        if self.serializer.is_valid():
            data = self.serializer.data
            self.assertEqual(set(data.keys()), set(['id', 'email', 'first_name', 
                'last_name', 'major', 'minor', 'year', 'self_bio', 'is_active',
                'date_created', 'date_updated', 'is_admin', 'date_updated']))
        else:
            print(self.serializer)
            print(self.user)
            raise Exception('Serializer not valid.')

    def test_email(self):
        if self.serializer.is_valid():
            data = self.serializer.data
            self.assertEqual(data['email'], self.user_attributes['email'])
        else:
            raise Exception('Serializer not valid.')

    def test_last_name(self):
        if self.serializer.is_valid():
            data = self.serializer.data
            self.assertEqual(data['last_name'], self.user_attributes['last_name'])
        else:
            raise Exception('Serializer not valid.')

    def test_first_name(self):
        if self.serializer.is_valid():
            data = self.serializer.data
            self.assertEqual(data['first_name'], self.user_attributes['first_name'])
        else:
            raise Exception('Serializer not valid.')

    def test_major(self):
        if self.serializer.is_valid():
            data = self.serializer.data
            self.assertEqual(data['major'], self.user_attributes['major'])
        else:
            raise Exception('Serializer not valid.')

    def test_minor(self):
        if self.serializer.is_valid():
            data = self.serializer.data
            self.assertEqual(data['minor'], self.user_attributes['minor'])
        else:
            raise Exception('Serializer not valid.')

    def test_year(self):
        if self.serializer.is_valid():
            data = self.serializer.data
            self.assertEqual(data['year'], self.user_attributes['year'])
        else:
            raise Exception('Serializer not valid.')

    def test_self_bio(self):
        if self.serializer.is_valid():
            data = self.serializer.data
            self.assertEqual(data['self_bio'], self.user_attributes['self_bio'])
        else:
            raise Exception('Serializer not valid.')

    def test_first_name(self):
        if self.serializer.is_valid():
            data = self.serializer.data
            self.assertEqual(data['first_name'], self.user_attributes['first_name'])
        else:
            raise Exception('Serializer not valid.')

    def test_first_name(self):
        if self.serializer.is_valid():
            data = self.serializer.data
            self.assertEqual(data['first_name'], self.user_attributes['first_name'])
        else:
            raise Exception('Serializer not valid.')

