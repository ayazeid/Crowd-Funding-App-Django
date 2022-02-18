from rest_framework import serializers
from users.models import Profile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','username','email')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        fields = '__all__'
        model = Profile




