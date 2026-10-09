from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiTypes
from .utils import get_user_tokens
from rest_framework.parsers import FormParser,MultiPartParser
from rest_framework import generics
# Create your views here.

class GoogleAuthView(APIView):
    permission_classes=[AllowAny]
    serializer_class=GoogleSignUpSerializer

    def post(self,request):
        serializer=GoogleSignUpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'error':True,
                'message':serializer.errors
            },status=status.HTTP_400_BAD_REQUEST)

        google_user=serializer.validated_data['google_user']
        email=google_user.get('email')
        google_id=google_user.get('sub')

        user, created=User.objects.get_or_create(
            email=email,defaults={
            'full_name': google_user.get('name'),
            'google_id': google_id,
            }
        )
        if created:
            user.set_unusable_password()
            user.save()
        
        if not user.google_id:
            user.google_id=google_id
            user.save()

        tokens=get_user_tokens(user)['token']

        return Response({
            'error':False,
            'message':'Login Successful',
            'data':{
                'tokens':tokens,
                'is_profile_complete':user.is_profile_complete,
                'full_name':user.full_name,
                'email':email
            }
        },status=status.HTTP_200_OK)

class ProfileCompleteView(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class=ProfileCompleteSerializer
    parser_classes=[MultiPartParser,FormParser]

    def post(self,request):
        serializer=ProfileCompleteSerializer(request.user,data=request.data,partial=True)

        if serializer.is_valid():
            user=serializer.save()
            user.is_profile_complete=True
            user.save()

            return Response({
                'error':False,
                'message':'Profile Completed!',
                'data':{
                    'full_name':user.full_name,
                    'email':user.email,
                    'profile_picture':user.profile_picture,
                }
            },status=status.HTTP_200_OK)

        return Response({
            'error':True,
            'message':serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)

class ProfileUpdateView(APIView):
    permission_classes=[IsAuthenticated]
    parser_classes=[MultiPartParser, FormParser]

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'full_name': {'type': 'string'},
                    'profile_picture': {'type': 'string', 'format': 'binary'},
                }
            }
        },
        responses=ProfileUpdateSerializer
    )
    def patch(self, request):
        user = request.user

        full_name = request.data.get('full_name')
        if full_name:
            user.full_name = full_name

        image = request.data.get('profile_picture')
        if image:
            user.profile_picture = image

        user.save()

        return Response({
            'error': False,
            'message': "Profile Updated!",
            'data': ProfileUpdateSerializer(user,context={'request': request}).data
        }, status=status.HTTP_200_OK)

class CheckUserSessionView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user=request.user

        return Response({
            'error':False,
            'message':'Your Session',
            'data':{
                'name':user.full_name,
                'email':user.email,
                'is_active':user.is_active,
                'profile_picture':user.profile_picture if user.profile_picture else None,
            }
        },status=status.HTTP_200_OK)   

class UserDropDownView(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=UserDropdownSerializer

    def get_queryset(self):
        return User.objects.all().exclude(pk=self.request.user.pk)

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        serializer=self.get_serializer(queryset,many=True)

        return Response({
            'error':False,
            'message':'User Listed',
            'data':serializer.data
        },status=status.HTTP_200_OK)