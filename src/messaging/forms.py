from django.forms.models import ModelForm

from messaging.models import GroupMessage


class ChatMessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ["body"]
