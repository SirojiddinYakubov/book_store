import re
from django.core.validators import ValidationError

def validate_phone(value):
    pattern = r"^998\d{9}$"
    print('pattern', value)
    if not re.search(pattern, str(value)):
        raise ValidationError('Phone number must begin with 998 and contain only 12 numbers')