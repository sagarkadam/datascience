from rest_framework import serializers
from .models import DatasetProfile


class DatasetProfileSerializer(serializers.Serializer):

    problem_name = serializers.CharField(max_length=40)
    max_algorithm = serializers.CharField(max_length=40)
    model_accuracy = serializers.CharField(max_length=40)
    file_type = serializers.CharField(max_length=40)
    dataset_size = serializers.CharField(max_length=40)
    document_link = serializers.CharField(max_length=1000)
    application_link = serializers.CharField(max_length=1000)
    github_link = serializers.CharField(max_length=1000)
    aws_jupyter_link = serializers.CharField(max_length=1000)
    dataset_zip = serializers.CharField(max_length=1000)


class dataset_review_serializer(serializers.Serializer):
    id=serializers.IntegerField(default=None,allow_null=True)