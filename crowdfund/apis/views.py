from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from projects.models import *
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from datetime import date

class ListProjects(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ViewProject(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
# Must be authenticated
class CreateProject(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

# Must be authenticated
class UpdateProject(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

# Must be authenticated
class DeleteProject(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
            try:
                project = Project.objects.get(id=pk)
                current_fund_percentage = (project.current_fund / project.total_target)*100
                if  current_fund_percentage < 25:
                    project.delete()
                    return Response({'msg':'Project Deleted Successfully'},status.HTTP_200_OK)
                else:
                    return Response({'msg':"Sorry,\
                    you can't delete your project if it's current fund percentage is higher than 25%"},
                    status.HTTP_400_BAD_REQUEST)
            except Project.DoesNotExist:
                return Response({'msg':"Can't find project with given id"},status.HTTP_404_NOT_FOUND)


# Must be authenticated
class DonateFund(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        fund = float(request.POST.get('donation'))
        if fund:
            try:
                project = Project.objects.get(id=id)
                project.current_fund += fund
                project.save()
                return Response({'msg':"Thank you for your donation! <3"},status.HTTP_200_OK)
            except Project.DoesNotExist:
                return Response({'msg':"Can't find project with given id"},status.HTTP_404_NOT_FOUND)
        else:
            return Response({'msg':"Please check fund value"},status.HTTP_400_BAD_REQUEST)
 
# Must be authenticated
class ReportProject(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            project = Project.objects.get(id=id)
            token = request.META.get('HTTP_AUTHORIZATION','')
            token_key = token[6:]
            user = Token.objects.get(key=token_key).user
            if ProjectReport.objects.filter(user_reported=user,project=project):
                return Response({'msg':"You can't report the same project twice!"},status.HTTP_400_BAD_REQUEST)
            ProjectReport.objects.create(project=project,user_reported=user,report_date=date.today())
            project.reports_count += 1
            project.save()
            return Response({'msg':"Report sent successfully"},status.HTTP_201_CREATED)
        except:
            return Response({'msg':"Can't find project with given id"},status.HTTP_404_NOT_FOUND)



# Must be authenticated
# class RateProject(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, id):
#             try:
#                 project = Project.objects.get(id=id)
#                 token = request.META.get('HTTP_AUTHORIZATION','')
#                 token_key = token[6:]
#                 user = Token.objects.get(key=token_key).user
#                 if Rating.objects.filter(user_rated=user,project_id=project):
#                     return Response({'msg':"You can't rate the same project twice!"},status.HTTP_400_BAD_REQUEST)
#                 user_rating = request.POST.get('rating')
#                 Rating.objects.create(project_id=project,user_rated=user,rating=user_rating)
#                 rating_users_count = Rating.objects.filter(project_id=project).count()
#                 project.average_rate = project.total_rate / rating_users_count
#                 project.total_rate += user_rating
#                 project.save()
#                 return Response({'msg':"Rating sent successfully"},status.HTTP_201_CREATED)
#             except:
#                 return Response({'msg':"Can't find project with given id"},status.HTTP_404_NOT_FOUND)
