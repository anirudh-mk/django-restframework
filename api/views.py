from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Books
from api.serializer import BookSerializer


# Create your views here.


class PrintHello(APIView):
    def get(self, request, name):
        return Response(
            data={"success response": name},
            status=status.HTTP_200_OK
        )


class Login(APIView):
    def get(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None:
            return Response(
                data={
                    "error": "Please enter your username"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if password is None:
            return Response(
                data={
                    "error": "Please enter your password"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if username == 'anirudh' and password == '1234':
            return Response(
                data={
                    "success": "user logined successfully",
                },
                status=status.HTTP_200_OK
            )

        return Response(
            data={
                "error": "invalid username or password"
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class BooksAPI(APIView):
    def get(self, request, id=None):
        if id:
            books_queryset = Books.objects.filter(id=id).first()
            return Response(
                data={
                    "name": books_queryset.name,
                    "published_year": books_queryset.published_year,
                    "pages": books_queryset.pages,
                    "author": books_queryset.author,
                    "price": books_queryset.price
                },
                status=status.HTTP_200_OK
            )

        books = Books.objects.all().values()

        return Response(
            data=books,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        name = request.data.get('name')
        published_year = request.data.get('year')
        pages = request.data.get('pages')
        author = request.data.get('author')
        price = request.data.get('price')

        if name is None:
            return Response(
                data="name is required",
                status=status.HTTP_200_OK
            )

        books = Books(
            name=name,
            published_year=published_year,
            pages=pages,
            author=author,
            price=price
        )
        books.save()

        return Response(
            data="book created succssfully",
            status=status.HTTP_200_OK
        )


class BookAPI(APIView):
    def get(self, request, id=None):
        if id:
            book_queryset = Books.objects.filter(id=id).first()
            serializer = BookSerializer(book_queryset, many=False)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

        book_queryset = Books.objects.all()
        serializer = BookSerializer(book_queryset, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, requset):

        serializer = BookSerializer(data=requset.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                data='book created successfully',
                status=status.HTTP_200_OK
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_200_OK
        )

