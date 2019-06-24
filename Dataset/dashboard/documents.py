from django_elasticsearch_dsl import DocType,Index
from elasticsearch_dsl import connections

from .models import DatasetProfile

posts=Index('posts')
connections.create_connection()


@posts.doc_type
class PostDocument(DocType):
    class Meta:
        model=DatasetProfile

        fields = [
            'problem_name',
            'max_algorithm',
            'model_accuracy',
        ]