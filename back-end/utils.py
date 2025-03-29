from datetime import datetime

# Função para converter datetime para string
def date_to_string(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Converte para string no formato ISO 8601
    raise TypeError("Tipo não serializável")


def is_valid_email(email):
    # Valida se o email está no formato correto.
    import re
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None