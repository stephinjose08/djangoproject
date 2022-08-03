from cProfile import label
from pyexpat import model
from tokenize import Number
from django import forms
from .models import code

class codeVarification(forms.ModelForm):
    #OTPcode=forms.CharField(max_length=5, label='code',help_text="Enter the 5 digit SMS varification code")
    
    class Meta:
        model=code
        fields=('Otp',)
