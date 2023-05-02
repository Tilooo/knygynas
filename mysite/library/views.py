from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Book, BookInstance, Author


# Create your views here.
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_authors = Author.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_authors': num_authors,
        'num_instances_available': num_instances_available,
    }
    return render(request, 'index.html', context=context)


def authors(request):
    authors = Author.objects.all()
    context = {
        'authors': authors,
    }
    return render(request, 'authors.html', context=context)

def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    context = {
        'author': author,
    }
    return render(request, 'author.html', context=context)
