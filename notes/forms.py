from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Note

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Last Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
'email', 'password1', 'password2',)


class NoteForm(forms.ModelForm):
    title = forms.CharField(max_length = 120, required=False)
    content = forms.CharField(widget=forms.Textarea, required=True)
    pinned = forms.BooleanField(required = False, label="Pin to top")

    class Meta:
        model = Note
        fields = ('title', 'content', 'pinned', )

