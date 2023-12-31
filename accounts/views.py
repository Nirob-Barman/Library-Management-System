from django.shortcuts import render, redirect
from django.views.generic import FormView
from . forms import UserRegistrationForm, UserUpdateForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from books.models import Book

from transactions.models import Transaction
from transactions.constants import BORROWED, RETURN
# Create your views here.


def send_password_change_mail(user, subject, template):
    # mail_subject = 'Deposit Message'
    message = render_to_string(template, {
        'user': user,
    })
    # to_email = to_user
    # send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()

class RegistrationView(FormView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/registration.html'

    def form_valid(self, form):
        user = form.save()
        print(user)
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class LoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        # return reverse_lazy('accounts:profile')
        return reverse_lazy('profile')
        # return reverse_lazy('home')


# class LogoutView(LogoutView):
#     def get_success_url(self):
#         # if self.request.user.is_authenticated:
#         #     logout(self.request)
#         return reverse_lazy('home')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class UserProfileUpdateView(LoginRequiredMixin,View):
    template_name = 'accounts/update_profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        # return render(request, 'accounts/profile.html', {'form': form})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your profile has been updated successfully!')
            return redirect('home')
        else:
            print(form.errors)
            # return render(request, 'accounts/profile.html', {'form': form})
        # return render(request, 'accounts/profile.html', {'form': form})
        return render(request, self.template_name, {'form': form})


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'
    
    def get(self, request, *args, **kwargs):
        borrowed_books = Book.objects.filter(borrowers=request.user)

        all_transactions = Transaction.objects.filter(account=request.user.account).order_by('-timestamp')
        # for transaction in all_transactions:
        #     print(transaction.transaction_type, transaction.amount, transaction.balance_after_transaction)

        # Create a list to store book details along with their borrowing history
        books_with_history = []

        for book in borrowed_books:
            # Get the borrowing history for each book
            history = Transaction.objects.filter(
                account=request.user.account,
                transaction_type=BORROWED,
                amount=book.price,
            ).order_by('-timestamp')

            # Add book and its history to the list
            books_with_history.append({'book': book, 'history': history})

            # Extract transaction details for each book
            transactions_for_book = [{'amount': transaction.amount, 'balance_after_transaction': transaction.balance_after_transaction}
                             for transaction in history]
        context = {
            'user': request.user,
            # 'borrowed_books': borrowed_books,
            'books_with_history': books_with_history,
            # 'all_transactions': all_transactions
        }

        # for book in borrowed_books:
        #     print(book.price)
        # print(borrowers)
        return render(request, self.template_name, context=context)


def password_change(request):
    if request.user.is_authenticated:
        form = PasswordChangeForm(request.user)
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(
                    request, 'Your password was successfully updated!')
                
                # send_password_change_mail(
                #     request.user, 
                #     'Password Changed',
                #     'accounts/email_templates/transaction_mail.html'
                #     )

                return redirect('profile')
            else:
                messages.error(request, 'Please correct the error below.')
        return render(request, 'accounts/form.html', {'form': form, 'title': 'Change Your Password', 'button_text': 'Change Password', 'button_class': 'btn-warning'})
    else:
        return redirect('home')
        # return redirect('profile')
