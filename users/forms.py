from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



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