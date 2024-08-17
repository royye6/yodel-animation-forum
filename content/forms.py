from django import forms
from django.forms import FileInput
from .models import Topic, Reply


class StaffTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content', 'file', 'is_pinned']

        widgets = {
            'image': FileInput(attrs={"onchange": "loadFile(event)", "class": "upload"})
        }


class UserTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content', 'file']

        widgets = {
            'file': FileInput(attrs={"onchange": "loadFile(event)", "class": "upload"})
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content', 'reply_file']

        widgets = {
            'reply_file': FileInput(attrs={"onchange": "loadFile(event)", "class": "upload"})
        }