from django import forms
from django.forms.models import inlineformset_factory
from .models import Project, ProjectPicture


class  ProjectPictureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectPictureForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control cf-dy-hidden'
            visible.label = ''

    class Meta:
        model = ProjectPicture
        fields = ['picture',]

class ProjectCreateForm(forms.ModelForm):
    """
    After authentication is done, implement this solution to get project_owner
    https://stackoverflow.com/questions/19051830/a-better-way-of-setting-values-in-createview
    """
    def __init__(self, *args, **kwargs):
        super(ProjectCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Project
        fields = ['title', 'total_target', 'current_fund', 'start_date', 'end_date', 'category', 'details']

ProjectPictureFormSet = inlineformset_factory(
    Project, ProjectPicture, form=ProjectPictureForm, fields=['picture'], extra=5, can_delete=False
)