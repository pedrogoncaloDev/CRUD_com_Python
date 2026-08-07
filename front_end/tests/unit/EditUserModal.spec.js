import { mount } from '@vue/test-utils';
import axios from 'axios';
import EditUserModal from '../../src/modais/EditUserModal.vue';
import { withVuetify } from './vuetify-setup';

jest.mock('axios');

// telefone já vem no formato mascarado: o watcher 'user.telefone' reformata o valor assim
// que os dados são sincronizados, então usar o valor já formatado aqui evita falso-positivo
// no teste do guard "nada foi alterado" (ver EditUserModal.vue, watch: 'user.telefone').
const informationsUser = { id: 1, nome: 'Ana Silva', email: 'ana@example.com', telefone: '(11) 98765-4321', data_criacao: null, data_atualizacao: null };

function mountModal() {
    const wrapper = mount(EditUserModal, withVuetify({
        props: { dialog: true, informationsUser: {} },
    }));
    wrapper.vm.$refs.form.validate = jest.fn().mockResolvedValue({ valid: true, errors: [] });
    return wrapper;
}

describe('EditUserModal.vue', () => {
    afterEach(() => {
        jest.clearAllMocks();
    });

    it('sincroniza os dados do formulário quando o usuário selecionado muda', async () => {
        const wrapper = mountModal();

        await wrapper.setProps({ informationsUser });

        expect(wrapper.vm.user).toEqual(informationsUser);
    });

    it('não chama a API quando nada foi alterado', async () => {
        const wrapper = mountModal();
        await wrapper.setProps({ informationsUser });

        await wrapper.vm.handleSubmit();

        expect(axios.put).not.toHaveBeenCalled();
        expect(wrapper.emitted('CloseModal')).toBeUndefined();
    });

    it('salva a edição e emite os eventos de sucesso quando há alteração válida', async () => {
        axios.put.mockResolvedValue({ status: 201 });

        const wrapper = mountModal();
        await wrapper.setProps({ informationsUser });
        wrapper.vm.user.nome = 'Ana Souza';

        await wrapper.vm.handleSubmit();

        expect(axios.put).toHaveBeenCalledWith(
            expect.stringContaining('/users'),
            expect.objectContaining({ nome: 'Ana Souza' })
        );
        expect(wrapper.emitted('CloseModal')).toHaveLength(1);
        expect(wrapper.emitted('showMessageModal')).toEqual([
            ['Sucesso', 'Usuário editado com sucesso!'],
        ]);
    });

    it('exibe a mensagem de erro retornada pela API quando a edição falha', async () => {
        axios.put.mockRejectedValue({ response: { data: { error: 'Email já utilizado por outro usuário.' } } });

        const wrapper = mountModal();
        await wrapper.setProps({ informationsUser });
        wrapper.vm.user.nome = 'Ana Souza';

        await wrapper.vm.handleSubmit();

        expect(wrapper.emitted('showMessageModal')).toEqual([
            ['Erro', 'Email já utilizado por outro usuário.'],
        ]);
        expect(wrapper.emitted('CloseModal')).toBeUndefined();
    });

    it('não envia quando a validação do formulário falha', async () => {
        const wrapper = mountModal();
        await wrapper.setProps({ informationsUser });
        wrapper.vm.user.nome = 'Ana Souza';
        wrapper.vm.$refs.form.validate = jest.fn().mockResolvedValue({ valid: false, errors: [] });

        await wrapper.vm.handleSubmit();

        expect(axios.put).not.toHaveBeenCalled();
        expect(wrapper.emitted('showMessageModal')).toEqual([
            ['Erro', 'Preencha todos os campos obrigatórios corretamente.'],
        ]);
    });
});
