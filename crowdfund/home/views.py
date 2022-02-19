from multiprocessing import context
from django.shortcuts import render,redirect
from projects.models import Project,Category,Tag,Rating
from django.db.models import Count,Sum
# Create your views here.

def top_rated(request):
 
    categories = Category.objects.all()

    latest_projects = Project.objects.all().order_by('-id')[:5]

    admin_projects = Project.objects.filter(featured=1).order_by('-id')[:5]
    top_projects=Project.objects.all()
    project_list=[]
    for project in top_projects:
        total_rate = Rating.objects.filter(project_id=project).aggregate(Sum('rating')).get('rating__sum')
        raters_count = Rating.objects.filter(project_id=project).count()
        try:
            rating= total_rate / raters_count
        except:
            rating= 0
        project_list.append({'project':project,'rating':rating})
    top_rated_projects = sorted(project_list, key=lambda d: d['rating'],reverse=True)[:5]
    return render(request,'home/index.html' ,{"latest_projects":latest_projects,"top_rated_projects":top_rated_projects,"categories":categories,"admin_projects":admin_projects })

def projectCategories(request):
   
    if request.method == 'POST':
        category = request.POST.get('categories')
        category_projects = Project.objects.filter(category_id=category)
        return render(request,'home/categoryProjects.html' , {"category_projects":category_projects })


def SearchTitle(request):
    title=request.POST.get('title')
    if title == "":
         return render(request, 'home/invalidValue.html')
    search_by_title =Project.objects.filter(title__contains=title)
    if not search_by_title :
        return render(request, 'home/noSearchValue.html')
    else:
        return render(request,'home/searchTitle.html' ,{"search_by_title":search_by_title})
  
def SearchTag(request):
 
    tag = request.POST.get('tag')
    if tag == "":
         return render(request, 'home/invalidValue.html')
    search_by_tag=Tag.objects.filter(tag_name__contains=tag)
    if not search_by_tag :
        return render(request, 'home/noSearchValue.html')
    else:
        return render(request,'home/searchTag.html' ,{"search_by_tag":search_by_tag })
 