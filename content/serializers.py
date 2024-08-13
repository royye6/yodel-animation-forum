from rest_framework import serializers
from .models import Topic, Reply


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['user', 'title', 'created_at', 'is_pinned']