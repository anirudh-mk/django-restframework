from rest_framework import serializers

from api.models import Books, Author
from django.contrib.auth.models import User

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


class UserCreateSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class BookCreateSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField()
    contry = serializers.CharField()
    age = serializers.CharField()

    class Meta:
        model = Books
        fields = [
            'name',
            'published_year',
            'pages',
            'price',
            'author_name',
            'contry',
            'age'
        ]

    def create(self, validated_data):
        print(self.initial_data)
        author = Author.objects.create(
            name=self.initial_data.get('author_name'),
            contry=self.initial_data.get('contry'),
            age=self.initial_data.get('age')
        )
        validated_data.pop('author_name')
        validated_data.pop('contry')
        validated_data.pop('age')

        validated_data['author'] = author
        return Books.objects.create(**validated_data)