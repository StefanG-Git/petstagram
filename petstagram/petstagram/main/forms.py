from django import forms

from petstagram.main.helpers import BootstrapFormMixin, get_this_year, DisableFieldsFormMixin
from petstagram.main.models import Profile, PetPhoto, Pet


class CreateProfileForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'picture',)
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                },
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name',
                },
            ),
            'picture': forms.URLInput(
                attrs={
                    'placeholder': 'Enter URL',
                },
            ),
        }


class EditProfileForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self.initial['gender'] = Profile.DO_NOT_SHOW

    class Meta:
        YEAR_MIN_VALUE = 1920

        model = Profile
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                },
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name',
                },
            ),
            'picture': forms.URLInput(
                attrs={
                    'placeholder': 'Enter URL',
                },
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter email',
                },
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Enter description',
                    'rows': 3,
                },
            ),
            'date_of_birth': forms.SelectDateWidget(
                years=range(get_this_year(), YEAR_MIN_VALUE - 1, -1),
            ),
        }


class DeleteProfileForm(forms.ModelForm):
    def save(self, commit=True):
        pets = list(self.instance.pet_set.all())
        pet_photos = PetPhoto.objects.filter(tagged_pets__in=pets)
        pet_photos.delete()
        self.instance.delete()

        return self.instance

    class Meta:
        model = Profile
        fields = ()


class CreatePetForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        YEAR_MIN_VALUE = 1920

        model = Pet
        exclude = ('user_profile',)
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter pet name',
                },
            ),
            'date_of_birth': forms.SelectDateWidget(
                years=range(get_this_year(), YEAR_MIN_VALUE - 1, -1),
            ),
        }


class EditPetForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        YEAR_MIN_VALUE = 1920

        model = Pet
        exclude = ('user_profile',)
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter pet name',
                },
            ),
            'date_of_birth': forms.SelectDateWidget(
                years=range(get_this_year(), YEAR_MIN_VALUE - 1, -1),
            ),
        }


class DeletePetForm(BootstrapFormMixin, DisableFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self._init_disabled_fields()

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        YEAR_MIN_VALUE = 1920

        model = Pet
        exclude = ('user_profile',)
        widgets = {
            'date_of_birth': forms.SelectDateWidget(
                years=range(get_this_year(), YEAR_MIN_VALUE - 1, -1),
            ),
        }
