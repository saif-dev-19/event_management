from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Permission,Group
from event.forms import StyledFormMixin
from django import forms
from django.contrib.auth.forms import AuthenticationForm
import re


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User

        fields = ['username','first_name','last_name','password1','password2','email']
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm,self).__init__(*args, **kwargs)

        for fieldname in ['username','password1','password2']:
            self.fields[fieldname].help_text = None
    

class CustomRegistrationForm(StyledFormMixin,forms.ModelForm):
    password1 =forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','confirm_password','email']

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        errors = []

        if len(password1) < 8:
            errors.append("Password must be 8 characters")
            
        if not re.search(r'[A-Z]',password1):
            errors.append("Password must include Upercase Character")

        if not re.search(r'[a-z]',password1):
            errors.append("Password must include lowecase Character")
        
        if not re.search(r'[0-9]',password1):
            errors.append("Password must include Atleast One number")
        
        if not re.search(r'[@#$%^&+=]',password1):
            errors.append("Password must include one special Character")
        
        if errors:
            raise forms.ValidationError(errors)
    
        return password1

    #field-error clean er pore field name ache
    def clean_email(self):
        email = self.cleaned_data.get('email')
        print(email)

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        
        return email
    

    #none-field error
    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')

        if password1 != confirm_password:
            raise forms.ValidationError("Password Do not match")

        return cleaned_data
    
    
class LoginForm(StyledFormMixin,AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class AssignRoleForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role",

    )

class CreateGroupForm(StyledFormMixin,forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required = False,
        label = "Assign Permission"
    )

    class Meta:
        model = Group
        fields = ['name','permissions']