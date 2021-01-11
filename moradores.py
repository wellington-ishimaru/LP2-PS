import _sqlite3


class Moradores:

    def __init__(self, nome, carro):
        self.nome = nome
        self.carro = carro
        self.morador = (nome, carro)

    @staticmethod
    def cria_tabela_moradores():
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS moradores (Id INTEGER PRIMARY KEY "
                  " AUTOINCREMENT, Nome TEXT COLLATE NOCASE, Carro TEXT COLLATE NOCASE"
                  ", UNIQUE(Nome) ON CONFLICT ABORT);")
        conn.commit()
        conn.close()

    @staticmethod
    def add_morador_bd():
        Moradores.cria_tabela_moradores()
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        nome = input("Digite o nome do morador: ")
        carro = input("Digite o carro do morador: ")
        morador = Moradores(nome, carro)
        try:  # trata a duplicidade de nomes
            c.execute("INSERT INTO moradores VALUES(NULL,?,?)", morador.morador)
            conn.commit()
            print("Morador adicionado com sucesso!")
        except _sqlite3.IntegrityError:
            print("Morador já está cadastrado no sistema.")
        conn.close()

    @staticmethod
    def altera_morador_bd():
        print("(1) Para alterar o nome.")
        print("(2) Para alterar o carro.")
        opcao = int(input("Digite a opcao desejada: "))
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        if opcao == 1:
            nome_anterior = (input("Digite o nome do morador que deseja alterar: "), )
            c.execute("SELECT * FROM moradores WHERE nome=?", nome_anterior)
            busca = c.fetchone()
            # trata o erro quando não houver nenhuma ocorrência com esses dados, nesses casos o
            # fetchone retorna None e pelas boas práticas não é correto passar None na comparação do IF
            try:
                if len(busca) > 0:
                    novo_nome = (input("Digite o novo nome do morador: "), nome_anterior[0])
                    c.execute("UPDATE moradores set Nome=? where Nome=?", novo_nome)
                    c.execute("Update estacionamento set Ocupante=? where Ocupante=?", novo_nome)
                    conn.commit()
                    print("Nome atualizado com sucesso!")
            except TypeError:
                print(f"Não foi encontrado um morador com esse nome {nome_anterior[0]}")
        elif opcao == 2:
            nome = input("Digite o nome do morador que deseja  alterar: ")
            carro = input("Digite o nome do carro que deseja alterar: ")
            nome_e_carro = (nome, carro)
            c.execute("SELECT * FROM moradores WHERE nome=? and Carro=?;", nome_e_carro)
            busca = c.fetchone()
            # trata o erro quando não houver nenhuma ocorrência com esses dados, nesses casos o
            # fetchone retorna None e pelas boas práticas não é correto passar None na comparação do IF
            try:
                if len(busca) > 0:
                    novo_carro = (input("Digite o novo carro do morador: "), nome)
                    c.execute("UPDATE moradores set Carro=? where Nome=?", novo_carro)
                    conn.commit()
                    print("Nome atualizado com sucesso!")
            except TypeError:
                print(f"Não foi encontrado um morador com nome {nome} e carro {carro}")
        else:
            print("Opcao invalida!")
        conn.close()
