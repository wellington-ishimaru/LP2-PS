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
        bloco_est = (input("Digite o bloco do estacionamento: "), "Estacionamento vago")
        visitante = Visitantes(nome, carro)
        try:
            c.execute("SELECT * FROM estacionamento WHERE Bloco=? AND Ocupante=?", bloco_est)
            busca_est = c.fetchone()
            try:
                if len(busca_est) > 0:
                    c.execute("INSERT INTO visitantes VALUES(NULL,?,?)", visitante.visitante)
                    c.execute("UPDATE estacionamento SET ocupante=? WHERE numero=?",
                              (visitante.visitante[0], busca_est[0]))
                    conn.commit()
                    print(f"Visitante {visitante.visitante[0]} adicionado com sucesso, "
                          f"estacionamento numero:{busca_est[0]}.")
            except TypeError:
                print("Desculpe, não há vagas no momento.")
        except _sqlite3.OperationalError:
            print("Dados incorretos, tente novamente.")
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
                    c.execute("Update estacionamento set Ocupante=? where Ocupante=?", novo_nome)
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

    @staticmethod
    def mostra_visitantes():
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        try:
            c.execute("Select * from visitantes")
            busca = c.fetchall()
            if busca == 0:
                print("Não há ocorrências para busca solicitada.")
            else:
                print("+" + "-" * 8 + "+" + "-" * 15 + "+" + "-" * 15 + "+")
                print("|" + "{:^8}".format("Id") + "|" + "{:^15}".format("Nome") +
                      "|" + "{:^15}".format("Carro") + "|")
                print("+" + "-" * 8 + "+" + "-" * 15 + "+" + "-" * 15 + "+")
                for item in range(len(busca)):
                    print("|" + "{:^8}".format(busca[item][0]) + "|" + "{:^15}".format(busca[item][1])
                          + "|" + "{:^15}".format(busca[item][2]) + "|")
                    print("+" + "-" * 8 + "+" + "-" * 15 + "+" + "-" * 15 + "+")
        except _sqlite3.Error:
            print("Não foi encontrada a tabela!")

    @staticmethod
    def exclui_visitante_bd():
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        nome = input("Informe o nome do visitante: ")
        carro = input("Informe o carro do visitante: ")
        parametro = (nome, carro)
        # trata o erro caso a tabela ainda não tenha sido criada
        try:
            c.execute("SELECT * FROM visitantes WHERE Nome=? and Carro=?", parametro)
            busca = c.fetchone()
            # trata o erro caso não encontre nenhum dado, o c.fetchone retorná None
            # e pelas boas práticas, não é correto passar o tipo None na comparação do If.
            try:
                if len(busca) > 0:
                    c.execute("DELETE FROM visitantes WHERE Nome=? and Carro =?", parametro)
                    c.execute("UPDATE estacionamento SET Ocupante=? WHERE Ocupante=?",
                              ('Estacionamento vago', nome))
                    conn.commit()
                    print("Visitante excluído com sucesso!")
            except TypeError:
                print(f"Visitante nome: {nome} e carro: {carro} não encontrado.\n"
                      f"Por favor, verifique os dados e tente novamente.")
        except _sqlite3.Error:
            print("Não foi encontrada nenhuma tabela.")
        conn.close()
