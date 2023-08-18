from django import forms
from .models import *

class Call_Me_Form(forms.Form):
    name=forms.CharField()
    subject=forms.CharField()
    massage=forms.CharField(widget=forms.Textarea)
    email=forms.EmailField()
    phone=forms.CharField(max_length=11 , required=False)

class CartForm(forms.Form):
    tedad=forms.IntegerField(min_value=1,max_value=9)

class CuponForm(forms.Form):
    code=forms.CharField(max_length=50)

class Comment_Product_Form(forms.ModelForm):
    class Meta:
        model=CommentProduct
        fields=('body',)
    
