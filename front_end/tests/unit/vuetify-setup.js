import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

export function withVuetify(mountOptions = {}) {
    const vuetify = createVuetify({ components, directives });

    return {
        ...mountOptions,
        global: {
            ...(mountOptions.global || {}),
            plugins: [vuetify, ...((mountOptions.global && mountOptions.global.plugins) || [])],
        },
    };
}
