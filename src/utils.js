export const API_URL = 'http://localhost:5000/users';

export function formatDate(isoString) {
    const date = new Date(isoString);

    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Meses começam do zero
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
}

export function formatPhone(limitedDigits) {
    const digits = limitedDigits.replace(/\D/g, '');
    
    let formatted = '';
    const length = digits.length;
    
    if (length >= 1) formatted += `(${digits.substring(0, 2)}`;
    if (length > 2) {
        // Limita a 8 ou 9 dígitos após o DDD (opcional)
        const maxDigits = 9; // Ou 8, dependendo do padrão
        formatted += `) ${digits.substring(2, 2 + maxDigits)}`;
    }
    
    return formatted;
}