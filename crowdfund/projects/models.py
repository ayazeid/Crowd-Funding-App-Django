from django.conf import settings
from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=30)


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=30)


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120)
    details = models.TextField()
    total_target = models.FloatField()
    current_fund = models.FloatField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    reports_count = models.IntegerField(default=0)
    average_rate = models.FloatField(default=0)
    # Needs Authentication app to be done first
    # project_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)  # Should populate category table with
    # at least one record to create a project (do not worry will not cause errors)


class ProjectPicture(models.Model):
    id = models.AutoField(primary_key=True)
    picture = models.ImageField()
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)


class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user_rated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    rating = models.FloatField()  # Rating out of 5


class ProjectReport(models.Model):
    class Meta:
        unique_together = (('project', 'user_reported', 'report_date'),)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_reported = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    report_date = models.DateField()