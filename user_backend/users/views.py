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

"""
LOGIN
/o/token POST
HEADER - Content-Type: application/x-www-form-urlencoded
Body -  grant_type: password
        username: <email>
        password: <password>
        client_id: <client_id>
        client_secret: <client_secret>

REFRESH ACCESS TOKEN
/o/token POST
HEADER - Content-Type: application/x-www-form-urlencoded
Body -  grant_type: refresh_token
        refresh_token: <refresh_token>
        client_id: <client_id>
        client_secret: <client_secret>

LOGOUT
/o/revoke_token POST
HEADER - Content-Type: application/x-www-form-urlencoded
BODY -  token: <access_token>
        client_id: <client_id>
        client_secret: <client_secret>
"""

class UserSignup(APIView):
    """
    Allow a user to sign up and create a user account
    Does not require authentication or permissions
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format=None):
        """
        Create a user.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = self.serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserService(APIView):
    """
    Manage user requests

    Get
    Update
    Delete

    Requires default permissions
    """

    def get(self, request, format=None):
        """
        Get data of a user.
        QUERY PARAMETER: email="email@address.com"
        """
        email = request.GET.get('email')
        user = get_user(email)
        serializer = UserSerializer(user)
        return Response(serializer.data)

        # Gets all user data
        # users = User.objects.all()
        # serializer = UserSerializer(users, many=True)
        # return Response(serializer.data)

    def put(self, request, format=None):
        """
        Update information about a user.
        """
        email = get_email(request)
        user = get_user(email)
        serializer = UserSerializer(user, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """
        Delete a user
        """
        email = get_email(request)
        user = get_user(email)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


### Non Router Functions ###
def get_user(email):
    """
    Returns user based on public key
    """
    try:
        return User.objects.get(email=email)
    except:
        raise Http404

def get_email(request):
    """
    Returns email of a user from the request, or raises Http404
    """
    try:
        return request.data["email"]
    except:
        raise Http404

def get_pk(request):
    """
    Returns public key from request
    """
    try:
        return request.data["id"]
    except:
        raise Http404

