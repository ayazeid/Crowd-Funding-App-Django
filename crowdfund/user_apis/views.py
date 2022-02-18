from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from users.models import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from crowdfund import settings
from django.utils import timezone
from datetime import timedelta
class Login(ObtainAuthToken):

    def post(self, request):
        serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
        if not serializer.is_valid():
            return Response({'error':'Invalid user data'},
            status=status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data['user']
        if user.is_active == False:
            return Response({
                'error':'Sorry, your account is not activated'
            }, status=status.HTTP_401_UNAUTHORIZED)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username':user.username,
            'profile_id':user.profile.id,
            'email': user.email
        })
class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'msg':'Successfully logged out'},status.HTTP_200_OK)

class Register(APIView):

    parser_classes = [MultiPartParser, FormParser]

    def send_mail(self, html,to_email):
        msg=MIMEMultipart('alternative')
        msg['From']='ITI CrowdFunding'
        msg['To']=to_email
        msg['Subject']='ITI Crowd Funding Account Activation'

        html_part = MIMEText(f"<h1>Here is your activation link:</h1><h3><a href={html}>Click here\
        to activate your account</a></h3>", 'html')
        msg.attach(html_part)
        msg_str=msg.as_string()

        server=smtplib.SMTP(host=settings.EMAIL_HOST,port=settings.EMAIL_PORT)
        server.ehlo()
        server.starttls()
        server.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
        server.sendmail(msg['From'],to_email,msg_str)
        server.quit()

    user = None

    def post(self, request):
        user_keys = ['username','password','first_name','last_name','email']
        user_dict = {}
        profile_dict = {}
        for key in request.data:
            if key in user_keys:
                user_dict[key]=request.data.get(key)
            else:
                if key == 'profile_picture':
                    continue
                else:
                    profile_dict[key]=request.data.get(key)
                
        if user_dict.get('username') and user_dict.get('password') and user_dict.get('email'):
            try:
                self.user = User.objects.create_user(**user_dict,is_active=False)
                profile = Profile.objects.create(**profile_dict,user=self.user)
                profile.profile_picture = request.data.get('profile_picture')
                profile.save()
                token, created = Token.objects.get_or_create(user=self.user)
                activation_link = f"http://127.0.0.1:8000/user_api/{self.user.id}/{token.key}"
                self.send_mail(activation_link,self.user.email)
                return Response({
                    'data':'we sent you a verification email, please check it and click the link',
                },status=status.HTTP_200_OK)
            except Exception as e:
                if isinstance(self.user,User):
                    self.user.delete()
                return Response({
                    'errors':f'Error : {e}',
                },status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'errors':'username and email and password are required',
            },status=status.HTTP_400_BAD_REQUEST)

class ActivateUser(APIView):
    def get(self, request, pk, token):
        try:
            user = Token.objects.get(key=token).user
            if user.id == pk:
                time_passed = timezone.now() - user.date_joined 
                if not time_passed >= timedelta(hours=24):
                    user.is_active = True
                    user.save()
                    return Response({
                        'msg':'User activated successfully'
                    },status=status.HTTP_200_OK)
                else:
                     return Response({
                        'error':'Sorry the link is expired'
                    },status=status.HTTP_400_BAD_REQUEST)                       
        except:
            return Response({
                    'error':'User not found',
                },status=status.HTTP_404_NOT_FOUND)

class DeleteUser(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        password = request.data.get('password')
        user = request.user
        if password and user.check_password(password):
            user.delete()
            return Response({
                'msg':'User deleted successfully'
            },status=status.HTTP_200_OK)
        else:
            return Response({
                'error':'Password is not given or incorrect'
            },status=status.HTTP_400_BAD_REQUEST)

class ViewProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            return Response({
                'data':ProfileSerializer(user.profile).data
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error':'Something wrong happened'
            },status=status.HTTP_400_BAD_REQUEST)

class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request):
        try:
            user = request.user
            profile = request.user.profile
            user_keys = ['username','password','first_name','last_name']
            user_dict = {}
            profile_dict = {}
            for key in request.data:
                if key in user_keys:
                    user_dict[key]=request.data.get(key)
                else:
                    profile_dict[key]=request.data.get(key)  
            #updating user data
            for key,val in user_dict.items():
                if key != 'password':
                    setattr(user,key,val)
                else:
                    user.set_password(val)
            #updating profile data
            for key,val in profile_dict.items():
                setattr(profile,key,val)
            user.save()
            profile.save()
            return Response({
                'msg':'Profile updated successfully',
                'data':ProfileSerializer(profile).data
            },status=status.HTTP_200_OK)
               
        except Exception as e:
            return Response({
                'errors':f'Error: {e}',
            },status=status.HTTP_400_BAD_REQUEST)            
            

    
