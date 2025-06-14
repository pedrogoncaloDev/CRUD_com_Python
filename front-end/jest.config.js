module.exports = {
    testEnvironment: 'node',
    testMatch: ['**/__tests__/**/*.js(*)', '**/?(*.)+(spec|test).js(x)'],
    transform: {
        '^.+\\.js$': ['babel-jest', { configFile: false }]
    },
}