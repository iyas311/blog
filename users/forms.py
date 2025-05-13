from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
# users/forms.py
class CustomUserCreationForm(UserCreationForm):
    profile_pic = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'}))
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_pic', 'contact_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].widget.attrs.update({'class': 'form-control'})
# users/forms.py
# users/forms.py
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 
                 'profile_pic', 'contact_number')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True