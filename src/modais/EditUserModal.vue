<template>
    <v-dialog v-model="localDialog" @keyup.esc="CloseModal()" @keyup.enter="EditUser()" max-width="500px" persistent="true">
        <v-card>
            <v-card-title>
                <span class="headline">Editar Usuário - {{ informationsUser.nome }} (ID: {{ informationsUser.id }}) </span>
            </v-card-title>
            <v-card-text>
                <v-container>
                    <v-row>
                        <v-col cols="12">
                            <v-text-field v-model="user.nome" label="Nome Completo" required clearable></v-text-field>
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
                            <span><strong>Data de criação:</strong> {{ formatDate(user.data_criacao) }}</span>
                        </v-col>
                        <v-col cols="12">
                            <span><strong>Data de atualização:</strong> {{ formatDate(user.data_atualizacao) }}</span>
                        </v-col>
                    </v-row>
                </v-container>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="CloseModal()">Cancelar</v-btn>
                <v-btn color="blue darken-1" text @click="EditUser()" :disabled="JSON.stringify(user) === JSON.stringify(informationsUser)">Salvar</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import { API_URL, formatDate } from '../utils';
import axios from 'axios';

export default {
    props: {
        dialog: Boolean,
        informationsUser: Object
    },

    emits: ["CloseModal", "showMessageModal"],

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

        informationsUser(newVal) {
            this.user = JSON.parse(JSON.stringify(newVal));
        },
    },

    methods: {
        formatDate(dateString) {
            return formatDate(dateString);
        },

        CloseModal() {
            this.$emit('CloseModal');
        },

        async EditUser() {
            if (JSON.stringify(this.user) === JSON.stringify(this.informationsUser)){
                return
            }

            try {
                this.user.data_atualizacao = new Date().toISOString();

                const response = await axios.put(API_URL, this.user);

                if (response.status === 201) {
                    this.CloseModal();
                    this.$emit("showMessageModal", "Sucesso", "Usuário editado com sucesso!");
                } else {
                    console.error("Erro ao salvar o usuário:", response.data);
                    this.$emit("showMessageModal", "Erro", "Erro ao editar o usuário!");
                }
            } catch (error) {
                console.error("Erro ao salvar o usuário:", error);
                this.$emit("showMessageModal", "Erro", error.message);
            }
        },
    }
};
</script>