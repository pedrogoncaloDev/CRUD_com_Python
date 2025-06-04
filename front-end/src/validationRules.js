export const validationRules = {
    required: value => !!value || 'Este campo é obrigatório.',
    telefone: value => {
        if (!value || value.trim() === '') return true;
        
        const digitsOnly = value.replace(/\D/g, '');
        return (digitsOnly.length === 10 || digitsOnly.length === 11) || 'Tamanho do número de telefone inválido';
    },
    email: value => {
        const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return pattern.test(value) || 'E-mail inválido.';
    }
};