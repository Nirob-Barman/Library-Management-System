"""
URL configuration for Library_Management_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', HomeView.as_view(), name='home'),
    # path('books_filter/<slug:book_category>', HomeView.as_view(), name='books_filter'),
    path('', home_view, name='home'),
    path('books_filter/<slug:book_category>', home_view, name='books_filter'),

    # path('books_filter/<path:book_category>/', home_view, name='books_filter'),
    path('accounts/', include('accounts.urls')),
    path('books/', include('books.urls')),
    path('transactions/', include('transactions.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
