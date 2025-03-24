<template>
  <v-container fluid class="pa-4">
    <v-text-field
      class="mx-3 placeholder-light"
      label="Pesquisar"
      clearable
      v-model="search"
      color="primary"
    ></v-text-field>

    <v-data-table
      :headers="headers"
      :items="filteredUsers"
      no-data-text="Nenhum usuário cadastrado"
      items-per-page-text="Itens por página"
      class="elevation-1"
      items-per-page="10"
      dark
    >
      <template v-slot:no-data>
        <v-card-text>
          Nenhum usuário cadastrado
        </v-card-text>
      </template>
      <template v-slot:item="{ item }">
        <tr>
          <td>
            <v-icon
              @click="EditUser(item)"
              icon="mdi mdi-file-edit-outline"
              size="30"
              class="mr-2"
              style="cursor: pointer;"
              color="primary"
            ></v-icon>
            <v-icon
              @click="DeleteUser(item)"
              icon="mdi mdi-delete-outline"
              size="30"
              style="cursor: pointer;"
              color="error"
            ></v-icon>
          </td>
          <td>{{ item.id }}</td>
          <td>{{ item.nome }}</td>
          <td>{{ item.email }}</td>
          <td>{{ item.senha }}</td>
          <td>{{ formatDate(item.data_criacao) }}</td>
          <td>{{ formatDate(item.data_atualizacao) }}</td>
        </tr>
      </template>
    </v-data-table>

    <v-btn v-if="IsOnAPI"
      color="primary"
      class="mt-3"
      block
      @click="ShowModalAddUser = true"
    >
      Cadastrar Novo Usuário
    </v-btn>
  </v-container>

  <!-- MODAIS -->
  <AddUserModal 
    :dialog="ShowModalAddUser" 
    @CloseModal="CloseModal"
    @showMessageModal="showMessageModal"
  />

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

  <v-snackbar :color="messageModal.color" v-model="messageModal.dialog" max-width="500" :persistent="true" timer="true" timeout="4000">
    <v-card-title class="text-h5">{{ messageModal.title }}</v-card-title>
    <v-card-text>{{ messageModal.message }}</v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn text @click="messageModal.dialog = false;">Fechar</v-btn>
    </v-card-actions>
  </v-snackbar>
</template>

<script>
import AddUserModal from "@/modais/AddUserModal.vue";
import EditUserModal from "@/modais/EditUserModal.vue";
import DeleteUserModal from "@/modais/DeleteUserModal.vue";
import { API_URL, formatDate } from "../utils";
import axios from "axios";

export default {
  name: "HomePage",

  components: {
    AddUserModal,
    EditUserModal,
    DeleteUserModal,
  },

  data() {
    return {
      headers: [
        { title: "Ações" },
        { title: "ID", key: "id" },
        { title: "Nome", key: "nome" },
        { title: "Email", key: "email" },
        { title: "Senha", key: "senha" },
        { title: "Data de Criação", key: "data_criacao" },
        { title: "Data de Atualização", key: "data_atualizacao" },
      ],

      users: [],
      search: "",
      informationsUser: {},
      ShowModalAddUser: false,
      ShowModalEditUser: false,
      ShowModalDeleteUser: false,
      messageModal: {
        dialog: false,
        title: "",
        message: "",
        color: ""
      },
      IsOnAPI: false
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
          user.senha.toLowerCase().includes(searchLower) ||
          user.id.toString().includes(searchLower) ||
          formatDate(user.data_criacao).includes(searchLower) ||
          formatDate(user.data_atualizacao).includes(searchLower)
        );
      });
    },
  },

  created() {
    this.GetUsers();
  },

  methods: {
    formatDate(dateString) {
      return formatDate(dateString);
    },

    CloseModal() {
      this.ShowModalAddUser = false;
      this.ShowModalEditUser = false;
      this.ShowModalDeleteUser = false;

      this.GetUsers();
    },

    GetUsers() {
      axios
        .get(API_URL)
        .then((response) => {
          this.users = response.data;
          this.IsOnAPI = true;
        })
        .catch((error) => {
          console.error("Houve um erro ao buscar os usuários:", error);
          this.showMessageModal("Erro", "Houve um erro ao buscar os usuários!");
        });
    },

    EditUser(user) {
      this.informationsUser = user;
      this.ShowModalEditUser = true;
    },

    DeleteUser(user) {
      this.informationsUser = user;
      this.ShowModalDeleteUser = true;
    },

    showMessageModal(title, message) {
      this.messageModal.title = title;
      this.messageModal.message = message;
      this.messageModal.dialog = true;
      this.messageModal.color = title === "Sucesso" ? "success" : "error";
    },
  },
};
</script>

<style scoped>
.text-nowrap {
  white-space: nowrap;
}

.placeholder-light ::v-deep(.v-input__control::placeholder) {
  color: rgba(255, 255, 255, 0.6);
}
</style>