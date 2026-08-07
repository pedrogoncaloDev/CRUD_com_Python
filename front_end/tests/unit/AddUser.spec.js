import { mount } from '@vue/test-utils';
import axios from 'axios';
import AddUser from '../../src/components/AddUser.vue';
import { withVuetify } from './vuetify-setup';

jest.mock('axios');

function mountAddUser() {
    const wrapper = mount(AddUser, withVuetify());
    wrapper.vm.$refs.form.resetValidation = jest.fn();
    return wrapper;
}

describe('AddUser.vue', () => {
    afterEach(() => {
        jest.clearAllMocks();
    });

    it('não envia o formulário quando os campos obrigatórios são inválidos', async () => {
        const wrapper = mountAddUser();
        wrapper.vm.$refs.form.validate = jest.fn().mockResolvedValue({ valid: false, errors: [] });

        await wrapper.vm.handleSubmit();

        expect(axios.post).not.toHaveBeenCalled();
        expect(wrapper.emitted('showMessageModal')).toEqual([
            ['Erro', 'Preencha todos os campos obrigatórios corretamente.'],
        ]);
    });

    it('cria o usuário e emite os eventos de sucesso quando os dados são válidos', async () => {
        axios.post.mockResolvedValue({ status: 201 });

        const wrapper = mountAddUser();
        wrapper.vm.$refs.form.validate = jest.fn().mockResolvedValue({ valid: true, errors: [] });
        wrapper.vm.newUser = { nome: 'Ana', email: 'ana@example.com', telefone: '11987654321' };

        await wrapper.vm.handleSubmit();

        expect(axios.post).toHaveBeenCalledWith(
            expect.stringContaining('/users'),
            expect.objectContaining({ nome: 'Ana', email: 'ana@example.com' })
        );
        expect(wrapper.emitted('showMessageModal')).toEqual([
            ['Sucesso', 'Usuário criado com sucesso!'],
        ]);
        expect(wrapper.emitted('GetUsers')).toHaveLength(1);
        expect(wrapper.vm.newUser.nome).toBe('');
    });

    it('exibe a mensagem de erro retornada pela API quando a criação falha', async () => {
        axios.post.mockRejectedValue({ response: { data: { error: 'Email já utilizado por outro usuário.' } } });

        const wrapper = mountAddUser();
        wrapper.vm.$refs.form.validate = jest.fn().mockResolvedValue({ valid: true, errors: [] });
        wrapper.vm.newUser = { nome: 'Ana', email: 'ana@example.com', telefone: '11987654321' };

        await wrapper.vm.handleSubmit();

        expect(wrapper.emitted('showMessageModal')).toEqual([
            ['Erro', 'Email já utilizado por outro usuário.'],
        ]);
        expect(wrapper.emitted('GetUsers')).toBeUndefined();
    });

    it('formata o telefone digitado automaticamente', async () => {
        const wrapper = mountAddUser();

        wrapper.vm.newUser.telefone = '11987654321';
        await wrapper.vm.$nextTick();

        expect(wrapper.vm.newUser.telefone).toBe('(11) 98765-4321');
    });
});
