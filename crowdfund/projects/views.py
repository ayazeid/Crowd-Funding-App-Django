from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from . import forms
from .models import Project

"""
--Project views--
users can only view, create, delete(only their own) projects
updating is prohibited according to our business logic
"""


class ProjectList(ListView):
    model = Project


class ProjectDetail(DetailView):
    pass


class ProjectCreate(CreateView):
    model = Project
    form_class = forms.ProjectCreateForm

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
