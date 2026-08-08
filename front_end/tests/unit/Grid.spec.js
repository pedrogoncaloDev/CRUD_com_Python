import { mount } from '@vue/test-utils';
import { nextTick } from 'vue';
import Grid from '../../src/components/Grid.vue';
import { withVuetify } from './vuetify-setup';

const users = [
    { id: 1, nome: 'Ana Silva', email: 'ana@example.com', telefone: '11900001111', data_criacao: null, data_atualizacao: null },
    { id: 777, nome: 'Bruno Costa', email: 'bruno@example.com', telefone: '11900003333', data_criacao: null, data_atualizacao: null },
];

function mountGrid(props = {}) {
    return mount(Grid, withVuetify({ props: { users, ...props } }));
}

describe('Grid.vue', () => {
    beforeEach(() => {
        jest.useFakeTimers();
    });

    afterEach(() => {
        jest.runOnlyPendingTimers();
        jest.useRealTimers();
    });

    it('não emite search antes do debounce vencer', async () => {
        const wrapper = mountGrid();
        wrapper.vm.search = 'ana';
        await nextTick();

        jest.advanceTimersByTime(399);

        expect(wrapper.emitted('search')).toBeUndefined();
    });

    it('emite search com o termo (sem espaços) após o debounce', async () => {
        const wrapper = mountGrid();
        wrapper.vm.search = '  ana  ';
        await nextTick();

        jest.advanceTimersByTime(400);

        expect(wrapper.emitted('search')).toEqual([['ana']]);
    });

    it('reinicia o debounce a cada nova digitação', async () => {
        const wrapper = mountGrid();
        wrapper.vm.search = 'a';
        await nextTick();
        jest.advanceTimersByTime(200);

        wrapper.vm.search = 'an';
        await nextTick();
        jest.advanceTimersByTime(200);

        wrapper.vm.search = 'ana';
        await nextTick();
        jest.advanceTimersByTime(400);

        expect(wrapper.emitted('search')).toEqual([['ana']]);
    });

    it('emite GetUsers ao clicar no botão de recarregar', async () => {
        const wrapper = mountGrid();
        // A v-data-table-server já emite GetUsers uma vez ao montar (opções padrão).
        const emissionsBeforeClick = wrapper.emitted('GetUsers').length;

        await wrapper.find('button').trigger('click');

        expect(wrapper.emitted('GetUsers')).toHaveLength(emissionsBeforeClick + 1);
        expect(wrapper.emitted('GetUsers').at(-1)).toEqual([]);
    });

    it('emite EditUser com o usuário correto', async () => {
        const wrapper = mountGrid();
        await wrapper.find('.mdi-file-edit-outline').trigger('click');
        expect(wrapper.emitted('EditUser')[0]).toEqual([users[0]]);
    });

    it('emite DeleteUser com o usuário correto', async () => {
        const wrapper = mountGrid();
        await wrapper.find('.mdi-delete-outline').trigger('click');
        expect(wrapper.emitted('DeleteUser')[0]).toEqual([users[0]]);
    });
});
