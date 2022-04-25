import re

def password_complexity(password):

    password_length = 8
    password_upper = True
    password_lower = True
    password_special = True
    password_digit = True

    if len(password) < password_length:
        return False
    elif password_upper and re.search(r"[A-Z]", password) is None:
        return False
    elif password_lower and re.search(r"[a-z]", password) is None:
        return False
    elif password_special and re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None:
        return False
    elif password_digit and re.search(r"\d", password) is None:
        return False
    else:
        return True
