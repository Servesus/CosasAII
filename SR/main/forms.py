# -*- encoding: utf-8 -*-
from django import forms

class UserForm(forms.Form):
    id = forms.CharField(label='User ID')
    
class BookForm(forms.Form):
    id = forms.CharField(label='Book ID')