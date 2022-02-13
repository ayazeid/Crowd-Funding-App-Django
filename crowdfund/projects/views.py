from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Project

"""
--Project views--
users can only view, create, delete(only their own) projects
updating is prohibited according to our business logic
"""


class ProjectList(ListView):
    model = Project


class ProjectCreate(CreateView):
    model = Project
    fields = '__all__'


class ProjectDelete(DeleteView):
    model = Project


"""
--Comments views--
"""
