# -*- encoding: utf-8 -*-
from django import forms

class GameForm(forms.Form):
    name = forms.CharField(label='Juego')
    