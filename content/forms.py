from django import forms
from .models import Topic


class StaffTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content', 'image', 'is_pinned']


class UserTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content', 'image']