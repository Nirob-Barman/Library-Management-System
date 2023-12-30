# from .models import BankSettings
from django.views import View
from django.shortcuts import render
from django.views.generic import TemplateView
from books.models import Book, CATEGORY_CHOICES
from django.template.defaultfilters import slugify
# from books.constants import CATEGORY_CHOICES
# Create your views here.

def home_view(request, book_category=None):
    books = Book.objects.all()
    categories = [category[0] for category in CATEGORY_CHOICES]
    # print(categories)
    bookCategory = book_category
    if book_category:
        books = books.filter(categories=bookCategory)

    return render(request, 'index.html', {'books': books, 'categories': categories})



# class HomeView(TemplateView):
#     template_name = 'index.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['books'] = Book.objects.all()
#         # context['categories'] = CATEGORY_CHOICES
#         # for book in context['books']:
#         #     print(book.categories)
#         # for category in context['categories']:
#         #     print(category[0])
#         context['categories'] = [category[0] for category in CATEGORY_CHOICES]
#         # Assuming you are using URL parameters
#         category = self.kwargs.get('category')
#         # print(context['categories'])
#         return context





# def home_view(request, book_category=None):
#     books = Book.objects.all()
#     categories = [category[0] for category in CATEGORY_CHOICES]
#     print(categories)

#     if category:
#         # Convert the slug back to the original format
#         category = slugify(book_category).replace('-', ' ')
#         books = books.filter(categories=category)

#     return render(request, 'index.html', {'books': books, 'categories': categories, 'category': category})


# def home_view(request, book_category=None):
#     books = Book.objects.all()
#     categories = [category[0] for category in CATEGORY_CHOICES]

#     if book_category:
#         # Convert the slug back to the original format
#         category = slugify(book_category).replace('-', ' ')
#         books = books.filter(categories=category)
#         print(books)
#         for book in books:
#             print(book.title)
#     else:
#         category = None

#     return render(request, 'index.html', {'books': books, 'categories': categories, 'category': category})
