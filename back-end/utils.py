from datetime import datetime

# Função para converter datetime para string
def date_to_string(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Converte para string no formato ISO 8601
    raise TypeError("Tipo não serializável")