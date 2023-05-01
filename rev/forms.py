from django import forms

class UploadForm(forms.Form):
    file = forms.FileField(label='CSV file')
    file2 = forms.FileField(label='CSV file2')