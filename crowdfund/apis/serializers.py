from rest_framework import serializers
from projects.models import *
from django.db.models import Sum

class ProjectSerializer(serializers.ModelSerializer):
    average_rate = serializers.SerializerMethodField('calc_average_rate')
    current_fund = serializers.SerializerMethodField('calc_average_rate')
    def calc_average_rate(self, project):
        try:
            average_rate = Rating.objects.filter(project_id=project).aggregate(Sum('rating')).get('rating__sum') / Rating.objects.filter(project_id=project).count()
            return average_rate
        except ZeroDivisionError:
            return 0 
    
    class Meta:
        model = Project
        fields = ['id','title','details','total_target','current_fund','start_date','end_date',
        'reports_count','category','average_rate','featured','images','tag_set','comment_set']
        depth = 1
        

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ProjectPicture

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Rating
