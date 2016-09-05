#serialize models. @Ganben 5.9.2016

from rest_framework import serializers
from .models import Question


class QuestionSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    question_text = serializers.CharField(required=True, allow_blank=False, max_length=200)

