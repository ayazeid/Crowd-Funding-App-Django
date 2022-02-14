from .models import Project
from django import forms


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
