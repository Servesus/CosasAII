# -*- encoding: utf-8 -*-
from django import forms

class UserForm(forms.Form):
    id = forms.CharField(label='User ID')
    
class GameForm(forms.Form):
    id = forms.CharField(label='Game name')

class TagForm(forms.Form):
    id = forms.CharField(label='Tag name')