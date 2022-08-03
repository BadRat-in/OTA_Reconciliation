from django import forms


#Data Class for the file form to verify the from data
class UploadFileForm(forms.Form):
    file1 = forms.FileField()
    file2 = forms.FileField()
    file3 = forms.FileField()
    file4 = forms.FileField()
    ota1 = forms.CharField(max_length=20)
    ota2 = forms.CharField(max_length=20)
    ota3 = forms.CharField(max_length=20)
