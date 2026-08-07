import { validationRules } from '../../src/validationRules.js';

describe('validationRules.required', () => {
    it('rejeita valores vazios', () => {
        expect(validationRules.required('')).toBe('Este campo é obrigatório.');
        expect(validationRules.required(null)).toBe('Este campo é obrigatório.');
        expect(validationRules.required(undefined)).toBe('Este campo é obrigatório.');
    });

    it('aceita valores preenchidos', () => {
        expect(validationRules.required('Ana')).toBe(true);
    });
});

describe('validationRules.telefone', () => {
    it('aceita campo vazio (telefone é opcional)', () => {
        expect(validationRules.telefone('')).toBe(true);
        expect(validationRules.telefone('   ')).toBe(true);
    });

    it('aceita telefone com 10 dígitos', () => {
        expect(validationRules.telefone('(11) 3333-4444')).toBe(true);
    });

    it('aceita telefone com 11 dígitos', () => {
        expect(validationRules.telefone('(11) 99999-9999')).toBe(true);
    });

    it('rejeita telefone com tamanho inválido', () => {
        expect(validationRules.telefone('123')).toBe('Tamanho do número de telefone inválido');
    });
});

describe('validationRules.email', () => {
    it('aceita emails válidos', () => {
        expect(validationRules.email('ana@example.com')).toBe(true);
    });

    it('rejeita emails inválidos', () => {
        expect(validationRules.email('ana@example')).toBe('E-mail inválido.');
        expect(validationRules.email('ana.example.com')).toBe('E-mail inválido.');
        expect(validationRules.email('')).toBe('E-mail inválido.');
    });
});
