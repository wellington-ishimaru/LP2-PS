# LP2-PS
# Projeto Semestral desenvolvido em python com integracao com o banco de dados Sqlite3
## Sistema para condomínios com o menu inicial a seguir:
1. Estacionamento
2. Apartamentos
3. Moradores
4. Funcionarios
5. Visitantes
9. Menu
0. Sair
************************************************************************
##### As opções (1) e (2) são bem similares com relação ao funcionamento.
##### Ao optar por ela, o usuário visualiza um sub-menu, no exemplo 
##### abaixo com estacionamento:
1. Criar estacionamento.
2. Mostrar estacionamento.
3. Excluir estacionamento.
4. Adiciona usuário da vaga.

Esse sub-menu possibilita as operações básicas do CRUD, na opção (1)
O usuário pode deve fornecer a quantidade de vagas que deseja criar e
O nome bloco do estacionamento. Pode visualizar as vagas com uma tabela 
Exibida no console e excluir determinada vaga, além de adicionar um 
Usuário manualmente.
************************************************************************
##### As opções (3) e (5) também funcionam de forma semelhante entre si.
##### Exibindo um sub-menu a seguir (exemplo moradores).
1. Adicionar morador.
2. Alterar nome ou carro.
3. Mostrar moradores
4. Excluir morador.

Ao adicionar um morador, o programa ja verifica se há vaga de estacionamento
E apartamento, só então conclui o cadastro. Ao criar, alterar ou excluir]
As tabelas de apartamento e estacionamento são atualizadas automaticamente.
**************************************************************************
##### A opção (5) cuida dos dados dos funcionários, realizando também as operações 
##### bbásicas do CRUD.
**************************************************************************
##### As opções (9) e (0) retornam ao menu inicial e finalizam o 
##### programa, respectivamente.
