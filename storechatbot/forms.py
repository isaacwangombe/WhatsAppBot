from django import forms


class MessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(
        attrs={"rows": "5"}), label="message", max_length=500)
