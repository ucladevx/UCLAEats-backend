from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.http import Http404
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User
from users.serializers import UserSerializer

# Create your views here.

class UserService(APIView):
    """
    Manage user requests
    Get
    Create
    Update
    Delete

    Login
    Logout
    """
    authentication_classes = ()
    permission_classes = ()


    def get(self, request, format=None):
        """
        Get data of all users.  THIS SHOULD BE DEPRECATED
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create a user.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        """
        Update information about a user.
        """
        email = self.get_email(request)
        user = self.get_user(email)
        serializer = UserSerializer(user, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """
        Delete a user
        """
        email = self.get_email(request)
        user = self.get_user(email)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Non Router Functions
    def get_user(self, email):
        """
        Returns user based on public key
        """
        try:
            return User.objects.get(email=email)
        except:
            raise Http404

    def get_email(self, request):
        """
        Returns email of a user from the request, or raises Http404
        """
        try:
            return request.data["email"]
        except:
            raise Http404

    def get_pk(self, request):
        """
        Returns public key from request
        """
        try:
            return request.data["id"]
        except:
            raise Http404


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    When a user is saved to the database, this function is run, and will
    associate a authtoken to that user
    """

    if created:
        Token.objects.create(user=instance)
