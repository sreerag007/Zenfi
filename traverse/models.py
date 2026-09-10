from django.db import models
from accounts.models import User

# Create your models here.

class Room(models.Model):
    room_code=models.CharField(max_length=8,unique=True)
    participants=models.ManyToManyField(User,related_name='rooms')
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='created_rooms')
    updated_at=models.DateTimeField(auto_now=True)    

class Share(models.Model):
    room=models.ForeignKey(to=Room,on_delete=models.CASCADE,related_name='shares')
    sender=models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='shares')
    text_msg=models.TextField(max_length=25000,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
       return f"{self.id}-{(self.text_msg or '')[:30]}"
    
class ShareFile(models.Model):
    share=models.ForeignKey(to=Share,on_delete=models.CASCADE,related_name='files')
    file=models.FileField(upload_to='pictures',null=True,blank=True)

    def __str__(self):
        return f"#{self.id} file for Share {self.share_id}"
