from django import forms
from .models import *

class FeedBackConsumerForm(forms.Form):
    content=forms.CharField(widget=forms.Textarea(attrs={'rows':'2','cols':'5'}))

