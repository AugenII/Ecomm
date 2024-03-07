from django import forms
from .models import CustomUser, Consumer

class CustomUserInputForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {'password': forms.PasswordInput(render_value=True)}


class ConsumerForm(forms.ModelForm):
    class Meta:
        model = Consumer
        fields = ['consumer_admin','phone_no']
