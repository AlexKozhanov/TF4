from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100,
        required=False,
        help_text='Mail')
    first_name = forms.CharField(
        max_length=150,
        required=False,
        help_text='Имя')
    last_name = forms.CharField(
        max_length=150,
        required=False,
        help_text='Фамилия')
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        help_text='Номер телефона')
    country = forms.CharField(
        max_length=50,
        required=False,
        help_text='Страна')
    avatar = forms.ImageField(
        upload_to='users/avatars/',
        required=False,
        help_text='Аватар')

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'country',
            'avatar',
            'password1',
            'password2',)

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Приложите emaiiil'
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Приложите first_name'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Приложите last_name'
        })
        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите телефоооон!'
        })
        self.fields['country'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите country'
        })
        self.fields['avatar'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите avatar'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите password1'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите password2'
        })

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError('Номер должен состоять только из цифр')
        return phone_number