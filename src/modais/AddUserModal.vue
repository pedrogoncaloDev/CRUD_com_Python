<template>
    <v-dialog v-model="localDialog" max-width="500px" :persistent="true">
        <v-card>
            <v-card-title>
                <span class="headline">Cadastrar Novo Usuário</span>
            </v-card-title>
            <v-card-text>
                <v-container>
                    <v-form ref="form" @submit.prevent="handleSubmit">
                        <v-row>
                            <v-col cols="12">
                                <v-text-field
                                    v-model="newUser.nome"
                                    label="Nome Completo"
                                    :rules="[rules.required]"
                                    required
                                    clearable
                                ></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field
                                    v-model="newUser.email"
                                    label="Email"
                                    :rules="[rules.required, rules.email]"
                                    required
                                    clearable
                                ></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field
                                    v-model="newUser.senha"
                                    :append-icon="ShowPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                    :type="ShowPassword ? 'text' : 'password'"
                                    label="Senha"
                                    :rules="[rules.required]"
                                    required
                                    clearable
                                    @click:append="ShowPassword = !ShowPassword"
                                ></v-text-field>
                            </v-col>
                        </v-row>
                    </v-form>
                </v-container>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="CloseModal()">Cancelar</v-btn>
                <v-btn color="blue darken-1" text type="submit" form="form" @click="handleSubmit()">Salvar</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import { API_URL } from '../utils';
import axios from 'axios';
import { validationRules } from '../validationRules';

export default {
    props: {
        dialog: Boolean
    },

    emits: ["CloseModal", "showMessageModal"],

    data() {
        return {
            newUser: { nome: '', email: '', senha: '', data_criacao: null, data_atualizacao: null },
            ShowPassword: false,
            localDialog: this.dialog,
            rules: validationRules,
        };
    },

    watch: {
        dialog(newVal) {
            this.localDialog = newVal;
        }
    },

    mounted() {
        window.addEventListener('keydown', this.handleKeydown);
    },

    beforeUnmount() {
        window.removeEventListener('keydown', this.handleKeydown);
    },


    methods: {
        CloseModal() {
            this.$emit('CloseModal');
            this.newUser = { nome: '', email: '', senha: '', data_criacao: null, data_atualizacao: null };
        },

        async handleSubmit() {
            const form_information = this.$refs.form.validate(); // Valida os campos do formulário

            if (!form_information) {
                this.$emit("showMessageModal", "Erro", "Preencha todos os campos obrigatórios corretamente.");
                return;
            }

            await this.CreateUser();
        },

        handleKeydown(event) {
            if (event.key === 'Escape' && this.localDialog) {
                this.CloseModal();
            }

            if (event.key === 'Enter' && this.localDialog) {
                this.CreateUser();
            }
        },

        async CreateUser() {
            try {
                const response = await axios.post(API_URL, this.newUser);

                if (response.status === 201) {
                    this.CloseModal();
                    this.$emit("showMessageModal", "Sucesso", "Usuário criado com sucesso!");
                } else {
                    console.error("Erro ao salvar o usuário:", response.data);
                    this.$emit("showMessageModal", "Erro", "Erro ao criar o usuário!");
                }
            } catch (error) {
                const message = error.response.data.error === undefined ? error.message : error.response.data.error;
                
                console.error("Erro ao salvar o usuário:", error);
                this.$emit("showMessageModal", "Erro", message);
            }
        },
    }
};
</script>