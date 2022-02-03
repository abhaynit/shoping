from testapp.models import addressed,addimg
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm


# THESE ARE THE PREDEFINED FORMS PROVIDED BY DJANGO
class SignUpForm(UserCreationForm):
    class Meta: 
        model = User
        fields = ['username','email']

class EditUserProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['first_name','last_name','email','date_joined','last_login']
        labels = {'email' : 'Email'}

class address(ModelForm):
    class Meta:
        model = addressed
        fields = ['city','state','zip_code','street','mobile']


class addim(ModelForm):
    class Meta:
        model = addimg
        fields = ['im']


##################################################################################
"""
class EditAdminProfile(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = '__all__'
        labels = {'email':'Email'}
"""






