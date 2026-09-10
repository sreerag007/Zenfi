import random,string
from .models import Room

def generate_room_code(length=6):
    chars=string.ascii_uppercase + string.digits
    while True:
        code=''.join(random.choices(chars,k=length))
        if not Room.objects.filter(room_code=code).exists():
            return code