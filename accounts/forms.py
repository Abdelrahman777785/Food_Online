from django import forms 
from .models import User, UserProfile
from .validators import allow_only_images_validator


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
        
#'foodbakery-dev-gallery-uploader'

class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'start typing...', 'required':'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn-success upload-btn'}), validators=[allow_only_images_validator]) # style button my restaurant
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class':'upload-btn foodbakery-dev-cover-upload-btn' , 'style':'display:;'}), validators=[allow_only_images_validator]) # style button my restaurant
    
    latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'})) # close write 
    longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'})) # close write 

    class Meta:
        model = UserProfile
        fields = ['profile_picture','cover_photo','address','country','state','city','pin_code','latitude','longitude',] 
        

# def __init__(self, *args, **kwargs):   ### close write 
#     super(UserProfileForm, self).__init__(*args, **kwargs)
#     for field in self.fields:
#         if field == 'latitude' or field == 'longitude':
#             self.fields[field].widget.attrs['readonly'] = 'readonly'


class UserInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']