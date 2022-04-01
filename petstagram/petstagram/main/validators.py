from django.core.exceptions import ValidationError


def only_letters_validator(value):
    for char in value:
        if not char.isalpha():
            raise ValidationError('Value must contains only letters')
