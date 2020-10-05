from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import *
from accounts.models import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny

from datetime import date
from accounts.utils import (get_tokens_for_user,get_points_earned_for_review,
    get_points_earned_for_short_story)




class UserCreate(APIView):
    permission_classes = [AllowAny,]
    
    def post(self, request, *args,**kwargs):
        serializer = UserSerializer(data=request.data)
        success = {}
        error = {}
        if serializer.is_valid():
            data=serializer.data
            
            password=request.data['password']
            username=data['username']
            
            first_name=data['first_name']
            last_name=data['last_name']
            
       
            try:
                user= User.objects.create_user(first_name=first_name,
                    last_name=last_name,password=password,username=username)
            except Exception as e:
                pass



            level_object = Level.objects.all().order_by('min_point')[0]

            print("level object name is",level_object.name)
        
            user.current_level = level_object
            user.save()


            if user:               
                token = get_tokens_for_user(user=user)
                json_data = serializer.data

                json_data['user_id'] = user.id

                json_data['access'] = token['access']
                json_data['refresh'] = token['refresh']



                return Response({"success":json_data,"error":error}, status=status.HTTP_201_CREATED)
        errors = serializer.errors
        print("error is ",errors)
        return Response({"error":serializer.errors,"success":success}, status=status.HTTP_400_BAD_REQUEST)




class LoginView(APIView):
    permission_classes = [AllowAny,]
    def post(self,request):
        success = {}
        error = {}

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token = get_tokens_for_user(user=user)

            access = token['access']
            refresh = token['refresh']
            user_id = user.id
            
            token = {'refresh': str(refresh), 'access': str(access),'user_id':user_id}  

            return Response({"success":token,"error":error}, status=200)

        return Response({"detail":serializer.errors,"success":{}}, status=401)

class ActionList(APIView):
    permission_classes = [AllowAny,]
    def get(self,request):

        success = {}
        error = {}
        
        to_send = Action.objects.all().values('id','name','current_point_limit_for_day','description')
      
        
        return Response({"success":to_send,"error":error}, status=200)
        
class LevelList(APIView):
    permission_classes = [AllowAny,]
    def get(self,request):

        success = {}
        error = {}
        
        to_send = Level.objects.all().order_by('max_point').values('id','name','min_point','max_point')
        
        
        return Response({"success":to_send,"error":error}, status=200)
     
class ProfileInfo(APIView):
    def get(self, request, format='json'):
        success = {}
        error = {}

        user = request.user
        username = user.username
        first_name = user.first_name
        last_name = user.last_name
        user_id = user.id
        current_level = user.current_level.name
        total_points = user.total_points


        to_send = {
            
            'username':username,
            'first_name':first_name,
            'last_name':last_name,
            'user_id':user_id,
            'current_level':current_level,
            'total_points':total_points



        }
        return Response({"success":to_send,"error":error}, status=200)

        


class CreateReview(APIView):
    def post(self, request, *args,**kwargs):
        serializer = CreateReviewSerializer(data=request.data,context={'request': request})
        success = {}
        error = {}
        if serializer.is_valid():
            data=serializer.data
            content=data['content'] 

            user=request.user
            current_level = user.current_level
            action_object = Action.objects.get(name='short review in 10 words')

            points_object = Points.objects.get(action=action_object,level=current_level)
            points_earned = points_object.points
                  
            review_object = Review.objects.create(content=content,points_earned=points_earned,user=user)           
            total_points = user.total_points + points_earned
            print("total_points is",total_points)
            user.total_points = total_points

            new_level_object = Level.objects.filter(max_point__gte=total_points).order_by('max_point')[0]
            print("level_object is",new_level_object)
            user.current_level = new_level_object
            
            user.save()

            if current_level == new_level_object:
                is_level_upgraded = False
            else:
                is_level_upgraded = True

            to_send = {"review_id":review_object.id,"points_earned":points_earned,
                    'is_level_upgraded':is_level_upgraded,'current_level':new_level_object.name,
                    "user_total_points":user.total_points}

            return Response({"success":to_send,"error":error}, status=201)

        return Response({"error":serializer.errors,"success":success}, status=400)




class CreateShortStory(APIView):
    def post(self, request, *args,**kwargs):
        serializer = CreateShortStorySerializer(data=request.data,context={'request': request})
        success = {}
        error = {}
        if serializer.is_valid():
            data=serializer.data

            content=data['content']
            
            user=request.user
            current_level = user.current_level
            action_object = Action.objects.get(name='short story in 50 words')

            points_object = Points.objects.get(action=action_object,level=current_level)
            points_earned = points_object.points
                   
            story_object = ShortStory.objects.create(content=content,points_earned=points_earned,user=user)           
            total_points = user.total_points + points_earned
            print("total_points is",total_points)
            user.total_points = total_points

            new_level_object = Level.objects.filter(max_point__gte=total_points).order_by('max_point')[0]
            print("level_object is",new_level_object)
            user.current_level = new_level_object
            
            user.save()

            if current_level == new_level_object:
                is_level_upgraded = False
            else:
                is_level_upgraded = True

            to_send = {"story_id":story_object.id,"points_earned":points_earned,
                    'is_level_upgraded':is_level_upgraded,'current_level':new_level_object.name,
                    "user_total_points":user.total_points}
                    
            return Response({"success":to_send,"error":error}, status=201)

        return Response({"error":serializer.errors,"success":success}, status=400)



class GetPoints(APIView):
    def get(self, request, format='json'):
        success = {}
        error = {}

        user = request.user
        dt = datetime.now()

        date = dt.strftime("%d-%m-%Y")
        print("date is",date)
        review_points_for_day,overall_review_points = get_points_earned_for_review(user)
        short_stories_points_for_day,overall_short_stories_points  = get_points_earned_for_short_story(user)

        point_for_day = review_points_for_day + short_stories_points_for_day

        overall_points = overall_review_points + overall_short_stories_points

   

        to_send = {
            
            "review_points_for_day":review_points_for_day,
            "short_stories_points_for_day":short_stories_points_for_day,
            "overall_review_points":overall_review_points,
            "overall_short_stories_points":overall_short_stories_points,
            "point_for_day":point_for_day,
            "overall_points":overall_points,

            "date":date,


        }
        
        return Response({"success":to_send,"error":error}, status=200)
       


class GetAllReviews(APIView):
    def get(self, request, format='json'):
        success = {}
        error = {}

        user = request.user
        review_list = Review.objects.filter(user=user).order_by('-created_date')
        review_list = review_list.values('id','content','points_earned','created_date')

   

        to_send = review_list
        
        return Response({"success":to_send,"error":error}, status=200)



class GetShortStories(APIView):
    def get(self, request, format='json'):
        success = {}
        error = {}

        user = request.user
        review_list = ShortStory.objects.filter(user=user).order_by('-created_date')
        review_list = review_list.values('id','content','points_earned','created_date')

   

        to_send = review_list
        
        return Response({"success":to_send,"error":error}, status=200)