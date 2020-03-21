from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

User = settings.AUTH_USER_MODEL

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()



class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, blank=True, null=True)
    content = models.TextField(null=True, blank=True)
    pinned = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add = True)
    class Meta:
        ordering = ['-created', 'pinned']

def get_image_filename(instance, filename):
    id_ = instance.note.id
    return "media_root/static/uploads/{}".format(id_)

class Images(models.Model):
    note = models.ForeignKey(Note, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Images')


