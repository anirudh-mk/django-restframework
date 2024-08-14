from django.urls import path

from api import views

urlpatterns = [
    path('hello/<str:name>/', views.PrintHello.as_view()),
    path('login/', views.Login.as_view()),
    path('books/', views.BooksAPI.as_view()),
    path('books/<str:id>/', views.BooksAPI.as_view()),
    path('book-serializer/', views.BookAPI.as_view()),
    path('book-serializer/<str:id>/', views.BookAPI.as_view())
]