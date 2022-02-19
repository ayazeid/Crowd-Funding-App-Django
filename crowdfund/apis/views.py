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
class UpdateProject(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def put(self, request, pk):
        try:
            project = Project.objects.get(id=pk)
            if project.project_owner == request.user:
                request_images = request.FILES.getlist('images')
                project_serializer = ProjectSerializer(project,data=request.data)
                if project_serializer.is_valid():
                    project_images = ProjectPicture.objects.filter(project_id=pk)
                    #images in request
                    images = request_images
                    
                    if images and len(images) > 0:
                    #there are new images, so delete old images and add new ones
                        for image in images:
                            new_image_serializer = ProjectImageSerializer(data={'project_id':project.id,'picture':image})
                            if not new_image_serializer.is_valid():
                                return Response({
                                    'msg':'There is a problem in your images',
                                    'error':new_image_serializer.errors
                                },status=status.HTTP_400_BAD_REQUEST)

                        [image.delete() for image in project_images]

                        for image in images:
                            new_image_serializer = ProjectImageSerializer(data={'project_id':project.id,'picture':image})
                            if new_image_serializer.is_valid():
                                new_image_serializer.save()
             
                    project_serializer.save()
                    return Response({
                        'msg':'Project Updated Successfully',
                        'data': project_serializer.data
                    },status=status.HTTP_200_OK)
                else:
                    return Response({
                        'errors':project_serializer.errors
                    },status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'errors':"You can't update a project that you didn't create"
                },status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                'error':'Project not found',
            },status=status.HTTP_404_NOT_FOUND)

# Must be authenticated
class DeleteProject(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
            try:
                project = Project.objects.get(id=pk)
                if project.project_owner == request.user:
                    project_current_fund = UserDonation.objects.filter(project=project).aggregate(Sum('amount')).get('amount__sum')
                    print(project_current_fund)
                    current_fund_percentage = (project_current_fund / project.total_target)*100
                    if  current_fund_percentage < 25:
                        project.delete()
                        return Response({'msg':'Project Deleted Successfully'},status.HTTP_200_OK)
                    else:
                        return Response({'msg':"Sorry, you can't delete your project if it's current fund percentage is higher than 25%"},
                        status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'msg':"You can't delete a project that you didn't create"},
                    status.HTTP_401_UNAUTHORIZED)                    
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
                UserDonation.objects.create(user_donated=request.user,project=project,amount=fund)
                project_current_fund = UserDonation.objects.filter(project=project).aggregate(Sum('amount')).get('amount__sum')
                if project_current_fund >= project.total_target:
                    project.delete()
                    return Response({'msg':"Project Fund has reached the target! ^^"},status.HTTP_200_OK)
                else:
                    project.save()
                    return Response({'msg':"Thank you for your donation! <3"},status.HTTP_200_OK)
            except Project.DoesNotExist:
                return Response({'msg':"Can't find project with given id"},status.HTTP_404_NOT_FOUND)
        else:
            return Response({'msg':"Please check donation value"},status.HTTP_400_BAD_REQUEST)
 
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
                project.save()
                return Response({'msg':"Rating sent successfully"},status.HTTP_201_CREATED)
            except:
                return Response({'msg':"Can't find project with given id"},status.HTTP_404_NOT_FOUND)

class CommentProject(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            project = Project.objects.get(id=pk)
            comment_serializer = CommentSerializer(data={'content':request.data.get('content'),
            'user_commented':request.user.id,'project':project.id})
            if comment_serializer.is_valid():
                comment_serializer.save()
                return Response({
                    'msg':'comment added successfully'
                },status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'errors':'comment data is not valid',
                    'exc':f'{comment_serializer.errors}'
                },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'errors':'Project not found',
                'exception':f'{e}'
            },status=status.HTTP_404_NOT_FOUND)

class ReportProjectComment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
            user = request.user
            if ReportComment.objects.filter(user_reported=user,comment=comment):
                return Response({'msg':"You can't report the same comment twice!"},status.HTTP_400_BAD_REQUEST)
            ReportComment.objects.create(comment=comment,user_reported=user,report_date=date.today())
            comment.reports_count += 1
            comment.save()
            return Response({'msg':"Report sent successfully"},status.HTTP_201_CREATED)
        except:
            return Response({
                'msg':"Can't find comments with given id",
                },status.HTTP_404_NOT_FOUND)