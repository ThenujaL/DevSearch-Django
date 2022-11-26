from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile



#inherits rom UserCreationForm - has all the attributes as that
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',  'email', 'password1', 'password2']

        #these are the fields that the user can modify
        labels = {'username': 'Username', 'first_name': 'First Name', 'last_name':'Last Name', 'email': 'Email'}

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'email', 'city', 'country', 'short_intro',
                  'bio', 'profile_image', 'social_github', 'social_twitter', 'social_linkedin', 
                   'social_youtube', 'social_website']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})