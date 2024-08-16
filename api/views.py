import math

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Books
from api.serializer import BookSerializer, UserCreateSerilizer, BookCreateSerializer

from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import authenticate


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

        page_no = request.GET.get('page')

        if id:
            book_queryset = Books.objects.filter(id=id).first()
            serializer = BookSerializer(book_queryset, many=False)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

        book_queryset = Books.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 2
        page = paginator.paginate_queryset(book_queryset, request)
        total_pages = math.ceil(book_queryset.count() / 2)
        serializer = BookSerializer(page, many=True)
        return Response(
            data={
                'response': serializer.data,
                'current_page': page_no,
                'total_response': book_queryset.count(),
                'total_pages': total_pages
            },
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

    def patch(self, request, id):

        books_queryset = Books.objects.filter(id=id).first()

        if books_queryset is None:
            return Response(
                data='book not found',
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BookSerializer(books_queryset, data=request.data, partial=True)
        if serializer.is_valid():
            response = serializer.save()
            return Response(
                data=f'{response.name} edited successfully',
                status=status.HTTP_200_OK
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, id):
        books_queryset = Books.objects.filter(id=id).first()

        if books_queryset is None:
            return Response(
                data='book not found',
                status=status.HTTP_400_BAD_REQUEST
            )

        books_queryset.delete()

        return Response(
            data=f'book deleted successfully',
            status=status.HTTP_200_OK
        )


class UserCreateAPI(APIView):
    def post(self, request):
        serializer = UserCreateSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "success": "User created successfully"
                },
                status=status.HTTP_200_OK
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserLoginAPI(APIView):
    def get(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username and password:
            return Response(
                data={
                    "error": "please enter username and password"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)
        if user:
            return Response(
                data={
                    "success": "user Logined successfully"
                },
                status=status.HTTP_200_OK
            )
        return Response(
            data={
                "error": "invalid username or password"
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class BookCreateAPI(APIView):
    def post(self, request):
        serializer = BookCreateSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "success": "book created successfully"
                },
                status=status.HTTP_200_OK
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
