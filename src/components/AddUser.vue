<template>
    <v-form class="mb-3" ref="form" @submit.prevent="handleSubmit">
        <v-row>
            <v-col cols="12" md="3">
                <v-text-field 
                    v-model="newUser.nome"
                    label="Nome Completo"
                    :rules="showErrors ? [rules.required] : []"
                    color="primary"
                    required
                    clearable
                    :hide-details="!showErrors"
                ></v-text-field>
            </v-col>

            <v-col cols="12" sm="6" md="3">
                <v-text-field
                    v-model="newUser.email"
                    label="Email"
                    :rules="showErrors ? [rules.required, rules.email] : []"
                    color="primary"
                    required
                    clearable
                    :hide-details="!showErrors"
                ></v-text-field>
            </v-col>

            <v-col cols="12" sm="6" md="3">
                <v-text-field
                    type="text"
                    return-masked-value
                    v-model="newUser.telefone"
                    label="Telefone"
                    :rules="showErrors ? [rules.telefone] : []"
                    color="primary"
                    clearable
                    :hide-details="!showErrors"
                ></v-text-field>
            </v-col>

            <v-col cols="12" md="3">
                <v-btn
                    color="primary"
                    class="mb-5 h-100"
                    block
                    @click="handleSubmit"
                    style="height: 56px !important;"
                >
                    Cadastrar Novo Usuário
                </v-btn>
            </v-col>
        </v-row>
    </v-form>
</template>

<script>
import { API_URL, formatPhone } from '../utils';
import axios from 'axios';
import { validationRules } from '../validationRules';

export default {
    props: {
        dialog: Boolean,

        modalDeleteIsOpen: {
            type: Boolean,
            default: false,
        },

        modalEditIsOpen: {
            type: Boolean,
            default: false,
        },
    },

    emits: ["GetUsers", "showMessageModal"],

    data() {
        return {
            newUser: { nome: '', email: '', telefone: '', data_criacao: null, data_atualizacao: null },
            rules: validationRules,
            showErrors: false
        };
    },

    watch: {
        'newUser.telefone'(newValue) {
            this.newUser.telefone = this.formatPhone(newValue);
        }
    },

    mounted() {
        window.addEventListener('keydown', this.handleKeydown);
    },

    beforeUnmount() {
        window.removeEventListener('keydown', this.handleKeydown);
    },

    methods: {
        formatPhone(phone) {
            return formatPhone(phone);
        },

        async handleSubmit() {
            this.showErrors = true;
            this.$refs.form.resetValidation();
            
            await this.$nextTick();
            
            const isValid = this.$refs.form.validate();
            
            if (!isValid) {
                this.$emit("showMessageModal", "Erro", "Preencha todos os campos obrigatórios corretamente.");
                return;
            }

            await this.CreateUser();
        },

        handleKeydown(event) {
            // Só funciona o atalho com os modais fechados
            // Se algum modal estiver aberto, não faz nada
            if (this.modalDeleteIsOpen || this.modalEditIsOpen) {
                return;
            }

            if (event.key === 'Enter') {
                this.handleSubmit();
            }
        },

        async CreateUser() {
            try {
                const response = await axios.post(API_URL, this.newUser);

                if (response.status === 201) {
                    this.$emit("showMessageModal", "Sucesso", "Usuário criado com sucesso!");
                    this.showErrors = false;
                    this.resetVariableUser();
                    this.$emit("GetUsers");
                } else {
                    console.error("Erro ao salvar o usuário:", response.data);
                    this.$emit("showMessageModal", "Erro", "Erro ao criar o usuário!");
                }
            } catch (error) {
                const message = error.response?.data?.error || error.error || "Erro ao criar usuário";
                console.error("Erro ao salvar o usuário:", error);
                this.$emit("showMessageModal", "Erro", message);
            }
        },

        resetVariableUser() {
            this.newUser = { nome: '', email: '', telefone: '', data_criacao: null, data_atualizacao: null };
        },
    }
};
</script>