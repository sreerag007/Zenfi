from django.shortcuts import render
from rest_framework import generics,status
from .serializers import *
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import FormParser,MultiPartParser
from .utils import generate_room_code
from django.db.models import Q
# Create your views here.

class ShareFileCreateView(generics.CreateAPIView):
    serializer_class=ShareCreateSerializer
    permission_classes=[IsAuthenticated]
    parser_classes=[MultiPartParser,FormParser]

    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'error':False,
            'message':'Attachment Shared Successfully!',
            'data':serializer.data
        },status=status.HTTP_200_OK)

class ShareFileListView(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=ShareFileSerializer

    def get_queryset(self):
        return Share.objects.filter(room__participants=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        page=self.paginate_queryset(queryset)

        if page is not None:
            serialzier=self.get_serializer(page,many=True)
            return self.get_paginated_response({
                'error':False,
                'message':'Shared Chats Listed',
                'data':serialzier.data
            })
        serialzier=self.get_serializer(queryset,many=True)
        return Response({
            'error':False,
            'message':'Shared Chats Listed',
            'data':serialzier.data
        })         

class RoomJoinView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=RoomJoinSerializer

    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code=serializer.validated_data['room_code']

        try:
            room = Room.objects.get(room_code=code)
        except Room.DoesNotExist:
            return Response({
                'error':True,
                'message':"Room Details Not Found!",
            },status=status.HTTP_404_NOT_FOUND)

        room.participants.add(request.user)

        return Response({
            'error':False,
            'message':'Room Found!',
            'data':{
                'room_code':room.room_code,
                'created_at':room.created_at
            }
        },status=status.HTTP_200_OK)


class RoomCreateView(generics.CreateAPIView):
    serializer_class=RoomSerializer
    permission_classes=[IsAuthenticated]       

    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(room_code=generate_room_code(),created_by=request.user)

        return Response({
            'error':False,
            'message':"Room Code Generated!",
            'data':serializer.data
        },status=status.HTTP_200_OK)     

class RoomListView(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=RoomSerializer

    def get_queryset(self):
        return Room.objects.filter(Q(participants=self.request.user) | Q(created_by=self.request.user))

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        page=self.paginate_queryset(queryset)

        if page is not None:
            serialzier=self.get_serializer(page,many=True)
            return self.get_paginated_response({
                'error':False,
                'message':'Room Listed',
                'data':serialzier.data
            })
        serialzier=self.get_serializer(queryset,many=True)
        return Response({
            'error':False,
            'message':'Room Listed',
            'data':serialzier.data
        },status=status.HTTP_200_OK)

# class RoomJoinView(generics.GenericAPIView):
#     permission_classes=[AllowAny]
#     serializer_class=RoomJoinSerializer

#     def post(self,request):
#         serializer=self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         code=serializer.validated_data['room_code']

#         try:
#             room = Room.objects.get(room_code=code)
#         except Room.DoesNotExist:
#             return Response({
#                 'error':True,
#                 'message':"Room Details Not Found!",
#             },status=status.HTTP_404_NOT_FOUND)

#         return Response({
#             'error':False,
#             'message':'Room Found!',
#             'data':{
#                 'room_code':room.room_code,
#                 'created_at':room.created_at
#             }
#         },status=status.HTTP_200_OK)
