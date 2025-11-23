from django import forms
from .models import Plant, Comment

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'description', 'category', 'is_edible', 'image', 'native_to', 'used_for']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'content': forms.Textarea(attrs={'placeholder': 'Your Comment'}),
        }