from django import forms
from django.contrib.auth.models import User
from .models import Post,Comment


class PostAdd(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['author','title','body','image','draft','created_date','published_date','status']


class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('author','text')

        widgets = {
        'author':forms.TextInput(attrs={'class':'textinputclass'}),
        'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }
