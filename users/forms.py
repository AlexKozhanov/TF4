from django import forms
from django.contrib.auth.forms import (
    PasswordResetForm, SetPasswordForm, UserCreationForm, UserChangeForm, AuthenticationForm)
from django.forms import ModelForm
from django.urls import reverse_lazy

from diary.forms import StyleFormMixin
from users.models import User


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    model = User


class UserRegistrationForm(StyleFormMixin, UserCreationForm):
    """
    Модель регистрация пользователя.
    """
    class Meta:
        model = User
        template_name = "users/user_form.html"
        fields = ("email", "password1", "password2")

    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой email уже используется в системе")
        return email


class UserForm(StyleFormMixin, UserChangeForm):
    """
    Модель форма пользователя.
    """
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "phone_number",
            "country",
            "avatar",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        phone_number = self.fields["phone_number"].widget

        self.fields["password"].widget = forms.HiddenInput()
        phone_number.attrs["class"] = "form-control bfh-phone"
        phone_number.attrs["data-format"] = "+7 (ddd) ddd-dd-dd"


class UserUpdateForm(StyleFormMixin, ModelForm):
    """
    Модель изменение пользователя.
    """
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "phone_number",
            "country",
            "avatar",
        )
        success_url = reverse_lazy("users:users")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        phone_number = self.fields["phone_number"].widget

        self.fields["password"].widget = forms.HiddenInput()
        phone_number.attrs["class"] = "form-control bfh-phone"
        phone_number.attrs["data-format"] = "+7 (ddd) ddd-dd-dd"

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Пользователь с таким Email уже существует.")

        return email


class UserForgotPasswordForm(PasswordResetForm):
    """Форма запроса на восстановление пароля"""

    def __init__(self, *args, **kwargs):
        """Обновление стилей формы"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


class UserSetNewPasswordForm(SetPasswordForm):
    """
    Форма изменения пароля пользователя после подтверждения
    """

    def __init__(self, *args, **kwargs):
        """Обновление стилей формы"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


class PasswordRecoveryForm(StyleFormMixin, forms.Form):
    """
    Модель форма восстановления пароля.
    """
    email = forms.EmailField(label="Укажите Email")

    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Такого email нет в системе")
        return email
