from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from . import forms, models


from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from . import forms, models
from accounts.models import UserLibraryAccount
from decimal import Decimal

from transactions.models import Transaction
from transactions.constants import BORROWED, RETURN

from django.contrib.auth.decorators import login_required

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def borrowed_mail(user, amount, subject, template, current_balance):
    # mail_subject = 'Deposit Message'
    message = render_to_string(template, {
        'user': user,
        'amount': amount,
        'current_balance': current_balance,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()

@login_required
def book_detail(request, book_id):
    # book = get_object_or_404(models.Book, id=book_id)
    book = models.Book.objects.get(id=book_id)
    user = request.user
    user_account = UserLibraryAccount.objects.filter(user=user).first()
    borrowers_list = []
    return_list = []

    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.book = book
            new_comment.user = user
            new_comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('book_detail', book_id=book.id)

        # if user.is_authenticated:
        #     # Check if the user has a library account
        #     user_account = UserLibraryAccount.objects.filter(user=user).first()

        #     if not user_account:
        #         messages.error(
        #             request, 'You need a library account to borrow books. Please create an account.')
        #         return redirect('book_detail', book_id=book.id)

        #     # Check if the user has enough balance to borrow the book
        #     if user_account.balance < book.price:
        #         messages.error(
        #             request, 'You do not have enough balance to borrow this book.')
        #         return redirect('book_detail', book_id=book.id)

        #     # Update the user's balance and add the book to the borrower list
        #     # user_account.balance -= book.price
        #     user_account.balance -= Decimal(str(book.price))

        #     user_account.save()

        #     Transaction.objects.create(
        #         account=user_account,
        #         amount=book.price,
        #         balance_after_transaction=user_account.balance,
        #         transaction_type=BORROWED
        #     )

        #     # Assuming you have a 'borrowers' field in your Book model
        #     book.borrowers.add(user)

        #     messages.success(request, 'Book borrowed successfully!')
        #     return redirect('book_detail', book_id=book.id)
        # else:
        #     messages.error(
        #         request, 'You need to be logged in to borrow books.')
        #     return redirect('login')

        # Check if the user has enough balance to borrow the book
        if 'borrow' in request.POST:
            if user_account.balance < book.price:
                messages.error(
                    request, 'You do not have enough balance to borrow this book.')
                return redirect('book_detail', book_id=book.id)
            user_account.balance -= Decimal(str(book.price))
            user_account.save()

            Transaction.objects.create(
                account=user_account,
                amount=book.price,
                balance_after_transaction=user_account.balance,
                transaction_type=BORROWED
            )

            borrowed_mail(user, book.price, 'Borrow Message','email_templates/borrowed_email.html', user_account.balance)

            # Assuming you have a 'borrowers' field in your Book model
            book.borrowers.add(user)
            borrowers_list.append(book)
            print(borrowers_list)
            messages.success(request, 'Book borrowed successfully!')

        elif 'return' in request.POST:
            # Add the book price back to the user's balance
            user_account.balance += Decimal(str(book.price))
            user_account.save()
            Transaction.objects.create(
                account=user_account,
                amount=book.price,
                balance_after_transaction=user_account.balance,
                transaction_type=RETURN
            )
            # Remove the book from the borrower list
            book.borrowers.remove(user)
            return_list.append(user)
            messages.success(request, 'Book returned successfully!')

        return redirect('book_detail', book_id=book.id)

    comments = models.Comment.objects.filter(book=book)
    comment_form = forms.CommentForm(initial={'user': user})

    return render(request, 'book_detail.html', {'book': book, 'comments': comments, 'comment_form': comment_form})


# def book_detail(request, book_id):
#     book = get_object_or_404(models.Book, id=book_id)

#     user = request.user
#     print(
#         f"User Details - Username: {user.username}, Email: {user.email}, Full Name: {user.get_full_name()}")


#     if request.method == 'POST':
#         form = forms.CommentForm(request.POST)
#         if form.is_valid():
#             new_comment = form.save(commit=False)
#             new_comment.book = book
#             new_comment.save()
#             messages.success(request, 'Comment added successfully!')
#             return redirect('book_detail', book_id=book.id)

#     comments = models.Comment.objects.filter(book=book)
#     # comment_form = forms.CommentForm()
#     comment_form = forms.CommentForm(initial={'user': request.user})


#     return render(request, 'book_detail.html', {'book': book, 'comments': comments, 'comment_form': comment_form})
