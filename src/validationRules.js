export const validationRules = {
    required: value => !!value || 'Este campo é obrigatório.',
    email: value => {
        const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return pattern.test(value) || 'E-mail inválido.';
    }
};