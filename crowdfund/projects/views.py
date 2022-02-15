from gettext import translation
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from extra_views import CreateWithInlinesView, InlineFormSetFactory


from .forms import ProjectCreateForm, ProjectPictureForm, ProjectPictureFormSet
from .models import Project, ProjectPicture

"""
--Project views--
users can only view, create, delete(only their own) projects
updating is prohibited according to our business logic
"""


class ProjectList(ListView):
    model = Project


class ProjectDetail(DetailView):
    pass



class ProjectPictureMetaInline(InlineFormSetFactory):
    model = ProjectPicture
    fields = '__all__'


class ProjectCreate(CreateWithInlinesView):
    model = Project
    inlines = [ProjectPictureMetaInline,]
    template_name = 'projects/project_form.html'
    form_class = ProjectCreateForm


    def get_context_data(self, **kwargs):
        data = super(ProjectCreate, self).get_context_data(**kwargs)
        data['project_pictures'] = ProjectPictureFormSet()
        if self.request.POST:
            data['project_pictures'] = ProjectPictureFormSet(self.request.POST, self.request.FILES)
        else:
            data['project_pictures'] = ProjectPictureFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        form_img = context['project_pictures']
        with translation.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if form_img.is_valid():
                form_img.instance = self.object
                form_img.save()
        return super(ProjectCreate, self).form_valid(form)

    # Django built-in function for redirecting to another url on success
    def get_success_url(self):
        # Use the following line once you create DetailView to redirect to the newly created project
        # return reverse('projects', kwargs={'title': self.object.title})
        return reverse('projects') #localhost:8000/projects/run-for-amputees


class ProjectDelete(DeleteView):
    model = Project


"""
--Comments views--
"""
