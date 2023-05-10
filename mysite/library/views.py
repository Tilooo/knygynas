from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Book, BookInstance, Author
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.forms import User
from django.views.generic.edit import FormMixin
from .forms import BookReviewForm


# Create your views here.
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_authors = Author.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()
    num_visits = request.session.get('nu_visits', 1)
    request.session['num_visits'] = num_visits +1
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_authors': num_authors,
        'num_instances_available': num_instances_available,
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)


def authors(request):
    paginator = Paginator(Author.objects.all(), 4)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    authors = paged_authors
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


def search(request):
    query = request.GET.get('query')
    search_results = Book.objects.filter(Q(title__icontains=query) | Q(summary__icontains=query) | Q(author__first_name__icontains=query) | Q(author__last_name__icontains=query))
    context = {
        'books': search_results,
        'query': query,
    }
    return render(request, 'search.html', context=context)

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'books.html'
    #paginate_by = 3

class BookDetailView(FormMixin, generic.DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'book.html'
    form_class = BookReviewForm

    def get_success_url(self):
        return reverse('book', kwargs={'pk': self.object.id})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.book = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)


class MyBookInstanceListView(LoginRequiredMixin, generic.ListView,):
    model = BookInstance
    context_object_name = 'my_books'
    template_name = 'my_books.html'

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user)



@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')


