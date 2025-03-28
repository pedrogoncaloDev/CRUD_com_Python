<template>
    <v-dialog v-model="localDialog" @keyup.esc="CloseModal()" @keyup.enter="CreateUser()" max-width="500px" persistent="true">
        <v-card>
            <v-card-title>
                <span class="headline">Cadastrar Novo Usuário</span>
            </v-card-title>
            <v-card-text>
                <v-container>
                    <v-row>
                        <v-col cols="12">
                            <v-text-field v-model="newUser.nome" label="Nome Completo" required></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field v-model="newUser.email" label="Email" required></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field
                                v-model="newUser.senha"
                                :append-icon="ShowPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                :type="ShowPassword ? 'text' : 'password'"
                                label="Senha"
                                @click:append="ShowPassword = !ShowPassword"
                            ></v-text-field>
                        </v-col>
                    </v-row>
                </v-container>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="CloseModal()">Cancelar</v-btn>
                <v-btn color="blue darken-1" text @click="CreateUser()">Salvar</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import { API_URL } from '../utils';
import axios from 'axios';

export default {
    props: {
        dialog: Boolean
    },

    emits: ["CloseModal", "showMessageModal"],

    data() {
        return {
            newUser: {
                name: '',
                email: '',
                password: ''
            },
            ShowPassword: false,
            localDialog: this.dialog
        };
    },

    watch: {
        dialog(newVal) {
            this.localDialog = newVal;
        }
    },

    methods: {
        CloseModal() {
            this.$emit('CloseModal');
            this.newUser = { name: '', email: '', password: '' };
        },

        async CreateUser() {
            try {
                this.newUser.data_criacao = new Date().toISOString();
                this.newUser.data_atualizacao = new Date().toISOString();

                const response = await axios.post(API_URL, this.newUser);

                if (response.status === 201) {
                    this.CloseModal();
                    this.$emit("showMessageModal", "Sucesso", "Usuário criado com sucesso!");
                } else {
                    console.error("Erro ao salvar o usuário:", response.data);
                    this.$emit("showMessageModal", "Erro", "Erro ao criar o usuário!");
                }
            } catch (error) {
                console.error("Erro ao salvar o usuário:", error);
                this.$emit("showMessageModal", "Erro", error.message);
            }
        },
    }
};
</script>