<template>
    <v-dialog v-model="localDialog" max-width="500px" :persistent="true">
        <v-card>
            <v-card-title>
                <span class="headline">Editar Usuário - {{ informationsUser.nome }} (ID: {{ informationsUser.id }}) </span>
            </v-card-title>
            <v-card-text>
                <v-container>
                    <v-form ref="form" @submit.prevent="handleSubmit">
                        <v-row>
                            <v-col cols="12">
                                <v-text-field v-model="user.nome" :rules="[rules.required]" label="Nome Completo" required clearable></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field v-model="user.email"  :rules="[rules.required, rules.email]" label="Email" required clearable></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field
                                    v-model="user.telefone"
                                    label="Telefone - (XX) XXXXX-XXXX"
                                    :rules="[rules.telefone]"
                                    clearable
                                ></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <span><strong>Data de criação:</strong> {{ formatDate(user.data_criacao) }}</span>
                            </v-col>
                            <v-col cols="12">
                                <span><strong>Data de atualização:</strong> {{ formatDate(user.data_atualizacao) }}</span>
                            </v-col>
                        </v-row>
                    </v-form>
                </v-container>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="CloseModal()">Cancelar</v-btn>
                <v-btn color="blue darken-1" text 
                    type="submit" form="form" 
                    @click="handleSubmit()" 
                    :disabled="JSON.stringify(user) === JSON.stringify(informationsUser)"
                >
                    Salvar
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import { API_URL, formatDate } from '../utils';
import axios from 'axios';
import { validationRules } from '../validationRules';

export default {
    props: {
        dialog: Boolean,
        informationsUser: Object
    },

    emits: ["CloseModal", "showMessageModal"],

    data() {
        return {
            user: {},
            localDialog: this.dialog,
            rules: validationRules,
        };
    },

    mounted() {
        window.addEventListener('keydown', this.handleKeydown);
    },

    beforeUnmount() {
        window.removeEventListener('keydown', this.handleKeydown);
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

        handleKeydown(event) {
            if (event.key === 'Escape' && this.localDialog) {
                this.CloseModal();
            }

            if (event.key === 'Enter' && this.localDialog) {
                this.handleSubmit();
            }
        },

        async handleSubmit() {
            const form_information = this.$refs.form.validate(); // Valida os campos do formulário

            if (!form_information) {
                this.$emit("showMessageModal", "Erro", "Preencha todos os campos obrigatórios corretamente.");
                return;
            }

            await this.EditUser();
        },


        async EditUser() {
            if (JSON.stringify(this.user) === JSON.stringify(this.informationsUser)){
                return
            }

            try {
                const response = await axios.put(API_URL, this.user);

                if (response.status === 201) {
                    this.CloseModal();
                    this.$emit("showMessageModal", "Sucesso", "Usuário editado com sucesso!");
                } else {
                    console.error("Erro ao salvar o usuário:", response.data);
                    this.$emit("showMessageModal", "Erro", "Erro ao editar o usuário!");
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