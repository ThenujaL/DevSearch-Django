
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User #django user models import
from .models import Profile




#delete user when profile is deleted
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    print('User deleted!')

post_delete.connect(deleteUser, sender=Profile)

#save or create profile
def createProfile(sender, instance, created, **kwargs):
    if created:
        newProfile = Profile.objects.create(
            user = instance,
            username = instance.username,
            email = instance.email
        )
        print("New User Created!")

    #profile update through users



post_save.connect(createProfile, sender=User)