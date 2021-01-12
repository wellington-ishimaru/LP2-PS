from estacionamento import Estacionamento
from apartamentos import Apartamentos
from moradores import Moradores
from funcionario import Funcionario
from visitantes import Visitantes


def imprime_menu():
    print("\n****************************************")
    print("***Bem vindo ao sistema de Condomínio***")
    print("****************************************\n")
    print("(1) Estacionamento")
    print("(2) Apartamentos")
    print("(3) Moradores")
    print("(4) Funcionarios")
    print("(5) Visitantes")
    print("(9) Menu")
    print("(0) Sair\n")


def pega_opcao():
    try:
        opcao = int(input("Digite a opcao desejada: "))
        while opcao != 0:
            if opcao == 1:
                print("(1) Criar estacionamento.")
                print("(2) Mostrar estacionamento.")
                print("(3) Excluir estacionamento.")
                print("(4) Adiciona usuário da vaga.")
                sub_opcao = int(input("Digite a opcao desejada: "))
                if sub_opcao == 1:
                    Estacionamento.cria_est_bd()
                elif sub_opcao == 2:
                    Estacionamento.mostra_est_bd()
                elif sub_opcao == 3:
                    Estacionamento.exclui_item_est_bd()
                elif sub_opcao == 4:
                    Estacionamento.add_pessoa_est()
                else:
                    print("Opcao inválida")
            elif opcao == 2:
                print("(1) Criar apartamentos.")
                print("(2) Mostrar apartamentos.")
                print("(3) Excluir apartamento.")
                print("(4) Adiciona morador.")
                sub_opcao = int(input("Digite a opcao desejada: "))
                if sub_opcao == 1:
                    Apartamentos.cria_apt_bd()
                elif sub_opcao == 2:
                    Apartamentos.mostra_apt_bd()
                elif sub_opcao == 3:
                    Apartamentos.exclui_item_apto_bd()
                elif sub_opcao == 4:
                    Apartamentos.add_morador_apt()
                else:
                    print("Opção inválida!")
            elif opcao == 3:
                print("(1)Adicionar morador.")
                print("(2)Alterar nome ou carro.")
                print("(3)Excluir morador.")
                sub_opcao = int(input("Digite a opcao desejada: "))
                if sub_opcao == 1:
                    Moradores.add_morador_bd()
                elif sub_opcao == 2:
                    Moradores.altera_morador_bd()
                elif sub_opcao == 3:
                    Moradores.exclui_morador_bd()
                else:
                    print("Opção inválida!")
            elif opcao == 4:
                print("(1)Adicionar funcionário.")
                print("(2)Alterar funcionário.")
                print("(3)Excluir funcionário.")
                sub_opcao = int(input("Digite a opcao desejada: "))
                if sub_opcao == 1:
                    Funcionario.add_funcionario_bd()
                elif sub_opcao == 2:
                    Funcionario.altera_funcionario_bd()
                elif sub_opcao == 3:
                    Funcionario.exclui_funcionario_bd()
                else:
                    print("Opção Inválida!")
            elif opcao == 5:
                print("(1)Adicionar visitante.")
                print("(2)Alterar nome ou carro.")
                print("(3)Excluir visitante.")
                sub_opcao = int(input("Digite a opcao desejada: "))
                if sub_opcao == 1:
                    Visitantes.add_visitante_bd()
                elif sub_opcao == 2:
                    Visitantes.altera_visitante_bd()
                elif sub_opcao == 3:
                    Visitantes.exclui_visitante_bd()
                else:
                    print("Opção inválida!")
            elif opcao == 9:
                imprime_menu()
            else:
                print("Opcao Invalida!")
            opcao = int(input("Digite a opcao desejada ou (9) para Menu: "))
    except ValueError:
        print("\nDigito inválido, use apenas números.")
        imprime_menu()
        pega_opcao()
    print("Muito obrigado e até breve!")


# inicia o programa
imprime_menu()
pega_opcao()
