from django import forms

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    # Card info would go here in real life
