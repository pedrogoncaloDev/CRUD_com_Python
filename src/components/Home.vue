<template>
  <v-container fluid>
    <v-text-field class="mx-3" label="Pesquisar" clearable></v-text-field>

    <v-data-table
      style="height: 100%; width: 100%;"
      :headers="headers" no-data-text="Nenhum usuário cadastrado" :items="users" class="border-b"
      items-per-page="10">
      <template v-slot:no-data>
        <v-card-text>
          <v-icon color="black" class=" mb-1" icon="mdi-emoticon-cool"></v-icon>
          Nenhum usuário cadastrado
        </v-card-text>
      </template>
      <template v-slot:item="{ item }">
        <tr>
          <td>
            <!-- <v-icon icon="mdi mdi-file-edit-outline" size="35" color="black" style="cursor: pointer;"></v-icon>
            <v-icon icon="mdi mdi-file-edit-outline" size="35" color="black" style="cursor: pointer;"></v-icon>
            <v-icon icon="mdi mdi-delete-outline" size="35" color="black" style="cursor: pointer;"></v-icon> -->

            <!-- <button @click="ShowModalAddUser = true;">criar</button> -->
            <button @click="EditUser(item)">editar</button>
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

    <v-btn color="primary" @click="ShowModalAddUser = true">Cadastrar Novo Usuário</v-btn>
  </v-container>

  <AddUserModal :dialog="ShowModalAddUser" @CloseModal="CloseModal" />
  <EditUserModal :dialog="ShowModalEditUser" :informationsUser="informationsUser" @CloseModal="CloseModal" />
</template>

<script>
import AddUserModal from '@/modais/AddUserModal.vue';
import EditUserModal from '@/modais/EditUserModal.vue';
import { API_URL, formatDate } from '../utils';
import axios from 'axios';

export default {
  name: 'HomePage',

  components: {
    AddUserModal,
    EditUserModal
  },

  data() {
    return {
      headers: [
        { acoes: null },
        { title: 'ID', key: 'id' },
        { title: 'Nome', key: 'nome',},
        { title: 'Email', key: 'email' },
        { title: 'Senha', key: 'senha' },
        { title: 'Data de Criação', key: 'data_criacao' },
        { title: 'Data de Atualização', key: 'data_atualizacao' },
      ],

      informationsUser: {},

      users: [],
      ShowModalAddUser: false,
      ShowModalEditUser: false
    }
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

      this.GetUsers();
    },

    GetUsers(){
      axios.get(API_URL)
      .then(response => {
        this.users = response.data;
      })
      .catch(error => {
        console.error("Houve um erro ao buscar os usuários:", error);
      });
    },

    EditUser(user){
      this.informationsUser = user; 
      this.ShowModalEditUser = true;
    }
  }
}
</script>

<style scoped>

</style>