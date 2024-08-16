from django import forms
from django.forms import FileInput
from .models import Topic


class StaffTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content', 'file', 'is_pinned']


class UserTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content', 'file']

        widgets = {
            'image': FileInput(attrs={"onchange": "loadFile(event)", "class": "upload"})
        }