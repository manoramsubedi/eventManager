from django import forms
from django.core.validators import MinLengthValidator
from datetime import date

class EventForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    participants = forms.IntegerField(validators=[MinLengthValidator(1)])
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)

    #Date Validation
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

    if start_date and end_date:
        if start_date > end_date:
            raise forms.ValidationError("End date should be greater than start date.")
    


