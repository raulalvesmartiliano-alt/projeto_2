import random
import datetime

# Exibe o menu e chama as funções conforme a opção escolhida
def menu():
    nome_arq = 'log.txt'
    while True:
        print('Monitor LogPy')
        print('1 - Gerar logs')
        print('2 - Analisar logs')
        print('3 - Gerar e Analisar logs')
        print('4 - Sair')
        opcao = input('Escolha uma opção: ')
        if opcao == '1':
            try:
                qtd = int(input('Quantidade de logs: '))
                gerarArquivo(nome_arq, qtd)
            except:
                print('Qtd incorreta')
        elif opcao == '2':
            analisarLog(nome_arq)
        elif opcao == '3':
            try:
                qtd = int(input('Quantidade de logs: '))
                gerarArquivo(nome_arq, qtd)
                analisarLog(nome_arq)
            except:
                print('Qtd incorreta')
        elif opcao == '4':
            print('Até mais')
            break
        else:
            print('opcao errada')

# Cria o arquivo de log e escreve uma linha por vez
def gerarArquivo(nome_arq, qtd):
    with open(nome_arq, 'w', encoding='UTF-8') as arq:
        for i in range(qtd):
            arq.write(montarLog(i) + '\n')
        print('Logs gerados')

# Monta uma linha completa de log chamando cada função auxiliar
def montarLog(i):
    data = gerarDataHora(i)
    ip = gerarIp(i)
    recurso = gerarRecurso(i)
    metodo = gerarMetodo(i)
    status = gerarStatus(i)
    tempo = gerarTempo(i)
    agente = gerarAgente(i)
    return f'[{data}] {ip} - {metodo} - {status} - {recurso} - {tempo}ms - 500B - HTTP/1.1 - {agente} - /home'

# Gera a data e hora somando segundos a partir de uma data base
def gerarDataHora(i):
    base = datetime.datetime(2026, 3, 30, 22, 8, 0)
    delta = datetime.timedelta(seconds=i * random.randint(5, 20))
    return (base + delta).strftime('%d/%m/%Y %H:%M:%S')

# Retorna um IP — nas linhas 20 a 30 sempre o mesmo IP para simular força bruta
def gerarIp(i):
    r = random.randint(1, 6)

    if i >= 20 and i <= 30:
        return '200.0.111.45'

    if r == 1:
        return '192.168.5.6'
    if r == 2:
        return '192.168.5.8'
    if r == 3:
        return '192.168.5.9'
    if r == 4:
        return '192.168.25.8'
    if r == 5:
        return '192.168.45.8'
    else:
        return '192.168.65.68'

# Retorna a página acessada — faixas específicas forçam os cenários obrigatórios
def gerarRecurso(i):
    # Linhas 20-30: força bruta no /login
    if i >= 20 and i <= 30:
        return '/login'

    # Linhas 40-42: acesso indevido ao /admin
    if i >= 40 and i <= 42:
        return '/admin'

    # Rotas sensíveis em linhas fixas
    if i == 50:
        return '/backup'
    if i == 51:
        return '/config'
    if i == 52:
        return '/private'

    # Demais linhas: alterna entre páginas comuns
    r = i % 5
    if r == 0:
        return '/home'
    if r == 1:
        return '/produtos'
    if r == 2:
        return '/contato'
    if r == 3:
        return '/sobre'
    else:
        return '/carrinho'

# Retorna POST para /login e GET para todo o resto
def gerarMetodo(i):
    recurso = gerarRecurso(i)
    if recurso == '/login':
        return 'POST'
    return 'GET'

# Retorna o status HTTP conforme o cenário de cada linha
def gerarStatus(i):
    recurso = gerarRecurso(i)

    # Linhas 20-30: login falhando = 403
    if i >= 20 and i <= 30:
        return 403

    # Linhas 60-62: três erros 500 seguidos (falha crítica)
    if i >= 60 and i <= 62:
        return 500

    # Acesso ao /admin, /backup, /config ou /private = 403
    if recurso == '/admin' or recurso == '/backup' or recurso == '/config' or recurso == '/private':
        return 403

    # Página não encontrada de vez em quando
    if i % 13 == 0:
        return 404

    # Erro de servidor esporádico
    if i % 17 == 0:
        return 500

    # Caso padrão: acesso bem-sucedido
    return 200

# Retorna o tempo de resposta — linhas 70-73 sobem gradualmente (degradação)
def gerarTempo(i):
    # Degradação progressiva obrigatória
    if i == 70:
        return 120
    if i == 71:
        return 250
    if i == 72:
        return 480
    if i == 73:
        return 900

    status = gerarStatus(i)

    # Erros 500 costumam demorar mais
    if status == 500:
        return random.randint(800, 2000)

    # Demais acessos: sorteia entre rápido, normal e lento
    r = random.randint(1, 3)
    if r == 1:
        return random.randint(50, 190)    # rápido
    if r == 2:
        return random.randint(200, 799)   # normal
    else:
        return random.randint(800, 1500)  # lento

# Retorna o navegador ou bot que fez o acesso
def gerarAgente(i):
    # Linhas 80-85: Bot, linhas 86-90: Crawler
    if i >= 80 and i <= 85:
        return 'Bot'
    if i >= 86 and i <= 90:
        return 'Crawler'

    # Spider aparece de vez em quando
    if i % 23 == 0:
        return 'Spider-indexer'

    # Navegadores comuns
    r = random.randint(1, 3)
    if r == 1:
        return 'Chrome'
    if r == 2:
        return 'Firefox'
    else:
        return 'Safari'


# =============================================================
# PARTE 2 — ANÁLISE
# =============================================================

# Extrai todos os campos de uma linha sem usar split()
# Usa find() para achar os separadores e fatiamento para pegar cada trecho
def extrairCampos(linha):
    linha = linha.strip()
    campos = {}

    if len(linha) == 0:
        return campos

    # Data/hora fica entre [ e ]
    pos_abre  = linha.find('[')
    pos_fecha = linha.find(']')
    if pos_abre == -1 or pos_fecha == -1:
        return campos
    campos['data_hora'] = linha[pos_abre + 1 : pos_fecha]

    # O restante começa logo após o ]
    resto = linha[pos_fecha + 2:]
    sep = ' - '

    # Cada campo fica antes do próximo " - "
    pos = resto.find(sep)
    campos['ip'] = resto[:pos]
    resto = resto[pos + len(sep):]

    pos = resto.find(sep)
    campos['metodo'] = resto[:pos]
    resto = resto[pos + len(sep):]

    pos = resto.find(sep)
    campos['status'] = resto[:pos]
    resto = resto[pos + len(sep):]

    pos = resto.find(sep)
    campos['recurso'] = resto[:pos]
    resto = resto[pos + len(sep):]

    # Tempo vem como "120ms" — pega só os números
    pos = resto.find(sep)
    tempo_bruto = resto[:pos]
    resto = resto[pos + len(sep):]
    numeros = ''
    for c in tempo_bruto:
        if c.isdigit():
            numeros = numeros + c
    campos['tempo'] = int(numeros) if numeros != '' else 0

    # Tamanho vem como "500B" — pega só os números
    pos = resto.find(sep)
    tam_bruto = resto[:pos]
    resto = resto[pos + len(sep):]
    numeros = ''
    for c in tam_bruto:
        if c.isdigit():
            numeros = numeros + c
    campos['tamanho'] = int(numeros) if numeros != '' else 0

    pos = resto.find(sep)
    campos['protocolo'] = resto[:pos]
    resto = resto[pos + len(sep):]

    pos = resto.find(sep)
    campos['agente'] = resto[:pos]
    resto = resto[pos + len(sep):]

    # Referer é o último campo — pega o que sobrou
    campos['referer'] = resto.strip()

    return campos


# Classifica o tempo como rápido, normal ou lento
def classificarTempo(tempo):
    if tempo < 200:
        return 'rapido'
    elif tempo <= 799:
        return 'normal'
    else:
        return 'lento'


# Define o estado final do servidor com base nas métricas coletadas
def classificarEstado(disponibilidade, total_falha_critica, total_lentos, total_acessos, total_bot):
    percentual_lentos = (total_lentos / total_acessos * 100) if total_acessos > 0 else 0

    if total_falha_critica >= 1 or disponibilidade < 70:
        return 'CRITICO'
    elif disponibilidade < 85 or percentual_lentos > 30:
        return 'INSTAVEL'
    elif disponibilidade < 95 or total_bot > 0:
        return 'ATENCAO'
    else:
        return 'SAUDAVEL'


# Imprime o relatório completo na tela
def imprimirRelatorio(r):
    print('\n' + '=' * 60)
    print('       RELATORIO MONITOR LOGPY - coderslabs.com')
    print('=' * 60)

    print('\n--- VISAO GERAL ---')
    print(f"Total de acessos         : {r['total_acessos']}")
    print(f"Total de sucessos        : {r['total_sucessos']}")
    print(f"Total de erros           : {r['total_erros']}")
    print(f"Total de erros criticos  : {r['total_erros_criticos']}")
    print(f"Disponibilidade          : {r['disponibilidade']}%")
    print(f"Taxa de erro             : {r['taxa_erro']}%")

    print('\n--- DESEMPENHO ---')
    print(f"Tempo medio de resposta  : {r['tempo_medio']}ms")
    print(f"Maior tempo de resposta  : {r['maior_tempo']}ms")
    print(f"Menor tempo de resposta  : {r['menor_tempo']}ms")
    print(f"Acessos rapidos (<200ms) : {r['total_rapidos']}")
    print(f"Acessos normais (200-799): {r['total_normais']}")
    print(f"Acessos lentos (>=800ms) : {r['total_lentos']}")

    print('\n--- DISTRIBUICAO DE STATUS ---')
    print(f"Status 200 (Sucesso)     : {r['status_200']}")
    print(f"Status 403 (Negado)      : {r['status_403']}")
    print(f"Status 404 (Nao encontro): {r['status_404']}")
    print(f"Status 500 (Erro critico): {r['status_500']}")

    print('\n--- COMPORTAMENTO ---')
    print(f"Recurso mais acessado    : {r['recurso_top']}")
    print(f"IP mais ativo            : {r['ip_top']}")
    print(f"IP com mais erros        : {r['ip_erros']}")

    print('\n--- SEGURANCA ---')
    print(f"Eventos de forca bruta   : {r['total_bruta']}")
    print(f"Ultimo IP forca bruta    : {r['ultimo_ip_bruta']}")
    print(f"Acessos indevidos /admin : {r['total_admin_indevido']}")
    print(f"Suspeitas de bot         : {r['total_bot']}")
    print(f"Ultimo IP bot suspeito   : {r['ultimo_ip_bot']}")
    print(f"Acessos rotas sensiveis  : {r['total_rotas_sensiveis']}")
    print(f"Falhas em rotas sensiveis: {r['total_falhas_sensiveis']}")

    print('\n--- ESTABILIDADE ---')
    print(f"Eventos de degradacao    : {r['total_degradacao']}")
    print(f"Eventos falha critica    : {r['total_falha_critica']}")

    print('\n' + '=' * 60)
    print(f"  ESTADO FINAL DO SISTEMA: {r['estado_final']}")
    print('=' * 60 + '\n')


# Lê o arquivo de log linha por linha e calcula todas as métricas
def analisarLog(nome_arq):
    try:
        arq = open(nome_arq, 'r', encoding='UTF-8')
    except:
        print('Arquivo nao encontrado. Gere os logs primeiro.')
        return

    print('\nAnalisando logs...')

    # Contadores gerais
    total_acessos        = 0
    total_sucessos       = 0
    total_erros          = 0
    total_erros_criticos = 0
    status_403           = 0
    status_404           = 0
    soma_tempos          = 0
    maior_tempo          = 0
    menor_tempo          = 999999  # começa alto para ser substituído pelo menor real
    total_rapidos        = 0
    total_normais        = 0
    total_lentos         = 0

    # Variáveis para detectar força bruta
    total_bruta          = 0
    seq_bruta_ip         = ''   # IP atual na sequência suspeita
    seq_bruta_count      = 0    # quantas vezes seguidas esse IP tentou /login
    ultimo_ip_bruta      = ''

    # Acessos indevidos ao /admin
    total_admin_indevido = 0

    # Variáveis para detectar degradação de desempenho
    total_degradacao     = 0
    ultimo_tempo         = -1   # tempo da linha anterior
    seq_degradacao       = 0    # quantos aumentos consecutivos

    # Variáveis para detectar falha crítica (3 erros 500 seguidos)
    total_falha_critica  = 0
    seq_500              = 0

    # Variáveis para detectar bot
    total_bot            = 0
    seq_bot_ip           = ''
    seq_bot_count        = 0
    ultimo_ip_bot        = ''

    # Rotas sensíveis
    total_rotas_sensiveis  = 0
    total_falhas_sensiveis = 0

    # Dicionários para contar acessos por IP e por recurso
    ips       = {}
    ips_erros = {}
    recursos  = {}

    # Lê uma linha por vez — para quando readline() retornar ''
    linha = arq.readline()
    while linha != '':
        linha = linha.strip()

        if linha == '':
            linha = arq.readline()
            continue

        campos = extrairCampos(linha)

        if len(campos) == 0:
            linha = arq.readline()
            continue

        ip      = campos.get('ip', '')
        status  = campos.get('status', '')
        recurso = campos.get('recurso', '')
        tempo   = campos.get('tempo', 0)
        agente  = campos.get('agente', '')

        # Conta o acesso
        total_acessos = total_acessos + 1

        # Separa entre sucesso e erro
        if status == '200':
            total_sucessos = total_sucessos + 1
        else:
            total_erros = total_erros + 1

        # Conta cada tipo de status
        if status == '500':
            total_erros_criticos = total_erros_criticos + 1
        elif status == '403':
            status_403 = status_403 + 1
        elif status == '404':
            status_404 = status_404 + 1

        # Acumula tempo e atualiza maior e menor
        soma_tempos = soma_tempos + tempo
        if tempo > maior_tempo:
            maior_tempo = tempo
        if tempo < menor_tempo:
            menor_tempo = tempo

        # Classifica o tempo e incrementa o contador correspondente
        classe = classificarTempo(tempo)
        if classe == 'rapido':
            total_rapidos = total_rapidos + 1
        elif classe == 'normal':
            total_normais = total_normais + 1
        else:
            total_lentos = total_lentos + 1

        # Conta quantas vezes cada recurso foi acessado
        if recurso in recursos:
            recursos[recurso] = recursos[recurso] + 1
        else:
            recursos[recurso] = 1

        # Conta quantas vezes cada IP acessou
        if ip in ips:
            ips[ip] = ips[ip] + 1
        else:
            ips[ip] = 1

        # Conta erros por IP
        if status != '200':
            if ip in ips_erros:
                ips_erros[ip] = ips_erros[ip] + 1
            else:
                ips_erros[ip] = 1

        # Força bruta: mesmo IP + /login + 403 três ou mais vezes seguidas
        if ip == seq_bruta_ip and recurso == '/login' and status == '403':
            seq_bruta_count = seq_bruta_count + 1
            if seq_bruta_count >= 3:
                total_bruta = total_bruta + 1
                ultimo_ip_bruta = ip
        else:
            if recurso == '/login' and status == '403':
                seq_bruta_ip    = ip
                seq_bruta_count = 1
            else:
                seq_bruta_ip    = ''
                seq_bruta_count = 0

        # Acesso indevido: /admin com qualquer erro
        if recurso == '/admin' and status != '200':
            total_admin_indevido = total_admin_indevido + 1

        # Degradação: tempo subindo 3 vezes seguidas
        if ultimo_tempo != -1:
            if tempo > ultimo_tempo:
                seq_degradacao = seq_degradacao + 1
                if seq_degradacao >= 3:
                    total_degradacao = total_degradacao + 1
            else:
                seq_degradacao = 0
        ultimo_tempo = tempo

        # Falha crítica: três erros 500 seguidos
        if status == '500':
            seq_500 = seq_500 + 1
            if seq_500 >= 3:
                total_falha_critica = total_falha_critica + 1
        else:
            seq_500 = 0

        # Bot: agente suspeito ou mesmo IP cinco vezes seguidas
        agente_suspeito = 'Bot' in agente or 'Crawler' in agente or 'Spider' in agente
        if agente_suspeito:
            total_bot = total_bot + 1
            ultimo_ip_bot = ip
        else:
            if ip == seq_bot_ip:
                seq_bot_count = seq_bot_count + 1
                if seq_bot_count >= 5:
                    total_bot = total_bot + 1
                    ultimo_ip_bot = ip
            else:
                seq_bot_ip    = ip
                seq_bot_count = 1

        # Rotas sensíveis: verifica se o recurso está na lista sem usar split()
        rotas = '/admin /backup /config /private'
        if rotas.find(recurso) != -1:
            total_rotas_sensiveis = total_rotas_sensiveis + 1
            if status != '200':
                total_falhas_sensiveis = total_falhas_sensiveis + 1

        linha = arq.readline()

    arq.close()

    # Calcula as métricas finais
    disponibilidade = round((total_sucessos / total_acessos * 100), 2) if total_acessos > 0 else 0
    taxa_erro       = round((total_erros    / total_acessos * 100), 2) if total_acessos > 0 else 0
    tempo_medio     = round((soma_tempos    / total_acessos), 2)        if total_acessos > 0 else 0

    if menor_tempo == 999999:
        menor_tempo = 0

    # Acha o recurso mais acessado percorrendo o dicionário
    recurso_top     = ''
    recurso_top_qtd = 0
    for chave in recursos:
        if recursos[chave] > recurso_top_qtd:
            recurso_top_qtd = recursos[chave]
            recurso_top     = chave

    # Acha o IP com mais acessos
    ip_top     = ''
    ip_top_qtd = 0
    for chave in ips:
        if ips[chave] > ip_top_qtd:
            ip_top_qtd = ips[chave]
            ip_top     = chave

    # Acha o IP com mais erros
    ip_erros     = ''
    ip_erros_qtd = 0
    for chave in ips_erros:
        if ips_erros[chave] > ip_erros_qtd:
            ip_erros_qtd = ips_erros[chave]
            ip_erros     = chave

    # Define o estado final do sistema
    estado = classificarEstado(disponibilidade, total_falha_critica, total_lentos, total_acessos, total_bot)

    # Monta o dicionário com todos os resultados
    relatorio = {
        'total_acessos'         : total_acessos,
        'total_sucessos'        : total_sucessos,
        'total_erros'           : total_erros,
        'total_erros_criticos'  : total_erros_criticos,
        'disponibilidade'       : disponibilidade,
        'taxa_erro'             : taxa_erro,
        'tempo_medio'           : tempo_medio,
        'maior_tempo'           : maior_tempo,
        'menor_tempo'           : menor_tempo,
        'total_rapidos'         : total_rapidos,
        'total_normais'         : total_normais,
        'total_lentos'          : total_lentos,
        'status_200'            : total_sucessos,
        'status_403'            : status_403,
        'status_404'            : status_404,
        'status_500'            : total_erros_criticos,
        'recurso_top'           : recurso_top,
        'ip_top'                : ip_top,
        'ip_erros'              : ip_erros,
        'total_bruta'           : total_bruta,
        'ultimo_ip_bruta'       : ultimo_ip_bruta,
        'total_admin_indevido'  : total_admin_indevido,
        'total_degradacao'      : total_degradacao,
        'total_falha_critica'   : total_falha_critica,
        'total_bot'             : total_bot,
        'ultimo_ip_bot'         : ultimo_ip_bot,
        'total_rotas_sensiveis' : total_rotas_sensiveis,
        'total_falhas_sensiveis': total_falhas_sensiveis,
        'estado_final'          : estado,
    }

    imprimirRelatorio(relatorio)
    return relatorio


# Inicia o programa
menu()
