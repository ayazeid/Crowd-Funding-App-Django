from django.conf import settings
from django.db import models
from datetime import date
from django.contrib.auth.models import User

""""
    click report -> Project(UpdateView) -> template: form (ok==sumbit) -> reverse('projects')

    click donate -> project(UpdateView):current_fund, UserDonations(UpdateView):{user_id-project_id-donation_amount} -> template: form (ok==sumbit) -> reverse('projects')
"""

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120)
    details = models.TextField()
    total_target = models.IntegerField()
    current_fund = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    reports_count = models.IntegerField(default=0)
    rating_users_count = models.IntegerField(default=0)
    total_rate = models.IntegerField(default=0)
    # Needs Authentication app to be done first
    project_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)  # Should populate category table with
    # at least one record to create a project (do not worry will not cause errors)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title


def image_upload(instance, filename):
    return f'project_images/{instance.project_id.id}/{filename}'

class ProjectPicture(models.Model):
    id = models.AutoField(primary_key=True)
    picture = models.ImageField(upload_to= image_upload)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')



RATING_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)

class Rating(models.Model):
    class Meta:
        unique_together = (('user_rated', 'project_id'),)

    id = models.AutoField(primary_key=True)
    user_rated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)  # Rating out of 5

    def __str__(self):
        return self.user_rated.username + ' - ' + self.project_id.title + " rating"


class ProjectReport(models.Model):
    class Meta:
        unique_together = (('project', 'user_reported', 'report_date'),)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_reported = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    report_date = models.DateField()

    def __str__(self):
        return self.user_reported.username + ' - ' + self.project.title + " report"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_commented = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    created_time = models.DateTimeField(auto_now_add=True)
    reports_count = models.IntegerField(default=0)
 

class ReportComment(models.Model):
    class Meta:
        unique_together = (('comment', 'user_reported', 'report_date'),)
    id = models.AutoField(primary_key=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user_reported = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    report_date = models.DateField()


class UserDonation(models.Model):
    id = models.AutoField(primary_key=True)
    user_donated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=30, default='')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.tag_name

