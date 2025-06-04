import { createApp } from 'vue';
import 'vuetify/styles';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import App from './App.vue';
import '@mdi/font/css/materialdesignicons.css';

const vuetify = createVuetify({
    components,
    directives,
    theme: {
        defaultTheme: 'dark',
        themes: {
            dark: {
                dark: true,
                colors: {
                primary: '#1E88E5', // Azul
                secondary: '#424242', // Cinza escuro
                background: '#121212', // Fundo escuro
                surface: '#1E1E1E', // Superfície escura
                error: '#FF5252', // Vermelho
                info: '#2196F3', // Azul
                success: '#4CAF50', // Verde
                warning: '#FFC107', // Amarelo
                },
            },
        },
    },
});

createApp(App).use(vuetify).mount('#app');