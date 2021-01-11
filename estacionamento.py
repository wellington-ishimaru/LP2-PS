import _sqlite3
from _sqlite3 import Error


class Estacionamento:
    """Cria uma lista de tuplas que recebe 3 valores: a
    variavel qtde será iterada e dará o numero da vaga.
    Qtde e Bloco serão fornecidos pelo usuário, o valor
    ocupante será por padrão criado como "Estacionamento vago"
    """

    def __init__(self, qtde, bloco):
        self.estacionamento = []
        for qtde in range(1, qtde + 1):
            bloco = bloco
            ocupante = "Estacionamento vago"
            vaga = (bloco, ocupante)
            self.estacionamento.append(vaga)

    # cria uma tabela no DB para estacionamento
    @staticmethod
    def cria_est_bd():
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        qtde = int(input("Informe a quantidade de vagas: "))
        bloco = input("Informe o nome do bloco: ")
        p = Estacionamento(qtde, bloco)
        # usando o collate nocase para deixar a busca sem caps sensitive
        c.execute("CREATE TABLE IF NOT EXISTS estacionamento (Numero INTEGER PRIMARY KEY "
                  "AUTOINCREMENT, Bloco TEXT COLLATE NOCASE, Ocupante TEXT, FOREIGN KEY "
                  "(Numero) REFERENCES moradores(ID), FOREIGN KEY (Numero) REFERENCES visitantes(Id),"
                  "FOREIGN KEY(Numero) REFERENCES funcionarios(ID), UNIQUE (Numero, Bloco) ON CONFLICT"
                  " ABORT);")
        # trata a duplicidade de dados.
        try:
            c.executemany("INSERT INTO estacionamento VALUES(NULL,?,?)", p.estacionamento)
            conn.commit()
            print("Estacionamento criado com sucesso.")
        except _sqlite3.IntegrityError:
            print("Dados duplicados, não foi possivel a inserção.")
        conn.close()

    @staticmethod
    def add_pessoa_est():
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        print("(1) Estacionamento para moradores.")
        print("(2) Estacionamento para visitantes.")
        escolha = int(input("Digite uma opção: "))
        if escolha == 1:
            bloco = (input("Digite o bloco do estacionamento: "), 'Estacionamento vago')
            c.execute("SELECT * FROM estacionamento WHERE bloco=? AND ocupante=?;", bloco)
            busca_est = c.fetchone()
            # trata o erro quando não houver nenhuma ocorrência com esses dados, nesses casos o
            # fetchone retorna None e pelas boas práticas não é correto passar None na comparação do IF
            try:
                if len(busca_est) > 0:
                    nome = input("Digite o nome do morador: ")
                    carro = input("Digite o carro do morador: ")
                    nome_carro = (nome, carro)
                    c.execute("SELECT * FROM moradores WHERE Nome=? AND Carro=?", nome_carro)
                    busca_mor = c.fetchone()
                    try:
                        if len(busca_mor) > 0:
                            c.execute("UPDATE estacionamento set ocupante=? where numero =?",
                                      (f"{busca_mor[1]} - {busca_mor[2]}", busca_est[0]))
                            conn.commit()
                            print("Morador adicionado com sucesso!")
                    except TypeError:
                        print("Morador não encontrado.")
            except TypeError:
                print("Não há estacionamento disponível no momento.")
        elif escolha == 2:
            bloco = (input("Digite o bloco do estacionamento: "), 'Estacionamento vago')
            c.execute("SELECT * FROM estacionamento WHERE bloco=? AND ocupante=?;", bloco)
            busca_est = c.fetchone()
            try:
                if len(busca_est) > 0:
                    nome = input("Digite o nome do visitante: ")
                    carro = input("Digite o carro do visitante: ")
                    nome_carro = (nome, carro)
                    c.execute("SELECT * FROM visitantes WHERE Nome=? AND Carro=?", nome_carro)
                    busca_vis = c.fetchone()
                    try:
                        if len(busca_vis) > 0:
                            c.execute("UPDATE estacionamento set ocupante=? where numero =?",
                                      (f"{busca_vis[1]} - {busca_vis[2]}", busca_est[0]))
                            conn.commit()
                            print("Visitante adicionado com sucesso!")
                    except TypeError:
                        print("Visitante não encontrado.")
            except TypeError:
                print("Não há estacionamento disponível no momento.")
        else:
            print("Opção inválida.")
        conn.close()

    # exibe a tabela estacionamento inteira ou
    # filtra por bloco de acordo com a opcao do usuario
    @staticmethod
    def mostra_est_bd():
        print("(1) Para visualizar todos.")
        print("(2) Para visualizar por blocos.")
        opcao = int(input("Digite uma opcao: "))
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        if opcao == 1:
            # trata o erro caso nao encontre a tabela
            try:
                c.execute("SELECT * FROM estacionamento  ")
                busca = c.fetchall()
                # imprime uma msg caso a tabela nao possua dados
                if busca == 0:
                    print("Não há ocorrências para busca solicitada.")
                else:
                    print("+" + "-" * 8 + "+" + "-" * 15 + "+" + "-" * 25 + "+")
                    print("|" + "{:^8}".format("Numero") + "|" + "{:^15}".format("Bloco") +
                          "|"+"{:^25}".format("Ocupante") + "|")
                    print("+" + "-" * 8 + "+" + "-" * 15 + "+" + "-" * 25 + "+")
                    for item in range(len(busca)):
                        print("|" + "{:^8}".format(busca[item][0])+"|" + "{:^15}".format(busca[item][1])
                              + "|" + "{:^25}".format(busca[item][2]) + "|")
                        print("+" + "-" * 8 + "+" + "-" * 15 + "+" + "-" * 25 + "+")
            except _sqlite3.Error:
                print("Não foi encontrada nenhuma tabela.")
            c.close()
        elif opcao == 2:
            bloco = input("Digite o nome do bloco: ")
            bloco = (bloco,)
            # trata o erro caso nao encontre a tabela
            try:
                c.execute("SELECT * FROM estacionamento WHERE Bloco=? ", bloco)
                busca = c.fetchall()
                # imprime uma msg caso a tabela nao possua dados
                if len(busca) == 0:
                    print("Não há ocorrências para busca solicitada.")
                else:
                    print("+" + "-" * 8 + "+" + "-" * 15 + "+" + "-" * 25 + "+")
                    print("|" + "{:^8}".format("Numero") + "|" + "{:^15}".format("Bloco") +
                          "|" + "{:^25}".format("Ocupante") + "|")
                    print("+" + "-" * 8 + "+" + "-" * 15 + "+" + "-" * 25 + "+")
                    for item in range(len(busca)):
                        print("|"+"{:^8}".format(busca[item][0]) + "|" + "{:^15}".format(busca[item][1]) +
                              "|" + "{:^25}".format(
                                busca[item][2]) + "|")
                        print("+" + "-" * 8 + "+" + "-" * 15 + "+" + "-" * 25 + "+")
            except Error:
                print("Não foi encontrada nenhuma tabela")
            c.close()
        else:
            print("Opção invalida!")
        conn.close()

    # exclui uma linha da tabela usando os parametros numero e bloco
    @staticmethod
    def exclui_item_est_bd():
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        numero = int(input("Informe o numero da vaga: "))
        bloco = input("Informe o nome do Bloco: ")
        parametro = (numero, bloco)
        # trata o erro caso a tabela ainda não tenha sido criada
        try:
            c.execute("SELECT * FROM estacionamento WHERE numero=? and Bloco=?", parametro)
            busca = c.fetchone()
            # trata o erro quando não houver nenhuma ocorrência com esses dados, nesses casos o
            # fetchone retorna None e pelas boas práticas não é correto passar None na comparação do IF
            try:
                if len(busca) > 0:
                    c.execute("DELETE FROM estacionamento where numero=? and Bloco =?", parametro)
                    conn.commit()
                    print("Estacionamento excluído com sucesso!")
            except TypeError:
                print(f"Estacionamento numero {numero} {bloco} não encontrado. "
                      f"Por favor, verifique os dados e tente novamente.")
        except Error:
            print("Não foi encontrada nenhuma tabela")
        conn.close()
