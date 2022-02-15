from dataclasses import fields
from rest_framework import serializers
from projects.models import *

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Project

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Rating

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag