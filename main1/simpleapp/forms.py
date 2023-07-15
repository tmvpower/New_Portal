from django import forms
from django.core.exceptions import ValidationError

from .models import Product, News


class ProductForm(forms.ModelForm):
    description = forms.CharField(min_length=20)

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'quantity']

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("description")
        name = cleaned_data.get("name")

        if name == description:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data

class NewsForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = News
        fields = ['name', 'author', 'content', 'date_published']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        content = cleaned_data.get("content")

        if name == content:
            raise ValidationError(
                "Содержание не должно быть идентично названию."
            )

        return cleaned_data

class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = News
        fields = ['name', 'author', 'content', 'date_published']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        content = cleaned_data.get("content")

        if name == content:
            raise ValidationError(
                "Содержание не должно быть идентично названию."
            )

        return cleaned_data
