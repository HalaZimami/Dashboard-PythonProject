from django import forms
from .models import *

class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ['photo']
		labels = {'photo':''}

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('title', 'file')
