from django import forms
from django.core.validators import MinValueValidator
from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime

class EventForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    participants = forms.IntegerField(validators=[MinValueValidator(1)])
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)

    # Date Validation
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError("Start date cannot be after end date.")

        return cleaned_data
    
# class EventForm(forms.Form):
#     title = forms.CharField(max_length=100)
#     description = forms.CharField(widget=forms.Textarea)
#     participants = forms.IntegerField(validators=[MinLengthValidator(1)])
#     start_date = forms.DateField(widget=forms.SelectDateWidget)
#     end_date = forms.DateField(widget=forms.SelectDateWidget)

#     #Date Validation
#     def clean(self):
#         cleaned_data = super().clean()
#         start_date = cleaned_data.get("start_date")
#         end_date = cleaned_data.get("end_date")

#     if start_date and end_date:
#             if start_date > end_date:
#                 raise ValidationError("End date should be greater than start date.")
   
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    


