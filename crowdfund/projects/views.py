from django.shortcuts import redirect
from django.db import transaction
from django.urls import reverse, reverse_lazy
from extra_views import CreateWithInlinesView, InlineFormSetFactory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .forms import ProjectCreateForm, ProjectRatingForm, ProjectPictureFormSet, ProjectTagFormSet
from .models import Project, ProjectPicture, Comment, Tag, UserDonation, Rating, ProjectReport
from datetime import datetime
"""
--Project views--
users can only view, create, delete(only their own) projects
updating is prohibited according to our business logic
"""



class ProjectList(ListView):
    model = Project


class ProjectDetail(DetailView):
    model = Project
    def get_context_data(self, **kwargs):
        data = super(ProjectDetail, self).get_context_data(**kwargs)
        data['current_user'] = self.request.user
        data['pics'] = ProjectPicture.objects.filter(project_id = self.kwargs["pk"])
        return data


class ProjectPictureMetaInline(InlineFormSetFactory):
    model = ProjectPicture
    fields = '__all__'


class ProjectTagMetaInline(InlineFormSetFactory):
    model = Tag
    fields = '__all__'


class ProjectCreate(LoginRequiredMixin, CreateWithInlinesView):
    model = Project
    inlines = [ProjectPictureMetaInline,ProjectTagMetaInline]
    login_url = reverse_lazy('signin')
    template_name = 'projects/project_form.html'
    form_class = ProjectCreateForm


    def get_context_data(self, **kwargs):
        data = super(ProjectCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['project_pictures'] = ProjectPictureFormSet(self.request.POST, self.request.FILES)
            data['project_tags'] = ProjectTagFormSet(self.request.POST)
        else:
            data['project_pictures'] = ProjectPictureFormSet()
            data['project_tags'] = ProjectTagFormSet()
        return data

    def form_valid(self, form):
        form.instance.project_owner = self.request.user
        form.save()
        # with transaction.atomic():

        return super(ProjectCreate, self).form_valid(form)

    # Django built-in function for redirecting to another url on success
    def get_success_url(self):
        # Use the following line once you create DetailView to redirect to the newly created project
        # return reverse('projects', kwargs={'title': self.object.title})
        return reverse('projects') #localhost:8000/projects/run-for-amputees



def projectDelete(request, pk):
    project = Project.objects.get(id=pk)
    current_fund_percentage = (project.current_fund / project.total_target)*100
    if  current_fund_percentage < 25 and request.user.id == project.project_owner.id:
        project.delete()
        return redirect("projects")
    else:
        return HttpResponse("Not allowed to delete this project!")


def projectReport(request, pk):
    project = Project.objects.get(id=pk)
    try:
        new_report = ProjectReport(project=project, user_reported=request.user, report_date=datetime.today().strftime('%Y-%m-%d'))
        new_report.save()
        project.reports_count = project.reports_count + 1
        project.save()
        return redirect("projects")
    except:
        return redirect("projects")

"""
--Comments views--
"""


class CommentCreate(CreateView):
    model = Comment
    fields = ['content', 'project', 'user_commented']
    
    def get_context_data(self, **kwargs):
        context = super(CommentCreate, self).get_context_data(**kwargs)
        # print(self.kwargs["pk"])
        context['pro_id'] = self.kwargs["pk"]
        context['user_commented_id'] = self.request.user.id
        return context

    def get_success_url(self):
        return reverse('details-project', kwargs={'pk': self.object.project.id})


"""
--Donations views--
"""

class DonateCreate(LoginRequiredMixin, CreateView):
    model = UserDonation
    login_url = reverse_lazy('signin')
    fields = ['amount', 'project', 'user_donated']

    def get_context_data(self, **kwargs):
        context = super(DonateCreate, self).get_context_data(**kwargs)
        context['project_id'] = self.kwargs["pk"]
        context['user_donated_id'] = self.request.user.id
        return context

    def form_valid(self, form):
        # context = self.get_context_data()
        # project_id = context['project_id']
        # donation_amount = context['form'].instance.amount
        # print(context['form'])
        # project = Project.objects.filter(id=project_id)[0]
        # project.current_fund += 2
        # project.save()
        form.save()
        return super(DonateCreate, self).form_valid(form)


    def get_success_url(self):
        return reverse('details-project', kwargs={'pk': self.object.project.id})
    
    # def form_invalid(self, form):
    #     return redirect("projects")



"""
--Rating views--
"""
class RateCreate(LoginRequiredMixin, CreateView):
    model = Rating
    login_url = reverse_lazy('signin')
    form_class = ProjectRatingForm

    def get_context_data(self, **kwargs):
        context = super(RateCreate, self).get_context_data(**kwargs)
        context['project_id'] = self.kwargs["pk"]
        context['user_rated_id'] = self.request.user.id
        return context
        
    def get_success_url(self):
        return reverse('details-project', kwargs={'pk': self.object.project_id.id})

    def form_invalid(self, form):
        return redirect("projects")
