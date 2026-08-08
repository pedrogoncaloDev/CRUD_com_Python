<template>
  <v-container class="pa-4 container-user">
    <AddUser
      :modalEditIsOpen="ShowModalEditUser"
      :modalDeleteIsOpen="ShowModalDeleteUser"
      @GetUsers="GetUsers"
      @showMessageModal="showMessageModal"
    />

    <Grid
      :users="users"
      :isLoading="isLoading"
      :totalUsers="totalUsers"
      :page="page"
      :itemsPerPage="itemsPerPage"
      @CloseModal="CloseModal"
      @GetUsers="GetUsers"
      @search="Search"
      @EditUser="EditUser"
      @DeleteUser="DeleteUser"
    />
  </v-container>

  <EditUserModal
    :dialog="ShowModalEditUser"
    :informationsUser="informationsUser"
    @CloseModal="CloseModal"
    @showMessageModal="showMessageModal"
  />

  <DeleteUserModal
    :dialog="ShowModalDeleteUser"
    :informationsUser="informationsUser"
    @CloseModal="CloseModal"
    @showMessageModal="showMessageModal"
  />

  <v-snackbar :color="messageModal.color" v-model="messageModal.dialog" :persistent="true" timer="true" timeout="4000">
    {{ messageModal.message }}

    <template v-slot:actions>
      <v-btn text @click="messageModal.dialog = false;">Fechar</v-btn>
    </template>
  </v-snackbar>
</template>

<script>
import AddUser from "@/components/AddUser.vue";
import EditUserModal from "@/modais/EditUserModal.vue";
import DeleteUserModal from "@/modais/DeleteUserModal.vue";
import Grid from "@/components/Grid.vue";
import { API_URL, formatDate } from "../utils";
import axios from "axios";

export default {
  name: "HomePage",

  components: {
    AddUser,
    EditUserModal,
    DeleteUserModal,
    Grid
  },

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

      users: [],
      totalUsers: 0,
      page: 1,
      itemsPerPage: 10,
      search: "",
      informationsUser: {},
      ShowModalEditUser: false,
      ShowModalDeleteUser: false,
      messageModal: {
        dialog: false,
        message: "",
        color: ""
      },
      IsOnAPI: false,
      isLoading: false,
    };
  },

  // Não busca usuários aqui: o v-data-table-server (dentro de Grid) emite
  // "update:options" automaticamente ao montar, com a página/tamanho padrão,
  // o que já dispara GetUsers. Chamar aqui também causaria uma requisição duplicada.

  methods: {
    formatDate(dateString) {
      return formatDate(dateString);
    },

    CloseModal() {
      this.ShowModalEditUser = false;
      this.ShowModalDeleteUser = false;

      this.GetUsers();
    },

    GetUsers(options) {
      if (options) {
        this.page = options.page;
        this.itemsPerPage = options.itemsPerPage;
      }

      this.isLoading = true;

      axios
        .get(`${API_URL}/users`, {
          params: { page: this.page, per_page: this.itemsPerPage, search: this.search || undefined },
        })
        .then((response) => {
          this.users = response.data.users;
          this.totalUsers = response.data.total;
          this.IsOnAPI = true;
        })
        .catch((error) => {
          console.error("Erro ao buscar usuários:", error);

          const errorMessage = error.response?.data?.message || "Erro ao buscar os usuários.";
          this.showMessageModal("Erro", errorMessage);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    Search(term) {
      this.search = term;
      this.page = 1;
      this.GetUsers();
    },

    EditUser(user) {
      this.informationsUser = user;
      this.ShowModalEditUser = true;
    },

    DeleteUser(user) {
      this.informationsUser = user;
      this.ShowModalDeleteUser = true;
    },

    showMessageModal(status, message) {
      this.messageModal.message = message;
      this.messageModal.dialog = true;
      this.messageModal.color = status === "Sucesso" ? "success" : "error";
    },
  },
};
</script>

<style scoped>
.container-user {
  /* height: 100vh; 
  display: flex; 
  flex-direction: column; */
}
</style>