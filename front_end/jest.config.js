// Precisa ser setado aqui (carregado antes dos workers de teste subirem) e não em
// setupFiles: o V8 cacheia o timezone do processo e ignora mudanças em process.env.TZ
// feitas depois que o processo já iniciou (efeito observado no Windows).
process.env.TZ = 'UTC';

module.exports = {
    moduleFileExtensions: ['js', 'json', 'vue'], // extensões reconhecidas
    testEnvironment: 'jsdom',
    setupFiles: ['<rootDir>/tests/unit/setup.js'],
    moduleNameMapper: {
        '\\.(css|less|scss)$': '<rootDir>/tests/unit/styleMock.js',
        '^@/(.*)$': '<rootDir>/src/$1',
    },
    transform: {
        '^.+\\.vue$': '@vue/vue3-jest', // transforma arquivos .vue usando Vue 3 Jest
        '^.+\\.(js|jsx)$': 'babel-jest' // transpila arquivos .js e .jsx usando Babel
    },
    transformIgnorePatterns: [
        '/node_modules/(?!(vuetify)/)' // transpila também o Vuetify (que usa import/export ES6)
    ],
}