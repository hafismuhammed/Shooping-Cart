from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class ProductForm(forms.Form):
    product_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
        max_length=255, required=True
    )
    product_discription = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Product Description', 'rows': 5}),
        max_length=1000, required=True
    )
    price = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Product price'}),
        required=True
    )
    product_image = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'multiple': False}),
        required=True
    )