from rest_framework import exceptions,serializers
from rest_framework.validators import UniqueValidator,UniqueTogetherValidator
from accounts.models import *
import django.contrib.auth.password_validation as validators

from django.contrib.auth import authenticate

from accounts.utils import (check_if_daily_short_story_limit_reached,
        check_if_daily_review_limit_reached,check_if_max_point_limit_reached,
        get_max_points_allowed)
from datetime import datetime



class UserSerializer(serializers.Serializer):


    password = serializers.CharField(write_only=True)
    username = serializers.CharField(max_length=150,required=True,
                validators=[UniqueValidator(queryset=User.objects.all(),message = 'username already exists')]
                 )
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)


    

    def validate(self, data):
        password = data.get('password')       

        username = data.get('username')
 
        username = username.lower()


        check_list = "abcdefghijklmnopqrstuvwxyz@.+-_0123456789"

        errors = dict()



        
        
        for character in username:
            if character not in check_list:
                errors['username'] = "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters."
                break

        

        try:
            validators.validate_password(password=password)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)



        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    # token = serializers.CharField(max_length = 600)

    def validate(self, attrs):
        print("attres is",attrs)
        authenticate_kwargs = {
            'username':attrs['username'],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass
        print("keyword argements is ",authenticate_kwargs)
        self.user = authenticate(**authenticate_kwargs)
        print("user is ",self.user)

        if self.user is None :
            raise exceptions.AuthenticationFailed(

                'No active account found with the given credentials',
            )

        if self.user.is_active is False:
            raise serializers.ValidationError("your account is inactive")

        return attrs




class CreateReviewSerializer(serializers.Serializer):
    content = serializers.CharField()
    def validate(self, data):

        request = self.context.get('request')
        user = request.user
        print('user is',user) 

        result1    = check_if_max_point_limit_reached(user,action_type='review')
        if result1 is True:
            mx_point = get_max_points_allowed()
            error_msg = "Maximum allowed points is {}".format(mx_point)
            raise serializers.ValidationError(error_msg)            

        result2 = check_if_daily_review_limit_reached(user)

        if result2 is True:
            error_msg = "Daily limit for points earned through review has been reached"
            raise serializers.ValidationError(error_msg)

        content = data['content']

        content = content.strip()

        if len(content) ==0:
            raise serializers.ValidationError("empty review not allowed")

        content = content.split(' ')

        if len(content) > 10:
            raise serializers.ValidationError("Review is more than 10 words")

        return data


class CreateShortStorySerializer(serializers.Serializer):
    content = serializers.CharField()
    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        print('user is',user) 
        result1    = check_if_max_point_limit_reached(user,action_type='short story')

        if result1 is True:
            mx_point = get_max_points_allowed()
            error_msg = "Maximum allowed points is {}".format(mx_point)
            raise serializers.ValidationError(error_msg)  

        result2 = check_if_daily_short_story_limit_reached(user)

        if result2 is True:
            error_msg = "Daily limit for points earned through short story has been reached"
            raise serializers.ValidationError(error_msg)

        content = data['content']

        content = content.strip()

        if len(content) ==0:
            raise serializers.ValidationError("empty story not allowed")

        content = content.split(' ')

        if len(content) > 50:
            raise serializers.ValidationError("story is more than 50 words")

        return data