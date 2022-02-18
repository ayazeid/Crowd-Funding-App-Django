from django import forms
from django.forms.models import inlineformset_factory
from .models import Project, ProjectPicture, Comment, Tag


class  ProjectPictureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectPictureForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control cf-dy-hidden'
            visible.label = ''

    class Meta:
        model = ProjectPicture
        fields = ['picture',]


class ProjectTagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectTagForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.label = ''

    class Meta:
        model = Tag
        fields = ['tag_name',]


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
        fields = ['title', 'total_target', 'start_date', 'end_date', 'category', 'details']

ProjectPictureFormSet = inlineformset_factory(
    Project, ProjectPicture, form=ProjectPictureForm, fields=['picture'], extra=5, can_delete=False
)

ProjectTagFormSet = inlineformset_factory(
    Project, Tag, form=ProjectTagForm, fields=['tag_name'], extra=5, can_delete=False
)

class  ProjectCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'project', 'user_commented']
        # def __init__(self, *args, **kwargs):
        #     """Save the request with the form so it can be accessed in clean_*()"""
        #     self.request = kwargs.pop('request', None)
        #     super(ProjectCommentForm, self).__init__(*args, **kwargs)
