<template>
    <v-dialog v-model="localDialog" max-width="500px" persistent="true">
        <v-card>
            <v-card-title>
                <span class="headline">Editar Usuário</span>
            </v-card-title>
            <v-card-text>
                <v-container>
                    <v-row>
                        <v-col cols="12">
                            <v-text-field v-model="user.nome" label="Nome" required clearable></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field v-model="user.email" label="Email" required clearable></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field
                                v-model="user.senha"
                                :append-icon="ShowPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                :type="ShowPassword ? 'text' : 'password'"
                                label="Senha"
                                @click:append="ShowPassword = !ShowPassword"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field v-model="user.data_criacao" label="Data de criação" :disabled="true"></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field v-model="user.data_atualizacao" label="Data de atualização" :disabled="true"></v-text-field>
                        </v-col>
                    </v-row>
                </v-container>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="CloseModal()">Cancelar</v-btn>
                <v-btn color="blue darken-1" text @click="EditUser()">Salvar</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import { API_URL } from '../utils';
import axios from 'axios';

export default {
    props: {
        dialog: Boolean,
        informationsUser: Object
    },

    emits: ['CloseModal'],

    data() {
        return {
            user: {},
            ShowPassword: false,
            localDialog: this.dialog
        };
    },

    watch: {
        dialog(newVal) {
            this.localDialog = newVal;
        },

        informationsUser(newVal){
            this.user = newVal;
        }
    },

    methods: {
        CloseModal() {
            this.$emit('CloseModal');
        },

        async EditUser() {
            try {
                this.user.data_atualizacao = new Date().toISOString();

                const response = await axios.put(API_URL, this.user);

                if (response.status === 201) {
                    this.CloseModal();
                } else {
                    console.error("Erro ao salvar o usuário:", response.data);
                }
            } catch (error) {
                console.error("Erro ao salvar o usuário:", error);
            }
        },
    }
};
</script>