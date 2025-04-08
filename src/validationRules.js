export const validationRules = {
    required: value => !!value || 'Este campo é obrigatório.',
    telefone: value => (value && value.length == 11) || 'Telefone inválido',
    email: value => {
        const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return pattern.test(value) || 'E-mail inválido.';
    }
};