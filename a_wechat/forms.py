from django import forms
from a_wechat.models import ChatGroup, ChatGroupMessages


class ChatMessageCreateForm(forms.ModelForm):

    class Meta:
        model = ChatGroupMessages
        fields = ['body']
        labels = {
            'body': ''
        }
        widgets = {
            'body': forms.TextInput(attrs={
                'placeholder': 'Write Message...',
                'class': 'w-full p-3 border border-gray-300 rounded-full bg-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-200 focus:border-indigo-200 text-gray-600',
                'maxlength': '300',
                'autofocus': True  # Corrected from 'autofocud' to 'autofocus'
            })
        }