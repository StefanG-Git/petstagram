from django.core.exceptions import ValidationError


def validate_only_letters(value):
    for char in value:
        if not char.isalpha():
            raise ValidationError('Value must contains only letters')


def validate_file_max_size_in_mb(max_size):
    def validate(value):
        file_size = value.file.size
        if file_size > max_size * 1024 * 1024:
            raise ValidationError(f'Max file size is {max_size}MB')

    return validate
