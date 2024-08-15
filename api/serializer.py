from rest_framework import serializers

from api.models import Books


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    author_country = serializers.CharField(source='author.contry', read_only=True)
    author_age = serializers.CharField(source='author.age', read_only=True)
    author_books = serializers.SerializerMethodField()

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
            "author_age",
            "author_books"
        ]

    def get_author_books(self, obj):
        author = obj.author
        books_values = Books.objects.filter(author=author).values_list('name', flat=True)

        return books_values

    def validate_name(self, name):
        if Books.objects.filter(name=name).exists():
            raise serializers.ValidationError('book already exists')
        return name