import re
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User



# egyptian phone number validation
def validate_egyptian_number(value):
    if not any(re.match(pattern, value) for pattern in [r"011+[0-9]{8}", r"012+[0-9]{8}", r"015+[0-9]{8}"]):
        raise ValidationError(
            _('%(value)s is not a valid egyptian number'),
            params={'value': value},
        )




def image_upload(instance, imagename):
    extension = imagename.split(".")[1]
    return "users/%s.%s" % (instance.id, extension)



# Create your models here.
class Profile(models.Model):
    # connect with auth_user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11,null=True,validators=[validate_egyptian_number],error_messages ={
                    "required":"this is not a valid egyptian number"
                    })
    profile_picture = models.ImageField(upload_to=image_upload,null=True)
    birth_date = models.DateField(null=True,blank=True)
    facebook_profile = models.URLField(null=True,blank=True)
    country = models.CharField(max_length=50,null=True,blank=True)
    # todo: projects

    def __str__(self):
        return str(self.user)

    



# todo: user-project donation