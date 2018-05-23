from django.test import TestCase

from users.models import User
# Create your tests here.

class UserTest(TestCase):
    def setUp(self):
        User.objects.create(
            email = "test1@gmail.com",
            first_name = "Test1",
            last_name = "Me",
            major = "Testing Studies",
            minor = "No Minor",
            year = 100,
            self_bio = "I'm a test case that you should pass before deploying",
        )

        User.objects.create(
            email = "test2@gmail.com",
            first_name = "Test2",
            last_name = "Me",
        )

        User.objects.create_user(
                email = "test3@gmail.com",
                password = "test_password",
        )

    def test_id(self):
        user1 = User.objects.get(email="test1@gmail.com")
        user2 = User.objects.get(email="test2@gmail.com")
        
        self.assertIsNotNone(user1.id)
        self.assertIsNotNone(user2.id)
        # self.assertEqual(user1.id, 1)
        # self.assertEqual(user2.id, 2)

    def test_email(self):
        user1 = User.objects.get(email="test1@gmail.com")
        user2 = User.objects.get(email="test2@gmail.com")

        self.assertIsNotNone(user1.email)
        self.assertEqual(user1.email, "test1@gmail.com")
        self.assertIsNotNone(user2.email)
        self.assertEqual(user2.email, "test2@gmail.com")

    def test_password(self):
        user1 = User.objects.get(email="test1@gmail.com")
        user3 = User.objects.get(email="test3@gmail.com")

        self.assertIsNotNone(user1.password)
        self.assertIsNotNone(user3.password)
        self.assertEqual(user1.password, "")
        self.assertIsNot(user3.password, "test_password")

    def test_first_name(self):
        user1 = User.objects.get(email="test1@gmail.com")
        user2 = User.objects.get(email="test2@gmail.com")
         
        self.assertIsNotNone(user1.first_name)
        self.assertIsNotNone(user2.first_name)
        self.assertEqual(user1.first_name, "Test1")
        self.assertEqual(user2.first_name, "Test2")

    def test_last_name(self):
        user1 = User.objects.get(email="test1@gmail.com")
        user2 = User.objects.get(email="test2@gmail.com")
         
        self.assertIsNotNone(user1.last_name)
        self.assertIsNotNone(user2.last_name)
        self.assertEqual(user1.last_name, "Me")
        self.assertEqual(user2.last_name, "Me")

    def test_major(self):
        user1 = User.objects.get(email="test1@gmail.com")
        user2 = User.objects.get(email="test2@gmail.com")

        self.assertIsNotNone(user1.major)
        self.assertIsNotNone(user2.major)
        self.assertEqual(user1.major, "Testing Studies")
        self.assertEqual(user2.major, "")

    def test_minor(self):
        user1 = User.objects.get(email="test1@gmail.com")
        user2 = User.objects.get(email="test2@gmail.com")

        self.assertIsNotNone(user1.minor)
        self.assertIsNotNone(user2.minor)
        self.assertEqual(user1.minor, "No Minor")
        self.assertEqual(user2.minor, "")

    def test_year(self):
        user1 = User.objects.get(email="test1@gmail.com")
        user2 = User.objects.get(email="test2@gmail.com")

        self.assertIsNotNone(user1.year)
        self.assertIsNotNone(user2.year)
        self.assertEqual(user1.year, 100)
        self.assertEqual(user2.year, 0)

    def test_self_bio(self):
        user1 = User.objects.get(email="test1@gmail.com")
        user2 = User.objects.get(email="test2@gmail.com")

        self.assertIsNotNone(user1.self_bio)
        self.assertIsNotNone(user2.self_bio)
        self.assertEqual(user1.self_bio, "I'm a test case that you should pass" \
                " before deploying")
        self.assertEqual(user2.self_bio, "")

    # def test_print(self):
    #     user1 = User.objects.get(email="test1@gmail.com")
    #     self.assertEqual(str(user1), "test1@gmail.com")

    def test_full_name(self):
        user1 = User.objects.get(email="test1@gmail.com")
        self.assertEqual(user1.get_full_name(), "Test1 Me")
