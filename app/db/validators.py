import re


def validate_email(email):

    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    return re.match(email_regex, email) is not None
