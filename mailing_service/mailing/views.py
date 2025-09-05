from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Client, Message, Mailing, MailingAttempt
from .forms import ClientForm, MessageForm, MailingForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import cache_page


@cache_page(60)  # Кэшировать на 1 минуту
def cache_test_view(request):
    from django.http import HttpResponse
    from django.utils import timezone

    return HttpResponse(f"Время генерации страницы: {timezone.now()}")


def home(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status="started").count()
    unique_clients = Client.objects.values("email").distinct().count()

    context = {
        "total_mailings": total_mailings,
        "active_mailings": active_mailings,
        "unique_clients": unique_clients,
    }
    return render(request, "mailing/home.html", context)


# Представления для клиента
class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        # Менеджеры видят всех клиентов, обычные пользователи - только своих
        if self.request.user.has_perm("mailing.view_all_clients"):
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")

    def get_queryset(self):
        # Менеджеры могут редактировать всех, обычные - только своих
        if self.request.user.has_perm("mailing.view_all_clients"):
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("mailing:client_list")

    def get_queryset(self):
        # Менеджеры могут удалять всех, обычные - только своих
        if self.request.user.has_perm("mailing.view_all_clients"):
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)


# Представления для Message
class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        # Менеджеры видят все сообщения, обычные пользователи - только свои
        if self.request.user.has_perm("mailing.view_all_messages"):
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def get_queryset(self):
        # Менеджеры могут редактировать все, обычные - только свои
        if self.request.user.has_perm("mailing.view_all_messages"):
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")

    def get_queryset(self):
        # Менеджеры могут удалять все, обычные - только свои
        if self.request.user.has_perm("mailing.view_all_messages"):
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


# Представления для Mailing
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self):
        # Менеджеры видят все рассылки, обычные пользователи - только свои
        if self.request.user.has_perm("mailing.view_all_mailings"):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    def get_queryset(self):
        # Менеджеры могут редактировать все, обычные - только свои
        if self.request.user.has_perm("mailing.view_all_mailings"):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")

    def get_queryset(self):
        # Менеджеры могут удалять все, обычные - только свои
        if self.request.user.has_perm("mailing.view_all_mailings"):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = "mailing/attempt_list.html"
    context_object_name = "attempts"

    def get_queryset(self):
        if self.request.user.has_perm("mailing.view_all_mailings"):
            return MailingAttempt.objects.all().select_related("mailing")
        return MailingAttempt.objects.filter(
            mailing__owner=self.request.user
        ).select_related("mailing")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        attempts = self.get_queryset()

        # Статистика
        context["total_attempts"] = attempts.count()
        context["successful_attempts"] = attempts.filter(status="success").count()
        context["failed_attempts"] = attempts.filter(status="failed").count()
        context["success_rate"] = (
            (context["successful_attempts"] / context["total_attempts"] * 100)
            if context["total_attempts"] > 0
            else 0
        )

        # Статистика по рассылкам
        mailing_stats = []
        mailings = Mailing.objects.filter(attempts__isnull=False).distinct()

        for mailing in mailings:
            mailing_attempts = attempts.filter(mailing=mailing)
            mailing_stats.append(
                {
                    "mailing": mailing,
                    "total": mailing_attempts.count(),
                    "success": mailing_attempts.filter(status="success").count(),
                    "failed": mailing_attempts.filter(status="failed").count(),
                }
            )

        context["mailing_stats"] = mailing_stats

        return context


@login_required
def start_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)

    # Проверяем права: только владелец или менеджер может запускать
    if not (
        request.user == mailing.owner
        or request.user.has_perm("mailing.view_all_mailings")
    ):
        messages.error(request, "У вас нет прав для запуска этой рассылки")
        return redirect("mailing:mailing_list")

    mailing.status = "started"
    mailing.save()
    messages.success(request, f'Рассылка "{mailing.message.subject}" запущена!')

    return redirect("mailing:mailing_list")
