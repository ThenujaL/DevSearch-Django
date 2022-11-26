
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User #django user models import
from .models import Profile

# sender -> model that sends it
# instance -> object of the model (row of the tbale) that sent this
# created -> bool isCreated (indicates new entry)


#delete user when profile is deleted
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    print('User deleted!')



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

# updates user info when profile is updated
def updateProfile(sender, instance, created, **kwargs):
    user = instance.user

    if not created:
        user.username = instance.username
        user.first_name = instance.first_name
        user.last_name = instance.last_name
        user.email = instance.email
        user.save()

post_delete.connect(deleteUser, sender=Profile)
post_save.connect(updateProfile, sender=Profile)
post_save.connect(createProfile, sender=User)