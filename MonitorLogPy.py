import random
import datetime

def menu():
    nome_arq = "log.txt"
    while True:
        print("MENU\n")
        print("1 - Gerar Logs")
        print("2 - Analisar Logs")
        print("3 - Gerar e analisa logs")
        print("4 - SAIR")
        opc = int(input("Escolha uma opção: "))
        if opc == 1:
            qtd = int(input("Quantidades de logs (Registros): "))
            gerarArquivo(nome_arq, qtd)

        elif opc == 2:
            analisarLogs(nome_arq)

        elif opc == 3:
            qtd = int(input("Quantidade de logs (Registros): "))
            gerarArquivo(nome_arq, qtd)
            analisarLogs(nome_arq)

        elif opc == 4:
            print("Até Mais!")
            break
        else:
            print("Opção Inválida")


# ================= GERAÇÃO =================
def gerarArquivo(nome_arq, qtd):
    with open(nome_arq, "w", encoding="UTF-8") as arq:
        for i in range(qtd):
            arq.write(montarLog(i) + "\n")
    print("Log Gerado")


def montarLog(i):
    data = gerarData(i)
    ip = gerarIp(i)
    recurso = gerarRecurso(i)
    metodo = gerarMetodo(i)
    status = gerarStatus(i)
    tempo = gerarTempo(i)
    agente = gerarAgente(i)
    protocolo = gerarProtocolo(i)
    tamanho = gerarTamanho(i)
    return f"[{data}] {ip} - {metodo} - {status} - {recurso} - {tempo}ms - {tamanho}B - {protocolo} - {agente} - /home"


def gerarData(i):
    base = datetime.datetime.now()
    delta = datetime.timedelta(seconds=i * random.randint(5,20))
    return (base + delta).strftime("%d/%m/%Y %H:%M:%S")


def gerarIp(i):
    if i >= 20 and i <= 50:
        return "203.120.45.7"
    return f"{random.randint(10,200)}.{random.randint(10,200)}.{random.randint(10,200)}.{random.randint(10,200)}"


def gerarRecurso(i):
    if i % 10 == 0:
        return "/admin"
    elif i % 7 == 0:
        return "/login"
    elif i % 5 == 0:
        return "/backup"
    elif i % 6 == 0:
        return "/config"
    elif i % 4 == 0:
        return "/private"
    return "/home"


def gerarMetodo(i):
    if i % 7 == 0:
        return "POST"
    return "GET"


def gerarStatus(i):
    if i % 10 == 0:
        return 403
    if i % 7 == 0 and i % 3 == 0:
        return 403
    if i % 15 == 0:
        return 500
    if i % 9 == 0:
        return 404
    return 200


def gerarTempo(i):
    if i % 15 == 0:
        return random.randint(800,1500)
    return random.randint(100,900)


def gerarAgente(i):
    if i % 8 == 0:
        return "Bot"
    return "Chrome"


def gerarProtocolo(i):
    return "HTTP/1.1"


def gerarTamanho(i):
    return random.randint(100,2000)


# ================= ANÁLISE =================
def analisarLogs(nome_arq):
    arq = open(nome_arq, "r", encoding="utf-8")

    total = sucesso = erros = erro500 = 0
    somaTempo = 0
    maiorTempo = 0
    menorTempo = 999999

    rapidos = normais = lentos = 0
    status200 = status403 = status404 = status500 = 0

    recurso_home = recurso_login = recurso_admin = recurso_backup = recurso_config = recurso_private = 0

    forca_bruta = 0
    ultimo_ip_forca = ""
    admin_erro = 0
    degradacao = 0
    falha_critica = 0
    bot = 0
    ultimo_ip_bot = ""
    rotas_sensiveis = 0
    falhas_sensiveis = 0

    ip_top = ""
    ip_top_cont = 0
    ip_erro_top = ""
    ip_erro_cont = 0

    prev_ip = ""
    cont_ip = 0
    cont_ip_erro = 0

    seq_login_403 = 0
    seq_ip = 0
    prev_tempo = -1
    seq_tempo = 0
    seq_500 = 0

    for linha in arq:
        total += 1

        # IP
        ip = ""
        i = linha.find("]") + 2
        while linha[i] != " ":
            ip += linha[i]
            i += 1

        # EXTRAÇÃO (SEM TRY)
        contador = 0
        campo = ""
        status = 0
        recurso = ""
        tempo = 0

        i = 0
        while i < len(linha):
            if linha[i] == "-":
                contador += 1
                i += 2
                campo = ""
                continue

            campo += linha[i]

            if contador == 2:
                if campo.strip().isdigit():
                    status = int(campo.strip())
                else:
                    status = 0
                campo = ""

            elif contador == 3:
                recurso = campo.strip()
                campo = ""

            elif contador == 4:
                temp_str = campo.replace("ms","").strip()
                if temp_str.isdigit():
                    tempo = int(temp_str)
                else:
                    tempo = 0
                break

            i += 1

        # PROCESSAMENTO
        somaTempo += tempo

        if tempo > maiorTempo:
            maiorTempo = tempo
        if tempo < menorTempo:
            menorTempo = tempo

        if tempo < 200:
            rapidos += 1
        elif tempo < 800:
            normais += 1
        else:
            lentos += 1

        if status == 200:
            sucesso += 1
            status200 += 1
        else:
            erros += 1

        if status == 403: status403 += 1
        if status == 404: status404 += 1
        if status == 500:
            status500 += 1
            erro500 += 1

        if recurso == "/home": recurso_home += 1
        elif recurso == "/login": recurso_login += 1
        elif recurso == "/admin": recurso_admin += 1
        elif recurso == "/backup": recurso_backup += 1
        elif recurso == "/config": recurso_config += 1
        elif recurso == "/private": recurso_private += 1

        if ip == prev_ip:
            cont_ip += 1
        else:
            cont_ip = 1

        if cont_ip > ip_top_cont:
            ip_top_cont = cont_ip
            ip_top = ip

        if status != 200:
            if ip == prev_ip:
                cont_ip_erro += 1
            else:
                cont_ip_erro = 1

            if cont_ip_erro > ip_erro_cont:
                ip_erro_cont = cont_ip_erro
                ip_erro_top = ip

        if recurso == "/login" and status == 403:
            if ip == prev_ip:
                seq_login_403 += 1
                if seq_login_403 == 3:
                    forca_bruta += 1
                    ultimo_ip_forca = ip
            else:
                seq_login_403 = 1
        else:
            seq_login_403 = 0

        if ip == prev_ip:
            seq_ip += 1
            if seq_ip == 5:
                bot += 1
                ultimo_ip_bot = ip
        else:
            seq_ip = 1

        if "Bot" in linha:
            bot += 1
            ultimo_ip_bot = ip

        if recurso == "/admin" and status != 200:
            admin_erro += 1

        if recurso == "/admin" or recurso == "/backup" or recurso == "/config" or recurso == "/private":
            rotas_sensiveis += 1
            if status != 200:
                falhas_sensiveis += 1

        if prev_tempo != -1 and tempo > prev_tempo:
            seq_tempo += 1
            if seq_tempo == 3:
                degradacao += 1
        else:
            seq_tempo = 0

        if status == 500:
            seq_500 += 1
            if seq_500 == 3:
                falha_critica += 1
        else:
            seq_500 = 0

        prev_ip = ip
        prev_tempo = tempo

    arq.close()

    media = somaTempo / total
    disponibilidade = (sucesso / total) * 100
    taxaErro = (erros / total) * 100

    recurso_top = "/home"
    maior = recurso_home

    if recurso_login > maior:
        maior = recurso_login
        recurso_top = "/login"
    if recurso_admin > maior:
        maior = recurso_admin
        recurso_top = "/admin"
    if recurso_backup > maior:
        maior = recurso_backup
        recurso_top = "/backup"
    if recurso_config > maior:
        maior = recurso_config
        recurso_top = "/config"
    if recurso_private > maior:
        recurso_top = "/private"

    if falha_critica > 0 or disponibilidade < 70:
        estado = "CRÍTICO"
    elif disponibilidade < 85:
        estado = "INSTÁVEL"
    elif disponibilidade < 95 or bot > 0:
        estado = "ATENÇÃO"
    else:
        estado = "SAUDÁVEL"

    print("\n===== RELATÓRIO FINAL =====")
    print("Total de acessos:", total)
    print("Total de sucessos:", sucesso)
    print("Total de erros:", erros)
    print("Total de erros críticos:", erro500)
    print("Disponibilidade:", round(disponibilidade,2), "%")
    print("Taxa de erro:", round(taxaErro,2), "%")
    print("Tempo médio:", round(media,2))
    print("Maior tempo:", maiorTempo)
    print("Menor tempo:", menorTempo)

    print("Rápidos:", rapidos)
    print("Normais:", normais)
    print("Lentos:", lentos)

    print("Status 200:", status200)
    print("Status 403:", status403)
    print("Status 404:", status404)
    print("Status 500:", status500)

    print("Recurso mais acessado:", recurso_top)

    print("IP mais ativo:", ip_top)
    print("IP com mais erros:", ip_erro_top)

    print("Força bruta:", forca_bruta)
    print("Último IP força bruta:", ultimo_ip_forca)

    print("Acessos indevidos ao /admin:", admin_erro)
    print("Degradação de desempenho:", degradacao)
    print("Falhas críticas:", falha_critica)

    print("Suspeitas de bot:", bot)
    print("Último IP suspeito:", ultimo_ip_bot)

    print("Acessos a rotas sensíveis:", rotas_sensiveis)
    print("Falhas em rotas sensíveis:", falhas_sensiveis)

    print("Estado final do sistema:", estado)


menu()
