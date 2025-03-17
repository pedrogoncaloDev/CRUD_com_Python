<template>
    <v-dialog v-model="localDialog" max-width="500px">
        <v-card>
            <v-card-title class="headline">Confirmar Exclusão</v-card-title>
            <v-card-text>
                Tem certeza de que deseja deletar este usuário?
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="this.$emit('CloseModal');">Cancelar</v-btn>
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
            id_user: Number
        },

        emits: ['CloseModal'],

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
                console.log(`${API_URL}/${this.id_user}`);

                axios.delete(`${API_URL}/${this.id_user}`)
                    .then(() => {
                        console.log("Usuário deletado com sucesso!");
                    })
                    .catch((error) => {
                        console.error("Erro ao deletar o usuário:", error);
                    });

                this.$emit('CloseModal');
            }
        }
    };
</script>