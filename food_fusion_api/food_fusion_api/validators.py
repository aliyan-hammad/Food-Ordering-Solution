from django.core.exceptions import ValidationError

def validator_contact(value):
    if len(value) != 11 or not value.isdigit():
        raise ValidationError(message='contact number should be 11 digits exactly')
    if int(value) <= 0:
        raise ValidationError(message='please enter your number in positive intigers')