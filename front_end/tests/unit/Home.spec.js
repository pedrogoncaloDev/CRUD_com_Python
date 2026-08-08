import { flushPromises, mount } from '@vue/test-utils';
import axios from 'axios';
import Home from '../../src/components/Home.vue';
import Grid from '../../src/components/Grid.vue';
import AddUser from '../../src/components/AddUser.vue';
import { withVuetify } from './vuetify-setup';

jest.mock('axios');

const user = { id: 1, nome: 'Ana Silva', email: 'ana@example.com', telefone: '11987654321', data_criacao: null, data_atualizacao: null };

function mountHome() {
    return mount(Home, withVuetify({ attachTo: document.body }));
}

describe('Home.vue (integração)', () => {
    beforeEach(() => {
        axios.get.mockResolvedValue({ data: { users: [user], total: 1, page: 1, per_page: 10 } });
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    it('busca os usuários ao montar e repassa para o Grid', async () => {
        const wrapper = mountHome();
        await flushPromises();

        expect(axios.get).toHaveBeenCalledWith(
            expect.stringContaining('/users'),
            { params: { page: 1, per_page: 10, search: undefined } },
        );
        expect(wrapper.findComponent(Grid).props('users')).toEqual([user]);
        expect(wrapper.findComponent(Grid).props('totalUsers')).toBe(1);
    });

    it('busca em todas as páginas ao pesquisar, voltando para a página 1', async () => {
        const wrapper = mountHome();
        await flushPromises();

        wrapper.vm.page = 3;
        await wrapper.findComponent(Grid).vm.$emit('search', 'ana');
        await flushPromises();

        expect(axios.get).toHaveBeenLastCalledWith(
            expect.stringContaining('/users'),
            { params: { page: 1, per_page: 10, search: 'ana' } },
        );
        expect(wrapper.vm.page).toBe(1);
    });

    it('mostra mensagem de erro quando a busca de usuários falha', async () => {
        axios.get.mockRejectedValue({ response: { data: { message: 'Erro ao buscar os usuários.' } } });

        const wrapper = mountHome();
        await flushPromises();

        expect(wrapper.vm.messageModal.dialog).toBe(true);
        expect(wrapper.vm.messageModal.color).toBe('error');
    });

    it('abre o modal de edição com o usuário selecionado no Grid', async () => {
        const wrapper = mountHome();
        await flushPromises();

        await wrapper.findComponent(Grid).vm.$emit('EditUser', user);

        expect(wrapper.vm.ShowModalEditUser).toBe(true);
        expect(wrapper.vm.informationsUser).toEqual(user);
    });

    it('abre o modal de exclusão com o usuário selecionado no Grid', async () => {
        const wrapper = mountHome();
        await flushPromises();

        await wrapper.findComponent(Grid).vm.$emit('DeleteUser', user);

        expect(wrapper.vm.ShowModalDeleteUser).toBe(true);
        expect(wrapper.vm.informationsUser).toEqual(user);
    });

    it('fecha os modais e recarrega a lista quando CloseModal é emitido', async () => {
        const wrapper = mountHome();
        await flushPromises();
        await wrapper.findComponent(Grid).vm.$emit('EditUser', user);

        wrapper.vm.CloseModal();
        await flushPromises();

        expect(wrapper.vm.ShowModalEditUser).toBe(false);
        expect(wrapper.vm.ShowModalDeleteUser).toBe(false);
        expect(axios.get).toHaveBeenCalledTimes(2);
    });

    it('recarrega a lista e exibe mensagem de sucesso quando o AddUser cria um usuário', async () => {
        const wrapper = mountHome();
        await flushPromises();

        await wrapper.findComponent(AddUser).vm.$emit('showMessageModal', 'Sucesso', 'Usuário criado com sucesso!');
        await wrapper.findComponent(AddUser).vm.$emit('GetUsers');
        await flushPromises();

        expect(wrapper.vm.messageModal).toMatchObject({ dialog: true, color: 'success', message: 'Usuário criado com sucesso!' });
        expect(axios.get).toHaveBeenCalledTimes(2);
    });
});
