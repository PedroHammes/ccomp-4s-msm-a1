"""
Responsável apenas pela interação do usuário via CLI
"""

# import mola_sem_atrito # a fazer
# import mola_com_atrito # a fazer
import functions # a fazer

def show_menu():
        print("\n[1] Massa e mola sem atrito\n[2] Massa e mola com atrito\n[3] Pêndulo\n[0] Sair\n")

def main():
    while True:
          show_menu()
          option = input("> ")

          match option:
                case '1': print("")#mola_sem_atrito()
                case '2': print("")#mola_com_atrito()
                case '3': functions.pendulo()
                case '0': print("Saindo...")
                case _: print("Opção inválida")

main()
