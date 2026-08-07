import { mount } from '@vue/test-utils';
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
    it('não filtra nada quando a busca está vazia', () => {
        const wrapper = mountGrid();
        expect(wrapper.vm.filteredUsers).toHaveLength(2);
    });

    it('filtra usuários pelo nome', () => {
        const wrapper = mountGrid();
        wrapper.vm.search = 'ana';
        expect(wrapper.vm.filteredUsers).toEqual([users[0]]);
    });

    it('filtra usuários pelo email', () => {
        const wrapper = mountGrid();
        wrapper.vm.search = 'bruno@example.com';
        expect(wrapper.vm.filteredUsers).toEqual([users[1]]);
    });

    it('filtra usuários pelo id', () => {
        const wrapper = mountGrid();
        wrapper.vm.search = '777';
        expect(wrapper.vm.filteredUsers).toEqual([users[1]]);
    });

    it('emite GetUsers ao clicar no botão de recarregar', async () => {
        const wrapper = mountGrid();
        await wrapper.find('button').trigger('click');
        expect(wrapper.emitted('GetUsers')).toHaveLength(1);
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
