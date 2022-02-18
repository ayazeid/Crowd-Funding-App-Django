from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from extra_views import CreateWithInlinesView, InlineFormSetFactory



from .forms import ProjectCreateForm, ProjectPictureForm, ProjectPictureFormSet
from .models import Project, ProjectPicture, Comment

"""
--Project views--
users can only view, create, delete(only their own) projects
updating is prohibited according to our business logic
"""



class ProjectList(ListView):
    model = Project


class ProjectDetail(DetailView):
    model = Project


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
        if self.request.POST:
            data['project_pictures'] = ProjectPictureFormSet(self.request.POST, self.request.FILES)
        else:
            data['project_pictures'] = ProjectPictureFormSet()
        return data

    def form_valid(self, form):
        form.instance.project_owner = self.request.user
        form.save()
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


class CommentCreate(CreateView):
    model = Comment
    # template_name = 'projects/project_detail.html'
    fields = ['content', 'project', 'user_commented']
    # def get_absolute_url(self):
    #     return reverse('details-project', args=[str(self.pk)])

    # def form_valid(self, form):
    #     project = get_object_or_404(Project, project=self.kwargs['id'])
    #     form.instance.user_commented = self.request.user
    #     form.instance.project = project
    #     form.save()
    #     return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(CommentCreate, self).get_context_data(**kwargs)
        print(self.kwargs["pk"])
        context['pro_id'] = self.kwargs["pk"]
        return context

    def get_success_url(self):
        return reverse('projects')
