from django import forms

from accounts.validators import allow_only_images_validator
from .models import Category, FoodItem


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name','description',]

class FoodItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn-success upload-btn'}), validators=[allow_only_images_validator]) # style button my restaurant
    class Meta:
        model = FoodItem
        fields = ['category','food_title','description','price','image','is_available',]