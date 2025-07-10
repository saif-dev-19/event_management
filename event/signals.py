from django.db.models.signals import post_save
from django.dispatch import receiver
from event.models import Event



@receiver(post_save,sender=Event)
def notify_rpsv(sender,instance,**kwargs):
    print('sender',sender)
    print('instance',instance)
    print(kwargs)