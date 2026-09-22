from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Customer, Restaurant
from captcha.fields import CaptchaField
from phonenumber_field.formfields import PhoneNumberField

class NewCustomerForm(UserCreationForm):
    fullname = forms.CharField(max_length=100)
    mobile = PhoneNumberField()
    Captcha = CaptchaField()
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self):
        user = super().save(commit=True)
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(
            user=user,
            cus_name=self.cleaned_data['fullname'],
            mobile=self.cleaned_data['mobile']
        )
        customer.save()
        return user



class SearchForm(forms.Form):
    search = forms.CharField()