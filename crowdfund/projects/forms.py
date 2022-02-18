from django import forms
from django.forms.models import inlineformset_factory
from .models import Project, ProjectPicture, Comment


class  ProjectPictureForm(forms.ModelForm):
    class Meta:
        model = ProjectPicture
        exclude = ()

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
        fields = ['title', 'details', 'total_target', 'current_fund', 'start_date', 'end_date', 'category']

ProjectPictureFormSet = inlineformset_factory(
    Project, ProjectPicture, form=ProjectPictureForm, fields=['picture'], extra=3, can_delete=True  # <- place where you can enter the nr of img
)

class  ProjectCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'project', 'user_commented']
        # def __init__(self, *args, **kwargs):
        #     """Save the request with the form so it can be accessed in clean_*()"""
        #     self.request = kwargs.pop('request', None)
        #     super(ProjectCommentForm, self).__init__(*args, **kwargs)