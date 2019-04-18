from rest_framework import serializers

from .models import WaitingUser, MatchedUsers

class WaitingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaitingUser
        fields = ('id', 'user', 'meal_times', 'meal_day', 'meal_period', 
                'dining_halls', 'status','date_updated')

    def create(self, validated_data):
        def convert(t):
            return t.strftime('%Y-%m-%d %H:%M:%S' )
        validated_data['meal_times'] = list(map(convert, validated_data['meal_times']))
        return WaitingUser.objects.create(**validated_data)

    def update(self, waiting_user, **validated_data):
        waiting_user.dining_hall = validated.get("dining_hall",
                waiting_user.dining_hall)

   
        waiting_user.times = validated_data.get("times", waiting_user.times)
        waiting_user.meal_period = validated_data.get("meal_period",
                waiting_user.meal_period)
        waiting_user.save()
        return waiting_user

class MatchedUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchedUsers
        fields = ('id', 'user1', 'user1_first_name', 'user1_last_name',
            'user2_first_name', 'user2_last_name', 'user2', 'meal_datetime', 
            'meal_period', 'dining_hall', 'chat_url')

    def create(self, validated_data):
        def convert(t):
            return t.strftime('%Y-%m-%d %H:%M:%S' )
        validated_data['meal_datetime'] = validated_data['meal_datetime'].strftime('%Y-%m-%d %H:%M:%S' )
        return MatchedUsers.objects.create(**validated_data)

    def update(self, matched_users, **validated_data):
        pass
