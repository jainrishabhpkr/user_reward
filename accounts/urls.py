from django.urls import path, include
from accounts import views
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt







urlpatterns = [
    path('createuser/', views.UserCreate.as_view(), name='account-create'),

    path('login/', views.LoginView.as_view(), name='login'),

    path('get_level_list/', views.LevelList.as_view(), name='get_limit'),
    path('get_action_list/', views.ActionList.as_view(), name='get_limit'),

    path('get_profile_info/', views.ProfileInfo.as_view(), name='get_limit'),
    path('get_points/', views.GetPoints.as_view(), name='create_review'),

    path('create_review/', views.CreateReview.as_view(), name='create_review'),
    path('create_short_story/', views.CreateShortStory.as_view(), name='create_short_story'),


    path('get_all_reviews/',views.GetAllReviews.as_view(), name='create_review'),
    path('get_all_short_stories/',views.GetShortStories.as_view(), name='create_review'),


    

]
