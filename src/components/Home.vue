<template>
  <div>
    <v-text-field class="mx-3" label="Pesquisar" clearable></v-text-field>

    <v-data-table
      :headers="headers"
      :items="items"
      class="elevation-1 mx-3"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Users</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="AddUser">Add User</v-btn>
        </v-toolbar>
      </template>
      <template v-slot:item.action="{ item }">
        <v-btn icon @click="EditUser(item)">
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
        <v-btn icon @click="DeleteUser(item)">
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </template>
    </v-data-table>
  </div>
</template>

<script>
export default {
  name: 'HomePage',

  data() {
    return {
      headers: [
        { text: 'Actions', value: 'action', sortable: false },
        { text: 'ID', value: 'id' },
        { text: 'Nome', value: 'nome' },
        { text: 'Email', value: 'email' },
        { text: 'Senha', value: 'senha' },
        { text: 'Data de Criação', value: 'data_criacao' },
        { text: 'Data de Atualização', value: 'data_atualizacao' }
      ],
      items: [
        {
          id: 1,
          nome: 'Novo Nome',
          email: 'teste@email.com',
          senha: 'senha123',
          data_criacao: '2025-01-03T23:57:32.225Z',
          data_atualizacao: '2025-01-03T23:57:32.225Z'
        }
      ]
    }
  },
  methods: {
    AddUser() {
      // Lógica para adicionar um novo usuário
    },
    EditUser(item) {
      console.log('Edit item:', item);
      // Lógica para editar o usuário
    },
    DeleteUser(item) {
      console.log('Delete item:', item);
      // Lógica para deletar o usuário
    }
  }
}
</script>

<style scoped>
/* Estilos personalizados */
</style>