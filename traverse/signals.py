from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Share,ShareFile


@receiver(post_save,sender=Share)
def notify_share_created(sender,instance,created,**kwargs):
    if not created:
        return

    channel_layer=get_channel_layer()
    group_name=f"room_{instance.room.room_code}"

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type':'share_message',
            'event':'new_share',
            'share_id':instance.id,
            'text_msg':instance.text_msg,
        }
    )  

@receiver(post_save,sender=ShareFile)
def notify_file_uploaded(sender,instance,created,**kwargs):
    if not created:
        return

    channel_layer=get_channel_layer()
    group_name=f"room_{instance.share.room.room_code}"

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type':'share_message',
            'event':'new_file',
            'share_id':instance.share_id,
            'file_id':instance.id,
            'file_url':instance.file.url,            
        }
    )