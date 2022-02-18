from multiprocessing import context
from django.shortcuts import render
from projects.models import Project,Category
from django.db.models import Count
# Create your views here.

def top_rated(request):

    categories = Category.objects.all()

    latest_projects = Project.objects.all().order_by('-id')[:5]

    admin_projects = Project.objects.filter(featured=1).order_by('-id')[:5]

    top_rated_projects_id=Project.objects.values('id').annotate(num_projects=Count('total_rate')).order_by('-total_rate')[:5]
    top_rated_projects=[]
    for i in top_rated_projects_id:
        project=Project.objects.filter(id=i["id"])[0]
        top_rated_projects.append(project)

    return render(request,'home/index.html' ,{"latest_projects":latest_projects,"top_rated_projects":top_rated_projects,"categories":categories,"admin_projects":admin_projects })

def projectCategories(request):
    if request.method == 'POST':
        category = request.POST.get('categories')
        category_projects = Project.objects.filter(category_id=category)
        return render(request,'home/categoryProjects.html' , {"category_projects":category_projects })


def SearchTitle(request):
    title=request.POST.get('title')
    search_by_title =Project.objects.filter(title__contains=title)
    return render(request,'home/searchTitle.html' ,{"search_by_title":search_by_title})