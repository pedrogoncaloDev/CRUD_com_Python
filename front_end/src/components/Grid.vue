<template>
  <v-data-table-server
    :headers="headers"
    :items="users"
    :items-length="totalUsers"
    :loading="isLoading"
    :page="page"
    :items-per-page="itemsPerPage"
    loading-text="Carregando usuários..."
    no-data-text="Nenhum usuário cadastrado"
    :items-per-page-options="[
                              {value: 10, title: '10'},
                              {value: 25, title: '25'},
                              {value: 50, title: '50'},
                              {value: 100, title: '100'}
                            ]"
    items-per-page-text="Usuários por página"
    page-text="{0} de {1}"
    class="elevation-1 grid-table"
    item-value="id"
    dark
    @update:options="onOptionsUpdate"
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
            placeholder="Pesquise por qualquer campo (todas as páginas)"
            density="default"
            variant="underlined"
            validateOn="blur"
            color="primary"
            max-width="400"
            class="mt-4"
            outlined
            clearable
            ></v-text-field>

            <v-btn icon @click="$emit('GetUsers')" class="ml-2">
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
            <td>{{ formatPhone(item.telefone) }}</td>
            <td>{{ formatDate(item.data_criacao) }}</td>
            <td>{{ formatDate(item.data_atualizacao) }}</td>
        </tr>
      </template>
  </v-data-table-server>
</template>

<script>
import { formatDate, formatPhone } from "../utils";

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

    totalUsers: {
      type: Number,
      default: 0,
    },

    page: {
      type: Number,
      default: 1,
    },

    itemsPerPage: {
      type: Number,
      default: 10,
    },
  },

  emits: ["EditUser", "DeleteUser", "GetUsers", "search"],

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
      searchDebounceTimer: null,
    };
  },

  watch: {
    search(newValue) {
      clearTimeout(this.searchDebounceTimer);

      this.searchDebounceTimer = setTimeout(() => {
        this.$emit("search", (newValue || "").trim());
      }, 400);
    },
  },

  methods: {
    formatDate(dateString) {
      return formatDate(dateString);
    },

    formatPhone(phone) {
      return formatPhone(phone);
    },

    onOptionsUpdate({ page, itemsPerPage }) {
      this.$emit("GetUsers", { page, itemsPerPage });
    },
  },
};
</script>

<style scoped>
.grid-table {
  flex: 1;
  overflow: auto;
  min-height: 400px;
}

.action-buttons {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
</style>
