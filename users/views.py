import secrets

from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordResetConfirmView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import (
    DetailView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    FormView,
    TemplateView,)

from config.settings import EMAIL_HOST_USER
from users.forms import (
    UserRegistrationForm, UserUpdateForm,
    UserForgotPasswordForm, UserSetNewPasswordForm,
    PasswordRecoveryForm, UserLoginForm, )
from users.models import User


# --- CRUD User ---
class UserCreateView(CreateView):
    """
    Модель создания пользователя.
    """
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:email_confirmation")

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в наш сервис!'
        message = 'Спасибо т**е, что зарегистрировался в нашем сервисе!'
        from_email = 'iVasya2033@yandex.ru'
        recipient_list = [user_email, ]
        send_mail(subject, message, from_email, recipient_list)

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        user.token = token

        users_group = Group.objects.get(name='Пользователи')
        user.groups.add(users_group)

        user.save()
        send_mail(
            subject="Подтверждение почты",
            message=f"Здравствуйте, перейдите по ссылке для подтверждения почты: {url} ",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Модель просмотра пользователя.
    """
    model = User
    template_name = "users/user_list.html"

    def test_func(self):
        return self.request.user.is_superuser


class UserDetailView(LoginRequiredMixin, DetailView):
    """
    Модель Детального просмотра пользователя.
    """
    model = User
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.object.email == self.request.user.email:
            return self.object
        raise PermissionDenied


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    Модель Изменения пользователя.
    """
    model = User
    form_class = UserUpdateForm

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy("users:user_list")
        else:
            return reverse_lazy("diary:home")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.object.email == self.request.user.email:
            return self.object
        raise PermissionDenied


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy("users:users")
        else:
            return reverse_lazy("diary:home")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.object.email == self.request.user.email:
            return self.object
        raise PermissionDenied

    # Поменять на прощание
    # def send_welcome_email(self, idiot_email):
    #     subject = 'Добро пожаловать в наш сервис!'
    #     message = 'Спасибо т**е, что зарегистрировался в нашем сервисе!'
    #     from_email = 'iVasya2033@yandex.ru'
    #     recipient_list = [idiot_email, ]
    #     send_mail(subject, message, from_email, recipient_list)


class UserLoginView(LoginView):
    model = User
    form_class = UserLoginForm


class EmailConfirmationView(TemplateView):
    model = User
    template_name = "users/email_confirmation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Письмо активации отправлено"
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """Представление установки нового пароля"""

    form_class = UserSetNewPasswordForm
    template_name = "users/user_password_set_new.html"
    success_url = reverse_lazy("users:login")
    success_message = "Пароль успешно изменен. Можете авторизоваться на сайте."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Установить новый пароль"
        return context


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """Представление по сбросу пароля по почте"""

    form_class = UserForgotPasswordForm
    template_name = "users/password_reset.html"
    success_url = reverse_lazy("users:login")
    success_message = "Письмо с инструкцией по восстановлению пароля отправлено на ваш email"
    subject_template_name = "users/email/password_subject_reset_mail.txt"
    email_template_name = "users/email/password_reset_mail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Запрос на восстановление пароля"
        return context


class PasswordRecoveryView(FormView):
    template_name = "users/password_recovery.html"
    form_class = PasswordRecoveryForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = User.objects.get(email=email)
        length = 12
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        password = get_random_string(length, alphabet)
        user.set_password(password)
        user.save()
        send_mail(
            subject="Восстановление пароля",
            message=f"Ваш новый пароль: {password}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return super().form_valid(form)
