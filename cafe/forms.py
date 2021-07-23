from django import forms
from django.forms import ModelForm

# def name_validation(value:str):
#     if not value.istitle():
#         reasie validationError
#
#
# class CreateMenuItem(forms.Form):
#     name = forms.CharField(max_length=50, label='my name is menuitem')
#     price = forms.IntegerField()
#     Discount = forms.IntegerField()
#     Category = forms.IntegerField()
#     image = forms.FileField(required=False)
from cafe.models import MenuItems


class CreateMenuItem(forms.ModelForm):
    class Meta:
        model= MenuItems
        fields = ['name', 'price', 'category']
        widgets = {
            # 'name':forms.CharField(),
            'category':forms.Select()
        }


