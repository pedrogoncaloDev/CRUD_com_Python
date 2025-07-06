from utils import date_to_string, is_valid_email, format_phone

def test_date_to_string():
    from datetime import datetime

    # Teste com um objeto datetime válido
    dt = datetime(2025, 1, 1, 12, 0, 0)
    assert date_to_string(dt) == "2025-01-01T12:00:00"

    # Teste com um objeto que não é datetime
    try:
        date_to_string("2025-01-01")
    except TypeError as e:
        assert str(e) == "Tipo não serializável"

def test_is_valid_email():
    # Teste com email válido
    assert is_valid_email("teste@gmail.com")

    #teste com email inválido
    assert not is_valid_email("teste@gmail")

def test_format_phone():
    # Teste com telefone no formato (00) 0000-0000
    assert format_phone("(11) 1234-5678") == "(11) 1234-5678"

    # Teste com telefone no formato (00) 00000-0000
    assert format_phone("(11) 91234-5678") == "(11) 91234-5678"

    # Teste com telefone sem formatação
    assert format_phone("11987654321") == "(11) 98765-4321"

    # Teste com telefone inválido
    assert format_phone("12345") == "12345"  # Retorna os dígitos sem formatação
    