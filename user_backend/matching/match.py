from matching.models import WaitingUser
from matching.serializers import WaitingUserSerializer

def attempt_match(waiting_user):
    users = WaitingUser.objects.all()
            .filter(meal_period=waiting_user.meal_period)
            .filter(found_match=False)
    for user in users:
        if user.id != waiting_user.id:
            for hall in waiting_user.dining_hall:
                for time in waiting_user.times:
                    if hall in waiting_user.dining_halls and time in
                            waiting_user.times:
                        
                        # user at this point has been "matched"
                        # create a MatchedUserInstance
                        # send a request to the messaging
