<template>
    <v-dialog v-model="localDialog" @keyup.esc="this.$emit('CloseModal')" @keyup.enter="confirmDelete()" max-width="500px" :persistent="true">
        <v-card>
            <v-card-title class="headline">Confirmar Exclusão</v-card-title>
            <v-card-text>
                Tem certeza de que deseja deletar este usuário?<br>
                {{ informationsUser.nome }} (ID: {{ informationsUser.id }})
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="this.$emit('CloseModal')">Cancelar</v-btn>
                <v-btn color="red darken-1" text @click="confirmDelete()">Deletar</v-btn>
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

        emits: ["CloseModal", "showMessageModal"],

        data() {
            return {
                localDialog: this.dialog
            };
        },

        watch: {
            dialog(newVal) {
                this.localDialog = newVal;
            },
        },

        methods: {
            confirmDelete() {
                axios.delete(`${API_URL}/${this.informationsUser.id}`)
                    .then(() => {
                        this.$emit("CloseModal");
                        this.$emit("showMessageModal", "Sucesso", "Usuário deletado com sucesso!");
                    })
                    .catch((error) => {
                        console.error("Erro ao deletar o usuário:", error);
                        this.$emit("showMessageModal", "Erro", "Erro ao deletar o usuário!");
                    });
            }
        }
    };
</script>