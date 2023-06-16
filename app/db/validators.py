import re

from fastapi import HTTPException


def validate_email(email):

    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    return re.match(email_regex, email) is not None


def check_min_value(min_number: int, field_name: str):

    def check(value):
        if value < min_number:
            raise HTTPException(status_code=400,
                                detail='%s value must be greater than %s!' % (field_name, min_number))

    return check
