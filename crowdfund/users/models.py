from django.db import models


def image_upload(instance, imagename):
    extension = imagename.split(".")[1]
    return "users/%s.%s" % (instance.id, extension)


# Create your models here.
class Profile(models.Model):
    # todo: connect with auth_user
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField()
    profile_picture = models.ImageField(upload_to=image_upload)
    birth_date = models.DateField(blank=True,null=True)
    facebook_profile = models.URLField(blank=True,null=True)
    country = models.CharField(max_length=50,blank=True,null=True)
    # todo: projects

    def __str__(self):
        return self.username

# todo: user-project donation