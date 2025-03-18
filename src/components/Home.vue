<template>
  <v-container fluid>
    <v-text-field
      class="mx-3"
      label="Pesquisar"
      clearable
    ></v-text-field>

    <v-data-table
      style="height: 100%; width: 100%;"
      :headers="headers"
      no-data-text="Nenhum usuário cadastrado"
      :items="users"
      class="border-b"
      items-per-page="10"
    >
      <template v-slot:no-data>
        <v-card-text>
          Nenhum usuário cadastrado
        </v-card-text>
      </template>
      <template v-slot:item="{ item }">
        <tr>
          <td class="w-30 text-nowrap">
            <v-icon
              @click="EditUser(item)"
              icon="mdi mdi-file-edit-outline"
              size="30"
              class="mr-2"
              style="cursor: pointer;"
            ></v-icon>
            <v-icon
              @click="DeleteUser(item.id)"
              icon="mdi mdi-delete-outline"
              size="30"
              style="cursor: pointer;"
            ></v-icon>
          </td>
          <td class="w-30 text-nowrap">{{ item.id }}</td>
          <td class="w-150 text-nowrap">{{ item.nome }}</td>
          <td class="w-200 text-nowrap">{{ item.email }}</td>
          <td class="w-150 text-nowrap">{{ item.senha }}</td>
          <td class="w-200 text-nowrap">
            {{ formatDate(item.data_criacao) }}
          </td>
          <td class="w-200 text-nowrap">
            {{ formatDate(item.data_atualizacao) }}
          </td>
        </tr>
      </template>
    </v-data-table>

    <v-btn
      color="primary"
      class="mt-3"
      block
      @click="ShowModalAddUser = true"
    >
      Cadastrar Novo Usuário
    </v-btn>
  </v-container>

  <AddUserModal :dialog="ShowModalAddUser" @CloseModal="CloseModal" />
  <EditUserModal
    :dialog="ShowModalEditUser"
    :informationsUser="informationsUser"
    @CloseModal="CloseModal"
  />
  <DeleteUserModal
    :dialog="ShowModalDeleteUser"
    :id_user="IDUserDelete"
    @CloseModal="CloseModal"
  />
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
        { title: 'Ações' },
        { title: 'ID', key: 'id' },
        { title: 'Nome', key: 'nome',},
        { title: 'Email', key: 'email' },
        { title: 'Senha', key: 'senha' },
        { title: 'Data de Criação', key: 'data_criacao' },
        { title: 'Data de Atualização', key: 'data_atualizacao' },
      ],

      users: [],
      informationsUser: {},
      ShowModalAddUser: false,
      ShowModalEditUser: false,
      ShowModalDeleteUser: false,
      IDUserDelete: null,
    };
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
        })
        .catch((error) => {
          console.error("Houve um erro ao buscar os usuários:", error);
        });
    },

    EditUser(user) {
      this.informationsUser = user;
      this.ShowModalEditUser = true;
    },

    DeleteUser(id_user) {
      this.IDUserDelete = id_user;
      this.ShowModalDeleteUser = true;
    },
  },
};
</script>

<style scoped>
.text-nowrap {
  white-space: nowrap;
}
</style>