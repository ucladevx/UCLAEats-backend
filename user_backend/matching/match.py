from matching.models import WaitingUser
from matching.serializers import WaitingUserSerializer, MatchedUsersSerializer

def attempt_match(waiting_user):
    users = WaitingUser.objects.filter(found_match=False) \
            .filter(meal_day=waiting_user.meal_day) \
            .filter(meal_period=waiting_user.meal_period)

    for user in users:
        if user.user_id != waiting_user.user_id:
            common_dining_halls = list(set(user.dining_halls)
                    .intersection(set(waiting_user.dining_halls)))
            if len(common_dining_halls) == 0:
                continue
            common_times = list(set(user.meal_times)
                    .intersection(set(waiting_user.meal_times)))
            if len(common_times) == 0:
                continue
            

            # Terribly choose the first time and dining hall
            
            matched_users_data = {
                "user1" : waiting_user.user_id,
                "user2" : user.user_id,
                "meal_datetime" : common_times[0],
                "meal_period" : waiting_user.meal_period,
                "dining_hall" : common_dining_halls[0],
            }

            serializer = MatchedUsersSerializer(data=matched_users_data)
            if serializer.is_valid():
                matched_users = serializer.save()
                print(serializer.data)

                # pass this point, they have a match
                user.found_match = True
                waiting_user.found_match = True
                user.save()
                waiting_user.save()
                # Send request to match making through messenger
            else:
                print("Serializer Not Valid", serializer.errors)
            return 
