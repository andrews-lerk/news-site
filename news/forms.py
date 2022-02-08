from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from .models import *


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        #widgeds = {
         #   'username': forms.TextInput(attrs={'class': 'form-input'}),
          #  'password1': forms.TextInput(attrs={'class': 'form-input'}),
           # 'password2': forms.TextInput(attrs={'class': 'form-input'}),
        #}

class WriteCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

class ChangeUsername(forms.Form):
    change_name = forms.CharField(max_length=191)

class ChangePass(forms.Form):
    new_pass = forms.CharField(widget=forms.PasswordInput())
    new_pass_confirmation=forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(ChangePass, self).clean()
        new_pass = cleaned_data.get("new_pass")
        new_pass_confirmation= cleaned_data.get("new_pass_confirmation")

        if new_pass and new_pass_confirmation:
            # Only do something if both fields are valid so far.
            if new_pass!=new_pass_confirmation:
                raise forms.ValidationError('Passwords do not match!')
            if len(new_pass)<8:
                raise forms.ValidationError('Password is too short!')


        # Always return the full collection of cleaned data.
        return cleaned_data

class UserQuestionForm(forms.ModelForm):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'style':"font-size:12pt;height:35px;width:250px;", 'placeholder':'Your name'}))
    text = forms.CharField(
        widget=forms.Textarea(attrs={'style': "font-size:12pt;height:70px;width:250px;background-color:#2E2E2E;border-color: transparent",
                                     'placeholder': 'Question',}))

    class Meta:
        model = UserQuestion
        fields = ('user_name', 'text')
        widgeds = {
        'user_name': forms.TextInput(attrs={'style':"font-size:18pt;height:420px;width:200px;"}),
        }