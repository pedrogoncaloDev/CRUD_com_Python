<template>
    <v-data-table
        :headers="headers"
        :items="filteredUsers"
        :loading="isLoading"
        loading-text="Carregando usuários..."
        no-data-text="Nenhum usuário cadastrado"
        items-per-page-text="Itens por página"
        class="elevation-1"
        items-per-page="50"
        item-value="id"
        dark
    >
        <template v-slot:no-data>
        <v-card-text>
            Nenhum usuário encontrado
        </v-card-text>
        </template>

        <template v-slot:top>
        <v-toolbar flat>
            <v-toolbar-title class="d-flex align-start">Usuários</v-toolbar-title>
            <v-text-field
            v-model="search"
            label="Pesquisar"
            density="default"
            variant="underlined"
            validateOn="blur"
            color="primary"
            max-width="400"
            class="mt-4"
            outlined
            clearable
            ></v-text-field>

            <v-btn icon @click="GetUsers()" class="ml-2">
            <v-icon>mdi-reload</v-icon>
            </v-btn>
        </v-toolbar>
        </template>

        <template v-slot:item="{ item }">
        <tr>
            <td class="action-buttons">
              <v-icon
                  @click="$emit('EditUser', item)"
                  icon="mdi mdi-file-edit-outline"
                  size="30"
                  class="mr-2"
                  style="cursor: pointer;"
                  color="primary"
              ></v-icon>
              <v-icon
                  @click="$emit('DeleteUser', item)"
                  icon="mdi mdi-delete-outline"
                  size="30"
                  style="cursor: pointer;"
                  color="error"
              ></v-icon>
            </td>
            <td>{{ item.id }}</td>
            <td>{{ item.nome }}</td>
            <td>{{ item.email }}</td>
            <td>{{ item.telefone }}</td>
            <td>{{ formatDate(item.data_criacao) }}</td>
            <td>{{ formatDate(item.data_atualizacao) }}</td>
        </tr>
        </template>
    </v-data-table>
</template>

<script>
import { formatDate } from "../utils";

export default {
  name: "GridComponent",

  props: {
    users: {
      type: Array,
      default: () => [],
    },

    isLoading: {
      type: Boolean,
      default: false,
    },
  },

  emits: ["EditUser", "DeleteUser"],

  data() {
    return {
      headers: [
        { title: "Ações" },
        { title: "ID", key: "id" },
        { title: "Nome Completo", key: "nome" },
        { title: "Email", key: "email" },
        { title: "Telefone", key: "telefone" },
        { title: "Data de Criação", key: "data_criacao" },
        { title: "Data de Atualização", key: "data_atualizacao" },
      ],
      search: "",
    };
  },

  computed: {
    filteredUsers() {
      if (!this.search) {
        return this.users;
      }

      const searchLower = this.search.toLowerCase();
      return this.users.filter((user) => {
        return (
          user.nome.toLowerCase().includes(searchLower) ||
          user.email.toLowerCase().includes(searchLower) ||
          user.telefone.toLowerCase().includes(searchLower) ||
          user.id.toString().includes(searchLower) ||
          formatDate(user.data_criacao).includes(searchLower) ||
          formatDate(user.data_atualizacao).includes(searchLower)
        );
      });
    },
  },

  methods: {
    formatDate(dateString) {
      return formatDate(dateString);
    },
  },
};
</script>
