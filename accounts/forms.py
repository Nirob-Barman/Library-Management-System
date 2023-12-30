from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . constants import GENDER_TYPE
from django import forms
from .models import UserLibraryAccount, UserAddress


class UserRegistrationForm(UserCreationForm):
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    street_address = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2',
                   'gender', 'birthdate', 'street_address', 'city', 'postal_code', 'country']

    def save(self, commit=True):
        our_user = super().save(commit=False)

        if commit == True:
            our_user.save()
            birthdate = self.cleaned_data['birthdate']
            gender = self.cleaned_data['gender']

            street_address = self.cleaned_data['street_address']
            city = self.cleaned_data['city']
            postal_code = self.cleaned_data['postal_code']
            country = self.cleaned_data['country']

            UserAddress.objects.create(
                user=our_user,
                street_address=street_address,
                city=city,
                postal_code=postal_code,
                country=country
            )
            UserLibraryAccount.objects.create(
                user=our_user,
                account_number=10000+our_user.id,
                birthdate=birthdate,
                gender=gender,
                # initial_deposit_date=user.date_joined,
                # balance=0
            )
            # return user
        return our_user

    def __init__(self, *args, **kwargs):
        # super.__init__(*args, **kwargs)
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })


class UserUpdateForm(forms.ModelForm):
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)

    street_address = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=50)

    class Meta:
        model = User
        # fields = ['username', 'first_name', 'last_name', 'email']
        # prohibited to update username
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        # super.__init__(*args, **kwargs)
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })

        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
            except UserLibraryAccount.DoesNotExist:
                user_account = None
                user_address = None

            if user_account:
                self.fields['birthdate'].initial = user_account.birthdate
                self.fields['gender'].initial = user_account.gender

            if user_address:
                self.fields['street_address'].initial = user_address.street_address
                self.fields['city'].initial = user_address.city
                self.fields['postal_code'].initial = user_address.postal_code
                self.fields['country'].initial = user_address.country

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit == True:
            user.save()
            user_account, created = UserLibraryAccount.objects.get_or_create(
                user=user
            )
            user_address, created = UserAddress.objects.get_or_create(
                user=user
            )
            user_account.birthdate = self.cleaned_data['birthdate']
            user_account.gender = self.cleaned_data['gender']
            user_account.save()

            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.country = self.cleaned_data['country']

            # return user
        return user
