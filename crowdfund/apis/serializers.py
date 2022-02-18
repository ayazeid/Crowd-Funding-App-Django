from rest_framework import serializers
from projects.models import *

# class ProjectListSerializer(serializers.ModelSerializer):

class ProjectSerializer(serializers.ModelSerializer):
    average_rate = serializers.SerializerMethodField('calc_average_rate')

    def calc_average_rate(self, project):
        try:
            average_rate = project.total_rate / project.rating_users_count
            return average_rate
        except ZeroDivisionError:
            return 0 
    
    class Meta:
        model = Project
        fields = ['id','title','details','total_target','current_fund','start_date','end_date',
        'reports_count','rating_users_count','total_rate','category','average_rate','images']
        depth = 1
        

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ProjectPicture

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Rating

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag