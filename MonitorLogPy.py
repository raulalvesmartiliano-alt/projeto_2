import random
import datetime

def menu():
    nome_arq = 'log.txt'
    while True:
        print('MENU\n')
        print('1 - Gerar logs')
        print('2 - Analisar logs')
        print('3 - Gerar e analisar logs')
        print('4 - Sair')
        opc = int(input('Escolha uma opção: '))
        if opc == 1:
            try:
                qtd = int(input('Quantidade de Logs (registros): '))
                gerararquivos(nome_arq, qtd)
            except:
                print('Entrada inválida.')
        elif opc == 2:
            analisarLogs(nome_arq)
        elif opc == 3:
            try:
                qtd = int(input('Quantidade de Logs (registros): '))
                gerararquivos(nome_arq, qtd)
                analisarLogs(nome_arq)
            except:
                print('Entrada inválida.')
        elif opc == 4:
            print('Entrada inváida')
        else:
            print('Opção inválida')