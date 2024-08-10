from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Books


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
            print(books_queryset)
            return Response(
                data=books_queryset,
                status=status.HTTP_200_OK
            )

        books = Books.objects.all().values()

        return Response(
            data=books,
            status=status.HTTP_200_OK
        )