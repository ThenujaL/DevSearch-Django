
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User #django user models import
from .models import Profile
from django.core.mail import send_mail

# sender -> model that sends it
# instance -> object of the model (row of the tbale) that sent this
# created -> bool isCreated (indicates new entry)


#delete user when profile is deleted
def deleteUser(sender, instance, **kwargs):
    # try block needed as Profile is deleted due to CASCADE on_delete
    # if not this will keep calling itself
    try: 
        user = instance.user
        user.delete()
        print('User deleted!')

    except:
        print('Profile deleted from models.CASCADE')


#save or create profile
def createProfile(sender, instance, created, **kwargs):
    if created:
        newProfile = Profile.objects.create(
            user = instance,
            username = instance.username,
            email = instance.email,
            first_name = instance.first_name,
            last_name = instance.last_name
        )

        # confirmation email
        subject = 'Welcome to Devsearch'
        body = 'This is your confirmation email'
        sender = 'thenuja@thenuja.tech'
        to = instance.email

        send_mail(
            subject,
            body,
            sender,
            [to],
            fail_silently=False,
        )

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