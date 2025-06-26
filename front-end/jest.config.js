module.exports = {
    moduleFileExtensions: ['js', 'json', 'vue'], // extensões reconhecidas
    transform: {
        '^.+\\.vue$': '@vue/vue3-jest', // transforma arquivos .vue usando Vue 3 Jest
        '^.+\\.(js|jsx)$': 'babel-jest' // transpila arquivos .js e .jsx usando Babel
    },
    transformIgnorePatterns: [
        '/node_modules/(?!(vuetify)/)' // transpila também o Vuetify (que usa import/export ES6)
    ],
}