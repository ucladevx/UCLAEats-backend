from rest_framework import serializers
from .models import WaitingUser

class WaitingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaitingUser
        fields = ('id', 'user', 'start_time', 'end_time', 'dining_hall')

    def create(self, validated_data):
        return WaitingUser.objects.create(**validated_data)

    def update(self, waiting_user, validated_data)
        waiting_user.start_time = validated_data.get("start_time",
                waiting_user.start_time)
        waiting_user.end_time = validated_data.get("end_time",
                waiting_user.end_time)
        waiting_user.dining_hall = validated.get("dining_hall",
                waiting_user.dining_hall)
        waiting_user.save()
        return waiting_user
