import { formatDate, formatPhone, API_URL } from '../../src/utils.js';

describe('formatDate', () => {
    it('formata uma data ISO corretamente', () => {
        expect(formatDate('2024-07-07T15:30:45Z')).toBe('07/07/2024 15:30:45');
    });

    it('formata outra data ISO corretamente', () => {
        expect(formatDate('2023-01-01T01:02:03Z')).toBe('01/01/2023 01:02:03');
    });
});

describe('formatPhone', () => {
    it('formata número de 11 dígitos', () => {
        expect(formatPhone('11999999999')).toBe('(11) 99999-9999');
    });

    it('formata número de 10 dígitos', () => {
        expect(formatPhone('1133334444')).toBe('(11) 3333-4444');
    });

    it('formata número com caracteres não numéricos', () => {
        expect(formatPhone('(11) 99999-9999')).toBe('(11) 99999-9999');
    });

    it('formata número incompleto', () => {
        expect(formatPhone('11')).toBe('(11');
        expect(formatPhone('119')).toBe('(11) 9');
    });

    it('retorna string vazia para entrada vazia', () => {
        expect(formatPhone('')).toBe('');
        expect(formatPhone(null)).toBe('');
        expect(formatPhone(undefined)).toBe('');
    });
});

describe('API_URL', () => {
    it('possui o valor correto', () => {
        expect(API_URL).toBe('http://localhost:5000/users');
    });
});