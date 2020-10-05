from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date
from accounts.models import *

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def get_max_points_allowed():

    level_object = Level.objects.all().order_by('-max_point')[0]

    max_point = level_object.max_point
    return max_point

def get_points_earned_for_review(user):
 

    single_day_list = Review.objects.filter(user=user,created_date__date=date.today())
    
    single_day_list = single_day_list.values_list('points_earned',flat=True)

    if len(single_day_list)==0:
        single_day_points = 0
    else:
        single_day_points = sum(single_day_list)

    print("single_day_points for review is",single_day_points)

    overall_list = Review.objects.filter(user=user)
    
    overall_list = overall_list.values_list('points_earned',flat=True)

    if len(overall_list)==0:
        overall_points = 0
    else:
        overall_points = sum(overall_list)

    print("overall_points is",overall_points)
    return single_day_points,overall_points


def get_points_earned_for_short_story(user):
    single_day_list = ShortStory.objects.filter(user=user,created_date__date=date.today())
    
    single_day_list = single_day_list.values_list('points_earned',flat=True)

    if len(single_day_list)==0:
        single_day_points = 0
    else:
        single_day_points = sum(single_day_list)

    print("single_day_points  for short story is",single_day_points)

    overall_list = ShortStory.objects.filter(user=user)    
    overall_list = overall_list.values_list('points_earned',flat=True)

    if len(overall_list)==0:
        overall_points = 0
    else:
        overall_points = sum(overall_list)

    print("overall_points is",overall_points)
    return single_day_points,overall_points



def check_if_daily_review_limit_reached(user):
    single_day_points,overall_points = get_points_earned_for_review(user)


    current_level = user.current_level
    action_object = Action.objects.get(name='short review in 10 words')
    current_point_limit_for_day = action_object.current_point_limit_for_day

    points_object = Points.objects.get(action=action_object,level=current_level)

    points_to_be_earned = points_object.points

    if single_day_points + points_to_be_earned > current_point_limit_for_day :
        return True
    else:
        False


def check_if_daily_short_story_limit_reached(user):
    single_day_points,overall_points = get_points_earned_for_short_story(user)


    current_level = user.current_level
    action_object = Action.objects.get(name='short story in 50 words')
    current_point_limit_for_day = action_object.current_point_limit_for_day

    points_object = Points.objects.get(action=action_object,level=current_level)

    points_to_be_earned = points_object.points

    if single_day_points + points_to_be_earned > current_point_limit_for_day :
        return True
    else:
        False


def check_if_max_point_limit_reached(user,action_type):

    print("action_type is",action_type)
    if action_type == 'short story':
        action_object = Action.objects.get(name='short story in 50 words')
        single_day_points,overall_points = get_points_earned_for_short_story(user)
    elif action_type == 'review':
        action_object = Action.objects.get(name='short review in 10 words')
        single_day_points,overall_points = get_points_earned_for_review(user)

    
    current_level = user.current_level    
    points_object = Points.objects.get(action=action_object,level=current_level)
    points_to_be_earned = points_object.points
    max_point = get_max_points_allowed()

    print("overall_points + points_to_be_earned",overall_points + points_to_be_earned)
    print("max_point is",max_point)

    if overall_points + points_to_be_earned > max_point :
        return True
    else:
        False


