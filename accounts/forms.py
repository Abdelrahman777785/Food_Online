from django import forms 
from .models import User, UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']

    def clean(self):
        clean_data = super(UserForm, self).clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "password does not match!"
            )
        


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'upload-btn foodbakery-dev-cover-upload-btn', 'style':'display:;'}))
    cover_photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'foodbakery-dev-gallery-uploader', 'style':'display:;'}))
    class Meta:
        model = UserProfile
        fields = ['profile_picture','cover_photo','address_line_1','address_line_2','country','state','city','pin_code','latitude','longitude',] 
        
