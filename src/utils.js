export const API_URL = 'http://localhost:5000/users';

export function formatDate(isoString) {
    const date = new Date(isoString);

    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
}

export function formatPhone(limitedDigits) {
    const digits = limitedDigits.replace(/\D/g, ''); // Remove não numéricos
    const length = digits.length;
    
    let formatted = '';
    
    // Adiciona DDD (##)
    if (length >= 1) {
        formatted += `(${digits.substring(0, 2)}`;
    }
    
    // Formata o restante do número
    if (length > 2) {
        if (length === 10) { // (##) ####-####
            formatted += `) ${digits.substring(2, 6)}-${digits.substring(6)}`;
        } else if (length === 11) { // (##) #####-####
            formatted += `) ${digits.substring(2, 7)}-${digits.substring(7)}`;
        } else { // Outros casos (formata parcialmente)
            formatted += `) ${digits.substring(2)}`;
        }
    }
    
    return formatted;
}