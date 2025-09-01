from django import forms
from .models import  Client, Message, Mailing


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.request:
            instance.owner = self.request.user
        if commit:
            instance.save()
        return instance


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.request:
            instance.owner = self.request.user
        if commit:
            instance.save()
        return instance


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_time', 'end_time', 'message', 'clients']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'clients': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request:
            self.fields['message'].queryset = Message.objects.filter(owner=self.request.user)
            self.fields['clients'].queryset = Client.objects.filter(owner=self.request.user)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.request:
            instance.owner = self.request.user
        if commit:
            instance.save()
            self.save_m2m()
        return instance

