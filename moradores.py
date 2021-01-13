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
        bloco_apt = (input("Digite o bloco do apartamento: "), "Apartamento vago")
        bloco_est = (input("Digite o bloco do estacionamento: "), "Estacionamento vago")
        morador = Moradores(nome, carro)
        try:
            c.execute("SELECT * FROM apartamentos WHERE Bloco=? AND Ocupante=?", bloco_apt)
            busca_apt = c.fetchone()
            c.execute("SELECT * FROM estacionamento WHERE Bloco=? AND Ocupante=?", bloco_est)
            busca_est = c.fetchone()
            try:
                if len(busca_apt) > 0 and len(busca_est) > 0:
                    c.execute("INSERT INTO moradores VALUES(NULL,?,?)", morador.morador)
                    c.execute("UPDATE apartamentos SET ocupante=? WHERE numero=?", (morador.morador[0], busca_apt[0]))
                    c.execute("UPDATE estacionamento SET ocupante=? WHERE numero=?", (morador.morador[0], busca_est[0]))
                    conn.commit()
                    print(f"Morador {morador.morador[0]} adicionado com sucesso! Apartamento numero:{busca_apt[0]} "
                          f"Estacionamento numero:{busca_est[0]}.")
            except TypeError:
                print("Desculpe, não há vagas no momento.")
        except _sqlite3.OperationalError:
            print("Dados incorretos, tente novamente.")
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
                    c.execute("Update apartamentos set Ocupante=? where Ocupante=?", novo_nome)
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

    @staticmethod
    def mostra_moradores():
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        try:
            c.execute("Select * from moradores")
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
    def exclui_morador_bd():
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        nome = input("Informe o nome do morador: ")
        carro = input("Informe o carro do morador: ")
        parametro = (nome, carro)
        # trata o erro caso a tabela ainda não tenha sido criada
        try:
            c.execute("SELECT * FROM moradores WHERE Nome=? and Carro=?", parametro)
            busca = c.fetchone()
            print(busca)
            # trata o erro caso não encontre nenhum dado, o c.fetchone retorná None
            # e pelas boas práticas, não é correto passar o tipo None na comparação do If.
            try:
                if len(busca) > 0:
                    c.execute("DELETE FROM moradores WHERE Nome=? and Carro =?", parametro)
                    c.execute("UPDATE estacionamento set Ocupante=? where Ocupante=?",
                              ('Estacionamento vago', nome))
                    c.execute("UPDATE apartamentos set Ocupante=? where Ocupante=?",
                              ('Apartamento vago', nome))
                    conn.commit()
                    print("Morador excluído com sucesso!")
            except TypeError:
                print(f"Morador nome: {nome} e carro: {carro} não encontrado.\n"
                      f"Por favor, verifique os dados e tente novamente.")
        except _sqlite3.Error:
            print("Não foi encontrada nenhuma tabela.")
        conn.close()
