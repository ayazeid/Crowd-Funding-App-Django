from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from projects.models import *
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from datetime import date

class ListProjects(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ViewProject(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
# Must be authenticated
class CreateProject(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        project_serializer = ProjectSerializer(data=request.data)
        if project_serializer.is_valid():
            project = project_serializer.save()
            for image in request.FILES.getlist('images'):
                project_image_serializer = ProjectImageSerializer(data={'project_id':project.id,'picture':image})
                if project_image_serializer.is_valid():
                    project_image_serializer.save()
                else:
                    project.delete()
                    return Response({
                        "msg":"There is a problem with project images.",
                        "errors": project_image_serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                        "msg":"Project created successfully",
                        "data":project_serializer.data
                    }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                        "msg":"There is a problem with project data.",
                        "errors": project_serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)

# Must be authenticated
class UpdateProject(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

class UpdateProjectImages(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, id):
        try:
            project = Project.objects.get(id=id)
            #current images
            project_images = ProjectPicture.objects.filter(project_id=id)
            #images in request
            images = request.FILES.getlist('images')
            
            #no new images
            if len(images) == 0:
                return Response({
                    "msg":"No images provided, Your project images will still the same",
                    "data":ProjectSerializer(project).data
                }, status=status.HTTP_200_OK)
            
            #there is new images, so delete old images and add new ones
            for image in images:
                new_image_serializer = ProjectImageSerializer(data={'project_id':project.id,'picture':image})
                if not new_image_serializer.is_valid():
                    return Response({
                        'msg':'There is a problem in your images'
                    },status=status.HTTP_400_BAD_REQUEST)

            [image.delete() for image in project_images]

            for image in images:
                new_image_serializer = ProjectImageSerializer(data={'project_id':project.id,'picture':image})
                if new_image_serializer.is_valid():
                    new_image_serializer.save()
            return Response({
            "msg":"Project images updated successfully",
            "data":ProjectSerializer(project).data
                }, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({
                'msg':"Can't find project with the given id"
                },status.HTTP_404_NOT_FOUND)

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
class RateProject(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
            try:
                project = Project.objects.get(id=id)
                token = request.META.get('HTTP_AUTHORIZATION','')
                token_key = token[6:]
                user = Token.objects.get(key=token_key).user
                if Rating.objects.filter(user_rated=user,project_id=project):
                    return Response({'msg':"You can't rate the same project twice!"},status.HTTP_400_BAD_REQUEST)
                user_rating = request.POST.get('rating')
                Rating.objects.create(project_id=project,user_rated=user,rating=user_rating)
                project.rating_users_count += 1
                project.total_rate += int(user_rating)
                project.save()
                return Response({'msg':"Rating sent successfully"},status.HTTP_201_CREATED)
            except:
                return Response({'msg':"Can't find project with given id"},status.HTTP_404_NOT_FOUND)
