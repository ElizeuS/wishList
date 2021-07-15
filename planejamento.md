# Próximos passos

* [OK] Criar o modelo de Produtos
	- Título (OB)
	- Descrição (OP)
	- Link (OP)
	- Foto (OP)

* Modelo WishList
  - User_id (stranger)
  - Product_id (Stranger)
  - Comprou/ganhou [status] (OP)
  - Privado [status] (OP)

* [DOING] Implementar os métodos de registro, atualização, leitura e deleção de produtos

* Relacionar Usuário [N:N] Produto

* Filtrar os produtos ganhos/comprados

* Criar dois endpoints que retornem produtos aleatórios de um usuário especifico e de todos os usuários

* Relacionar usuários [N:N] (Follows, Friends) {user_following_user}
	- usuário_id (self stranger) follower
	- usuário_id (self stranger) followed

## Aprender
* Docker

## Produção
* Subir para o Heroku