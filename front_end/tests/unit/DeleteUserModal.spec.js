import { mount } from '@vue/test-utils';
import axios from 'axios';
import DeleteUserModal from '../../src/modais/DeleteUserModal.vue';
import { withVuetify } from './vuetify-setup';

jest.mock('axios');

const informationsUser = { id: 1, nome: 'Ana Silva' };

function mountModal(props = {}) {
    return mount(DeleteUserModal, withVuetify({
        attachTo: document.body,
        props: { dialog: true, informationsUser, ...props },
    }));
}

describe('DeleteUserModal.vue', () => {
    afterEach(() => {
        jest.clearAllMocks();
    });

    it('exibe o nome e o id do usuário a ser deletado', () => {
        mountModal();
        // O v-dialog do Vuetify usa Teleport para renderizar no <body>, fora da árvore do wrapper.
        expect(document.body.textContent).toContain('Ana Silva');
        expect(document.body.textContent).toContain('1');
    });

    it('deleta o usuário e emite os eventos de sucesso', async () => {
        axios.delete.mockResolvedValue({});

        const wrapper = mountModal();
        await wrapper.vm.confirmDelete();
        await wrapper.vm.$nextTick();

        expect(axios.delete).toHaveBeenCalledWith(expect.stringContaining(`/users/${informationsUser.id}`));
        expect(wrapper.emitted('CloseModal')).toHaveLength(1);
        expect(wrapper.emitted('showMessageModal')).toEqual([
            ['Sucesso', 'Usuário deletado com sucesso!'],
        ]);
    });

    it('emite mensagem de erro quando a exclusão falha', async () => {
        axios.delete.mockRejectedValue(new Error('falha de rede'));

        const wrapper = mountModal();
        await wrapper.vm.confirmDelete();
        await wrapper.vm.$nextTick();

        expect(wrapper.emitted('CloseModal')).toBeUndefined();
        expect(wrapper.emitted('showMessageModal')).toEqual([
            ['Erro', 'Erro ao deletar o usuário!'],
        ]);
    });
});
