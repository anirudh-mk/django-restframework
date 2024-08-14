from rest_framework import serializers

from api.models import Books


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    author_country = serializers.CharField(source='author.contry', read_only=True)
    author_age = serializers.CharField(source='author.age', read_only=True)

    class Meta:
        model = Books
        fields =[
            "id",
            "name",
            "published_year",
            "pages",
            "price",
            'author',
            "author_name",
            "author_country",
            "author_age"
        ]
