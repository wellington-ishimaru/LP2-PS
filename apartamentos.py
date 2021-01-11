import _sqlite3
from sqlite3 import Error

class Apartamentos:

    """Cria uma lista de tuplas que recebe 3 valores: a
    variavel qtde será iterada e dará o numero da vaga.
    Qtde e Bloco serão fornecidos pelo usuário, o valor
    morador será por padrão criado como "Apartamento vago"
    """
    def __init__(self, qtde, bloco):
        self.apartamentos = []
        for qtde in range(1, qtde + 1):
            bloco = bloco
            morador = "Apartamento vago"
            apto = (bloco, morador)
            self.apartamentos.append(apto)

    # mesma logica utilizada em estacionamento.py
    @staticmethod
    def cria_apt_bd():
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        qtde = int(input("Informe a quantidade de apartamentos: "))
        bloco = input("Informe o nome do bloco: ")
        ap = Apartamentos(qtde, bloco)
        try:#trata duplicidade de dados
            c.execute("CREATE TABLE IF NOT EXISTS apartamentos (Id INTEGER PRIMARY KEY"
                      " AUTOINCREMENT, Numero INT Bloco TEXT COLLATE NOCASE, Ocupante TEXT, UNIQUE (Numero, Bloco)"
                      " FOREIGN KEY (Numero) REFERENCES moradores(ID))")
            c.executemany("INSERT INTO apartamentos VALUES(null,?,?)", ap.apartamentos)
            conn.commit()
            print("Apartamentos criados com sucesso.")
        except _sqlite3.IntegrityError:
            print("Dados duplicados, não foi possível a inserção.")
        conn.close()

    @staticmethod
    def add_morador_apt():
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        bloco = (input("Digite o bloco do apartamento: "), 'Apartamento vago')
        c.execute("SELECT * FROM apartamentos WHERE bloco=? AND ocupante=?;", bloco)
        busca_apt = c.fetchone()
        if busca_apt == None:
            print("Não há apartamento disponível no momento.")
        else:
            nome = (input("Digite o nome do morador: "),)
            c.execute("SELECT * FROM moradores WHERE Nome=?", nome)
            busca_mor = c.fetchone()
            if busca_mor == None:
                print("Morador não encontrado.")
            else:
                c.execute("UPDATE apartamentos set ocupante=? where numero =?",
                          (busca_mor[1], busca_apt[0]))
                conn.commit()
                c.execute("SELECT * FROM estacionamento INNER JOIN moradores ON "
                          "estacionamento.ocupante = moradores.nome")
                print("Morador adicionado ao apartamento com sucesso")
        conn.close()

    @staticmethod
    def mostra_apt_bd():
        print("(1) Para visualizar todos.")
        print("(2) Para visualizar por blocos.")
        opcao = int(input("Digite uma opcao: "))
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        if opcao == 1:
            try:
                c.execute("SELECT * FROM apartamentos")
                busca = c.fetchall()
                if len(busca) == 0:
                    print("Não há ocorrências para busca solicitada.")
                else:
                    print("+" + "-" * 8 + "+" + "-" * 15 + "+" + "-" * 25 + "+")
                    print("|"+"{:^8}".format("Numero") + "|" + "{:^15}".format("Bloco") + "|" + "{:^25}".format("Morador") + "|")
                    print("+" + "-" * 8 + "+" + "-" * 15 + "+" + "-" * 25 + "+")
                    for item in range(len(busca)):
                        print("|"+"{:^8}".format(busca[item][0]) + "|" + "{:^15}".format(busca[item][1]) + "|" + "{:^25}".format(
                                busca[item][2]) + "|")
                        print("+" + "-" * 8 + "+" + "-" * 15 + "+" + "-" * 25 + "+")
            except _sqlite3.Error:
                print("Tabela não encontrada.")
            c.close()
        elif opcao == 2:
            try:
                bloco = input("Digite o nome do bloco: ")
                bloco = (bloco, )
                c.execute("SELECT * FROM apartamentos WHERE Bloco=?", bloco)
                busca = c.fetchall()
                if len(busca) == 0:
                    print("Não há ocorrências para busca solicitada.")
                else:
                    print("+" + "-" * 8 + "+" + "-" * 15 + "+" + "-" * 25 + "+")
                    print("|"+ "{:^8}".format("Numero") + "|" + "{:^15}".format("Bloco") + "|" + "{:^25}".format("Morador") + "|")
                    print("+"+"-"*8 +"+"+"-"*15 +"+"+"-"*25 + "+")
                    for item in range(len(busca)):
                        print("|"+ "{:^8}".format(busca[item][0]) + "|" + "{:^15}".format(busca[item][1]) + "|" + "{:^25}".format(
                                busca[item][2]) + "|")
                        print("+" + "-" * 8 + "+" + "-" * 15 + "+" + "-" * 25 + "+")
            except _sqlite3.Error:
                print("Tabela não encontrada")
        else:
            print("Opção inválida.")
        conn.close()

    @staticmethod
    def exclui_item_apto_bd():
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        numero = int(input("Informe o numero do Apartamento: "))
        bloco = input("Informe o nome do Bloco: ")
        parametro = (numero, bloco)
        # trata o erro caso ainda nenhuma tabela tenha sido criada
        try:
            c.execute("SELECT * FROM apartamentos WHERE Numero=? and Bloco=?", parametro)
            busca = c.fetchone()
            # trata o erro caso não encontre nenhum dado, o c.fetchone retorna None
            # E pelas boas práticas, não é correto passar o tipo None na comparação do If.
            try:
                if len(busca) == 0:
                    c.execute("DELETE FROM apartamentos WHERE Numero=? and Bloco =?", parametro)
                    conn.commit()
                    print("Apartamento excluído com sucesso!")
            except TypeError:
                print(f"Apartamento numero {numero} {bloco} não encontrado. "
                      f"Por favor, verifique os dados e tente novamente.")
        except Error:
            print("Não foi encontrada nenhuma tabela.")
        conn.close()



