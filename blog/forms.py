from django import forms
from .models import Post,Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'title', 'text')

        widgets = {
            'title': forms.TextInput(attrs={'class':'textimputclass'}), #mine
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}), #postcontent is mone another one is for medium editor
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'title': forms.TextInput(attrs={'class':'textimputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }