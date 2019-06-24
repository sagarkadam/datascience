from django.db import models
from django.urls import reverse

class DatasetProfile(models.Model):
    problem_name = models.CharField(max_length=40)
    max_algorithm = models.CharField(max_length=40)
    model_accuracy = models.CharField(max_length=40)
    file_type = models.CharField(max_length=40)
    dataset_size = models.CharField(max_length=40)
    document_link = models.CharField(max_length=1000)
    application_link = models.CharField(max_length=1000)
    github_link = models.CharField(max_length=1000)
    aws_jupyter_link = models.CharField(max_length=1000)
    user_jupyter_link = models.CharField(max_length=1000)
    dataset_zip = models.CharField(max_length=1000)
    dataset_valid=models.CharField(max_length=40)
    user_id = models.IntegerField()
    # created_time=models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('modelforms:thanks')

    class Meta:
        managed = False
        db_table = 'dataset_profile'


class DataScienceFaq(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)
    question_category= models.CharField(max_length=1000)
    question_url = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'datascience_faq'
