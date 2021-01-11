import _sqlite3
from _sqlite3 import Error

class Funcionario:
    def __init__(self, nome, cargo, carro):
        self.nome = nome
        self.cargo = cargo
        self.carro = carro
        self.funcionario = (nome, cargo, carro)

    @staticmethod
    def cria_tabela_funcionarios():
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS funcionarios (Id INTEGER PRIMARY KEY "
                  " AUTOINCREMENT, Nome TEXT COLLATE NOCASE, Cargo TEXT COLLATE NOCASE,"
                  " Carro TEXT COLLATE NOCASE, UNIQUE(Nome, Cargo) ON CONFLICT ABORT);")
        conn.commit()
        conn.close()

    @staticmethod
    def add_funcionario_bd():
        Funcionario.cria_tabela_funcionarios()
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        nome = input("Digite o nome do funcionario: ")
        cargo = input("Digite o cargo do funcionario: ")
        carro = input("Digite o carro do funcionario: ")
        funcionario = Funcionario(nome, cargo, carro)
        try:  # trata a duplicidade de nomes
            c.execute("INSERT INTO funcionarios VALUES(NULL,?,?,?)", funcionario.funcionario)
            conn.commit()
            print("Funcionário adicionado com sucesso!")
        except _sqlite3.IntegrityError:
            print("Funcionário já está cadastrado no sistema.")
        conn.close()

    @staticmethod
    def altera_funcionario_bd():
        print("(1) Para alterar o nome.")
        print("(2) Para alterar o cargo.")
        print("(3) Para alterar o carro.")
        opcao = int(input("Digite a opcao desejada: "))
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        if opcao == 1:
            nome_anterior = (input("Digite o nome do funcionario que deseja alterar: "), )
            c.execute("SELECT * FROM funcionarios WHERE nome=?", nome_anterior)
            busca = c.fetchone()
            if busca == None:
                print(f"Não foi encontrado um morador com esse nome {nome_anterior}")
            else:
                novo_nome = (input("Digite o novo nome do funcionário: "), nome_anterior[0])
                c.execute("UPDATE funcionarios set Nome=? where Nome=?", novo_nome)
                conn.commit()
                print("Nome atualizado com sucesso!")
        elif opcao == 2:
            nome = input("Digite o nome do funcionário que deseja  alterar: ")
            cargo = input("Digite o cargo atual que deseja alterar: ")
            nome_e_cargo = (nome, cargo)
            c.execute("SELECT * FROM funcionarios WHERE nome=? and Cargo=?;", nome_e_cargo)
            busca = c.fetchone()
            if busca == None:
                print(f"Não foi encontrado um funcionário com nome {nome} e cargo {cargo}")
            else:
                novo_cargo = (input("Digite o novo cargo do funcionário: "), nome)
                c.execute("UPDATE funcionarios set Cargo=? where Nome=?", novo_cargo)
                conn.commit()
                print("Cargo atualizado com sucesso!")
        elif opcao == 3:
            nome = input("Digite o nome do funcionário que deseja  alterar: ")
            carro = input("Digite o nome do carro atual que deseja alterar: ")
            nome_e_carro = (nome, carro)
            c.execute("SELECT * FROM funcionarios WHERE nome=? and Carro=?;", nome_e_carro)
            busca = c.fetchone()
            if busca == None:
                print(f"Não foi encontrado um funcionário com nome {nome} e carro {carro}")
            else:
                novo_carro = (input("Digite o novo carro do funcionário: "), nome)
                c.execute("UPDATE funcionarios set Carro=? where Nome=?", novo_carro)
                conn.commit()
                print("Carro atualizado com sucesso!")
        else:
            print("Opcao invalida!")
        conn.close()

    @staticmethod
    def exclui_funcionario_bd():
        conn = _sqlite3.connect("Condominio.db")
        c = conn.cursor()
        nome = input("Informe o nome do funcionário: ")
        cargo = input("Informe o cargo do funcionário: ")

        conn.commit()
        parametro = (nome, cargo)
        # trata o erro caso a tabela ainda não tenha sido criada
        try:
            c.execute("SELECT * FROM funcionarios WHERE Nome=? and Cargo=?", parametro)
            busca = c.fetchone()
            print(busca)
            # trata o erro caso não encontre nenhum dado, o c.fetchone retorná None
            # e pelas boas práticas, não é correto passar o tipo None na comparação do If.
            try:
                if len(busca) == 0:
                    c.execute("DELETE FROM funcionarios WHERE Nome=? and cargo =?", parametro)
                    conn.commit()
                    print("Funcionário excluído com sucesso!")
            except TypeError:
                print(f"Funcionário nome: {nome} e cargo: {cargo} não encontrado.\n"
                      f"Por favor, verifique os dados e tente novamente.")
        except Error:
            print("Não foi encontrada nenhuma tabela.")
        conn.close()

