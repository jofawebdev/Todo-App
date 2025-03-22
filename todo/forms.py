from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Task, Profile

class TaskForm(forms.ModelForm):
    """Form for creating and updating tasks."""
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'completed', 'priority']

        # Use HTML5 date input for due_date
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['due_date'].widget = forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        )


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']