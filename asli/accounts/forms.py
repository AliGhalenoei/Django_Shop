from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    password=forms.CharField()
    password2=forms.CharField()

    class Meta:
        model=User
        fields=(
            'phone',
            'email',
            'phone',
        )
    
    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password'] and cd['password2'] and cd['password2'] != cd['password']:
            raise ValidationError('Passwords is not Mach')
        return cd['password2']
    
    def save(self, commit=True) -> Any:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField()

    class Meta:
        model=User
        fields=(
            'phone',
            'email',
            'username',
            'password'
        )

# Authenticated Forms...

class Veryfy_Singup_Form(forms.Form):
    code=forms.IntegerField()

