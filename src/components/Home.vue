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
            <v-icon @click="EditUser(item)" icon="mdi mdi-file-edit-outline" size="35" color="black" style="cursor: pointer;"></v-icon>
            <v-icon @click="DeleteUser(item)" icon="mdi mdi-delete-outline" size="35" color="black" style="cursor: pointer;"></v-icon>
          </td>
          <td>{{ item.id }}</td>
          <td>{{ item.nome }}</td>
          <td>{{ item.email }}</td>
          <td>{{ item.senha }}</td>
          <td>{{ item.data_criacao }}</td>
          <td>{{ item.data_atualizacao }}</td>
        </tr>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import { API_URL } from '../utils';
import axios from 'axios';

export default {
  name: 'HomePage',

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

      users: [],
    }
  },

  created() {
    axios.get(API_URL)
      .then(response => {
        this.users = response.data;
      })
      .catch(error => {
        console.error("Houve um erro ao buscar os usuários:", error);
      });
  },

  methods: {

  }
}
</script>

<style scoped>

</style>