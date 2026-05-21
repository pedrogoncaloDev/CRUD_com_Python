from datetime import datetime

def date_to_string(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Converte para string no formato ISO 8601
    raise TypeError("Tipo não serializável")


def is_valid_email(email):
    # Valida se o email está no formato correto.
    import re
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None


def valid_phone(phone):
    # Remove todos os caracteres não numéricos
    digits = ''.join(filter(str.isdigit, str(phone)))
    
    if len(digits) == 10:  # Válido - Formato (00) 0000-0000
        return True
    elif len(digits) == 11:  # Válido - Formato (00) 00000-0000
        return True
    else:
        # Número de telefone inválido
        return False