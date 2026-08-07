from datetime import datetime

import pytest

from utils import date_to_string, is_valid_email, valid_phone


class TestDateToString:
    def test_converte_datetime_para_iso(self):
        dt = datetime(2025, 1, 1, 12, 0, 0)
        assert date_to_string(dt) == "2025-01-01T12:00:00"

    def test_levanta_type_error_para_nao_datetime(self):
        with pytest.raises(TypeError, match="Tipo não serializável"):
            date_to_string("2025-01-01")


class TestIsValidEmail:
    @pytest.mark.parametrize("email", [
        "teste@gmail.com",
        "usuario.nome@empresa.com.br",
        "usuario+tag@dominio.io",
    ])
    def test_emails_validos(self, email):
        assert is_valid_email(email) is True

    @pytest.mark.parametrize("email", [
        "teste@gmail",
        "sem-arroba.com",
        "@dominio.com",
        "usuario@",
        "",
    ])
    def test_emails_invalidos(self, email):
        assert is_valid_email(email) is False


class TestValidPhone:
    @pytest.mark.parametrize("phone", [
        "(11) 1234-5678",
        "(11) 91234-5678",
        "11987654321",
        "1133334444",
    ])
    def test_telefones_com_10_ou_11_digitos_sao_validos(self, phone):
        assert valid_phone(phone) is True

    @pytest.mark.parametrize("phone", [
        "12345",
        "",
        "119876543210",
    ])
    def test_telefones_fora_do_padrao_sao_invalidos(self, phone):
        assert valid_phone(phone) is False
