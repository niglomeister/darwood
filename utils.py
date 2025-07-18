import re 


def contains_numbers(s):
    return bool(re.search(r'\d', s))
def is_valid_phone(phone):
    pattern = r'^(\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'
    return bool(re.match(pattern, phone.strip()))
