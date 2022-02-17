from django.contrib import admin
from .models import Project, Category, ProjectReport,Rating, ProjectPicture

admin.site.register(Project)
admin.site.register(Category)
admin.site.register(ProjectReport)
admin.site.register(Rating)
admin.site.register(ProjectPicture)
