import _sqlite3


class Visitantes:
    def __init__(self, nome, carro):
        self.nome = nome
        self.carro = carro
        self.visitante = (nome, carro)

    @staticmethod
    def cria_tabela_visitantes():
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS visitantes (Id INTEGER PRIMARY KEY "
                  " AUTOINCREMENT, Nome TEXT COLLATE NOCASE, Carro TEXT COLLATE NOCASE, "
                  "UNIQUE(Nome) ON CONFLICT ABORT);")
        conn.commit()
        conn.close()

    @staticmethod
    def add_visitante_bd():
        Visitantes.cria_tabela_visitantes()
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        nome = input("Digite o nome do visitante: ")
        carro = input("Digite o carro do visitante: ")
        visitante = Visitantes(nome, carro)
        try:  # trata a duplicidade de nomes
            c.execute("INSERT INTO visitantes VALUES(NULL,?,?)", visitante.visitante)
            conn.commit()
            print("Visitante adicionado com sucesso!")
        except _sqlite3.IntegrityError:
            print("Visitante já está cadastrado no sistema.")
        conn.close()

    @staticmethod
    def altera_visitante_bd():
        print("(1) Para alterar o nome.")
        print("(2) Para alterar o carro.")
        opcao = int(input("Digite a opcao desejada: "))
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        if opcao == 1:
            nome_anterior = (input("Digite o nome do visitante que deseja alterar: "),)
            c.execute("SELECT * FROM visitantes WHERE nome=?", nome_anterior)
            busca = c.fetchone()
            # trata o erro quando não houver nenhuma ocorrência com esses dados, nesses casos o
            # fetchone retorna None e pelas boas práticas não é correto passar None na comparação do IF
            try:
                if len(busca) > 0:
                    novo_nome = (input("Digite o novo nome do visitante: "), nome_anterior[0])
                    c.execute("UPDATE visitantes set Nome=? where Nome=?", novo_nome)
                    conn.commit()
                    print("Nome atualizado com sucesso!")
            except TypeError:
                print(f"Não foi encontrado um visitante com esse nome {nome_anterior[0]}")
        elif opcao == 2:
            nome = input("Digite o nome do visitante que deseja  alterar: ")
            carro = input("Digite o nome do carro que deseja alterar: ")
            nome_e_carro = (nome, carro)
            c.execute("SELECT * FROM visitantes WHERE nome=? and Carro=?;", nome_e_carro)
            busca = c.fetchone()
            # trata o erro quando não houver nenhuma ocorrência com esses dados, nesses casos o
            # fetchone retorna None e pelas boas práticas não é correto passar None na comparação do IF
            try:
                if len(busca) > 0:
                    novo_carro = (input("Digite o novo carro do visitante: "), nome)
                    c.execute("UPDATE visitantes set Carro=? where Nome=?", novo_carro)
                    conn.commit()
                    print("Nome atualizado com sucesso!")
            except TypeError:
                print(f"Não foi encontrado nenhum visitante com nome {nome} e carro {carro}")
        else:
            print("Opcao invalida!")
        conn.close()
