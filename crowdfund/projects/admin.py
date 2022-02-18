from django.contrib import admin
<<<<<<< HEAD
from .models import *
admin.site.register(Project)
admin.site.register(Category)
admin.site.register(ProjectReport)
admin.site.register(Tag)
admin.site.register(ProjectPicture)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(ReportComment)
admin.site.register(UserDonation)
=======
from .models import Project, Category, ProjectReport, Rating, ProjectPicture

admin.site.register(Project)
admin.site.register(Category)
admin.site.register(ProjectReport)
admin.site.register(ProjectPicture)
admin.site.register(Rating)
>>>>>>> 034d448980305ec0d243b5d95779493e3862d54a
