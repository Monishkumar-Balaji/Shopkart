from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User
from django import forms 

class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter User Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter email'}))
    password1 = forms.Field(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter new Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
    class Meta:
        User = get_user_model()
        model=User
        fields=['username','email','password1','password2']        

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['password1'].widget.attrs.update({'class':'form-control'})
            self.fields['password2'].widget.attrs.update({'class':'form-control'})