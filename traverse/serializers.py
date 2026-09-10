from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from.models import *

class ShareFileSerializer(serializers.ModelSerializer):
    class Meta:
        model=ShareFile
        fields=[
            'id','file'
        ]
        read_only_fields=[
            'id'
        ]

class ShareSerializer(serializers.ModelSerializer):
    room_details=serializers.SerializerMethodField()
    class Meta:
        model=Share
        fields=['id','room_details','text_msg','created_at','updated_at']  

    @extend_schema_field(serializers.DictField())
    def get_room_details(self,obj):
        if obj.room:
            return {
                'room_id':obj.room.id,
                'room_name':obj.room.room_code
            }  

class ShareCreateSerializer(serializers.ModelSerializer):
    room_code=serializers.CharField(write_only=True)
    files=serializers.ListField(child=serializers.FileField(),write_only=True,required=False)
    attachments=ShareFileSerializer(many=True,read_only=True,source='files')

    class Meta:
        model=Share
        fields = ['id', 'room_code', 'text_msg', 'files', 'attachments', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self,validated_data):
        room_code=validated_data.pop('room_code')  
        uploaded_files=validated_data.pop('files',[])
        sender=self.context['request'].user

        # room,_=Room.objects.get_or_create(room_code=room_code)
        # share=Share.objects.create(room=room,**validated_data)
        try:
            room=Room.objects.get(room_code=room_code, participants=sender)
        except Room.DoesNotExist:
            raise serializers.ValidationError("Room not found or you're not a participant")

        share=Share.objects.create(room=room,sender=sender,**validated_data)

        for f in uploaded_files:
            ShareFile.objects.create(share=share,file=f)

        return share          

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=Room
        fields=['id','room_code','participants','created_by','created_at']
        read_only_fields=['room_code','created_at','participants','created_by']

class RoomJoinSerializer(serializers.Serializer):
    room_code=serializers.CharField(max_length=8)         