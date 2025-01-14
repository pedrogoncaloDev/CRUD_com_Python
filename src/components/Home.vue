<template>
  <v-text-field class="mx-3" label="Pesquisar" clearable></v-text-field>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      headers: [
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

    },

    EditUser(item) {
      console.log(item);
    },

    DeleteUser(item) { 
      console.log(item);
    }
  }
}
</script>

<style scoped>

</style>