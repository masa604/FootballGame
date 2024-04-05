#Diogo Ferreira - 2022220735
#Magda Nunes - 2022216602


import turtle as t
import functools
import random
import math
import time

LARGURA_JANELA = 1024
ALTURA_JANELA = 600
DEFAULT_TURTLE_SIZE = 40
DEFAULT_TURTLE_SCALE = 3
RAIO_JOGADOR = DEFAULT_TURTLE_SIZE / DEFAULT_TURTLE_SCALE
RAIO_BOLA = DEFAULT_TURTLE_SIZE / 2
PIXEIS_MOVIMENTO = 90
LADO_MAIOR_AREA = ALTURA_JANELA / 3
LADO_MENOR_AREA = 50
RAIO_MEIO_CAMPO = LADO_MAIOR_AREA / 4
START_POS_BALIZAS = ALTURA_JANELA / 6
BOLA_START_POS = (5, 5)
DEBOUNCE_INTERVAL = 0.5

# Limites do ambiente
limite_superior = ALTURA_JANELA / 2
limite_inferior = -ALTURA_JANELA / 2
limite_esquerdo = -LARGURA_JANELA / 2
limite_direito = LARGURA_JANELA / 2


# Funções responsáveis pelo movimento dos jogadores no ambiente.
# O número de unidades que o jogador se pode movimentar é definida pela constante
# PIXEIS_MOVIMENTO. As funções recebem um dicionário que contém o estado
# do jogo e o jogador que se está a movimentar.

def jogador_cima(estado_jogo, jogador):
    elemento = estado_jogo[jogador]
    elemento.seth(90)
    elemento.fd(PIXEIS_MOVIMENTO)


def jogador_baixo(estado_jogo, jogador):
    elemento = estado_jogo[jogador]
    elemento.seth(-90)
    elemento.fd(PIXEIS_MOVIMENTO)


def jogador_direita(estado_jogo, jogador):
    elemento = estado_jogo[jogador]
    elemento.seth(0)
    elemento.fd(PIXEIS_MOVIMENTO)


def jogador_esquerda(estado_jogo, jogador):
    elemento = estado_jogo[jogador]
    elemento.seth(180)
    elemento.fd(PIXEIS_MOVIMENTO)


def fora():
    t.forward(LARGURA_JANELA)
    t.right(90)
    t.forward(ALTURA_JANELA)
    t.right(90)


def desenha_linhas_campo():
    # campo
    t.pu()
    t.goto(limite_esquerdo, limite_superior)
    t.pd()
    t.pensize(5)
    t.color('white')
    for i in range(2):
        fora()

    # linha do meio
    t.pu()
    t.goto(0, limite_superior)
    t.pd()
    t.seth(-90)
    t.forward(ALTURA_JANELA)

    # círculo do meio
    t.pu()
    t.goto(-RAIO_MEIO_CAMPO, 0)
    t.pd()
    t.circle(RAIO_MEIO_CAMPO)

    t.pu()
    t.goto(limite_esquerdo, START_POS_BALIZAS)
    t.pd()
    t.left(90)
    t.forward(LADO_MENOR_AREA)
    t.right(90)
    t.forward(LADO_MAIOR_AREA)
    t.right(90)
    t.forward(LADO_MENOR_AREA)

    t.pu()
    t.goto(limite_direito, START_POS_BALIZAS)
    t.pd()
    t.forward(LADO_MENOR_AREA)
    t.left(90)
    t.forward(LADO_MAIOR_AREA)
    t.left(90)
    t.forward(LADO_MENOR_AREA)

    ''' Função responsável por desenhar as linhas do campo, 
    nomeadamente a linha de meio campo, o círculo central, e as balizas. '''


def criar_bola():
    posInicial_x = BOLA_START_POS[0]
    posInicial_y = BOLA_START_POS[1]

    bola = t.Turtle()
    x = random.random() * 2 - 1
    y = random.random() * 2 - 1
    bola.shape('circle')
    bola.color('black')
    bola.pu()
    bola.goto(posInicial_x, posInicial_y)

    dicio = {
        'objecto': bola,
        'direcao_x': x,
        'direcao_y': y,
        'pos_anterior': None
    }

    '''
    Função responsável pela criação da bola. 
    Deverá considerar que esta tem uma forma redonda, é de cor preta, 
    começa na posição BOLA_START_POS com uma direção aleatória. 
    Deverá ter em conta que a velocidade da bola deverá ser superior à dos jogadores. 
    A função deverá devolver um dicionário contendo 4 elementos: o objeto bola, 
    a sua direção no eixo dos xx, a sua direção no eixo dos yy, 
    e um elemento inicialmente a None que corresponde à posição anterior da mesma.
    '''
    return dicio


def cria_jogador(x_pos_inicial, y_pos_inicial, cor):
    jogador = t.Turtle()
    jogador.shape('circle')
    jogador.color(cor)
    jogador.shapesize(stretch_wid=DEFAULT_TURTLE_SCALE, stretch_len=DEFAULT_TURTLE_SCALE)
    jogador.pu()
    jogador.goto(x_pos_inicial, y_pos_inicial)

    ''' Função responsável por criar e devolver o objeto que corresponde a um jogador (um objecto Turtle). 
    A função recebe 3 argumentos que correspondem às coordenadas da posição inicial 
    em xx e yy, e a cor do jogador. A forma dos jogadores deverá ser um círculo, 
    cujo seu tamanho deverá ser definido através da função shapesize
    do módulo \texttt{turtle}, usando os seguintes parâmetros: 
    stretch_wid=DEFAULT_TURTLE_SCALE, stretch_len=DEFAULT_TURTLE_SCALE. '''
    return jogador


def init_state():
    estado_jogo = {
        'bola': None,
        'jogador_vermelho': None,
        'jogador_azul': None,
        'var': {
            'bola': [],
            'jogador_vermelho': [],
            'jogador_azul': []
        },
        'pontuacao_jogador_vermelho': 0,
        'pontuacao_jogador_azul': 0,
        'lastColisionTimer': 0
    }
    return estado_jogo


def cria_janela():
    # create a window and declare a variable called window and call the screen()
    window = t.Screen()
    window.title("Foosball Game")
    window.bgcolor("green")
    window.setup(width=LARGURA_JANELA, height=ALTURA_JANELA)
    window.tracer(0)
    return window


def cria_quadro_resultados():
    # Code for creating pen for scorecard update
    quadro = t.Turtle()
    quadro.speed(0)
    quadro.color("Blue")
    quadro.penup()
    quadro.hideturtle()
    quadro.goto(0, 260)
    quadro.write("Player A: 0\t\tPlayer B: 0 ", align="center", font=('Monaco', 24, "normal"))
    return quadro


def terminar_jogo(estado_jogo):
    golos_vermelhos = estado_jogo['pontuacao_jogador_vermelho']
    golos_azuis = estado_jogo['pontuacao_jogador_azul']
    header = 'NJogo,JogadorVermelho,JogadorAzul\n'
    fich = 'historico_resultados.csv'
    f = open(fich, 'a+')
    f.seek(0)
    s = f.readline()
    contJogos = 1
    if s.strip() != header.strip():
        f.write(header)
    else:
        for x in f:
            contJogos += 1
    linha = f"{contJogos},{golos_vermelhos},{golos_azuis}\n"
    f.write(linha)
    f.close()

    print("Adeus")
    estado_jogo['janela'].bye()
    '''
     Função responsável por terminar o jogo. Nesta função, deverá atualizar o ficheiro
     ''historico_resultados.csv'' com o número total de jogos até ao momento,
     e o resultado final do jogo. Caso o ficheiro não exista,
     ele deverá ser criado com o seguinte cabeçalho:
     NJogo,JogadorVermelho,JogadorAzul.
    '''


def setup(estado_jogo, jogar):
    janela = cria_janela()
    # Assign keys to play
    janela.listen()
    if jogar:
        janela.onkeypress(functools.partial(jogador_cima, estado_jogo, 'jogador_vermelho'), 'w')
        janela.onkeypress(functools.partial(jogador_baixo, estado_jogo, 'jogador_vermelho'), 's')
        janela.onkeypress(functools.partial(jogador_esquerda, estado_jogo, 'jogador_vermelho'), 'a')
        janela.onkeypress(functools.partial(jogador_direita, estado_jogo, 'jogador_vermelho'), 'd')
        janela.onkeypress(functools.partial(jogador_cima, estado_jogo, 'jogador_azul'), 'Up')
        janela.onkeypress(functools.partial(jogador_baixo, estado_jogo, 'jogador_azul'), 'Down')
        janela.onkeypress(functools.partial(jogador_esquerda, estado_jogo, 'jogador_azul'), 'Left')
        janela.onkeypress(functools.partial(jogador_direita, estado_jogo, 'jogador_azul'), 'Right')
        janela.onkeypress(functools.partial(terminar_jogo, estado_jogo), 'Escape')
        quadro = cria_quadro_resultados()
        estado_jogo['quadro'] = quadro
    desenha_linhas_campo()
    bola = criar_bola()
    jogador_vermelho = cria_jogador(-((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0, "red")
    jogador_azul = cria_jogador(((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0, "blue")
    estado_jogo['janela'] = janela
    estado_jogo['bola'] = bola
    estado_jogo['jogador_vermelho'] = jogador_vermelho
    estado_jogo['jogador_azul'] = jogador_azul


def update_board(estado_jogo):
    estado_jogo['quadro'].clear()
    estado_jogo['quadro'].write("Player A: {}\t\tPlayer B: {} ".format(estado_jogo['pontuacao_jogador_vermelho'],
                                                                       estado_jogo['pontuacao_jogador_azul']),
                                align="center", font=('Monaco', 24, "normal"))


def movimenta_bola(estado_jogo):
    bola = estado_jogo['bola']['objecto']

    direcao_x = estado_jogo['bola']['direcao_x']
    direcao_y = estado_jogo['bola']['direcao_y']
    angle = math.degrees(math.atan2(direcao_y, direcao_x))
    bola.seth(angle)

    estado_jogo['bola']['pos_anterior'] = bola.pos()
    bola.fd(0.5)

    '''
    Função responsável pelo movimento da bola que deverá ser feito tendo em conta a
    posição atual da bola e a direção em xx e yy.
    '''


def verifyBallColisions(estado_jogo):
    bola = estado_jogo['bola']['objecto']
    x = bola.xcor()
    y = bola.ycor()

    # Verifica colisões com as laterais
    rangeBalizas = - START_POS_BALIZAS < y < START_POS_BALIZAS
    if not rangeBalizas:  # fora do range das balizas
        if x > limite_direito:
            bola.setx(limite_direito)
            estado_jogo['bola']['direcao_x'] *= -1
        elif x < limite_esquerdo:
            bola.setx(limite_esquerdo)
            estado_jogo['bola']['direcao_x'] *= -1

    # Verifica colisões no topo e na base
    if y > limite_superior:
        bola.sety(limite_superior)
        estado_jogo['bola']['direcao_y'] *= -1
    elif y < limite_inferior:
        bola.sety(limite_inferior)
        estado_jogo['bola']['direcao_y'] *= -1


def verifyPlayerColisions(estado_jogo, nome):
    if nome == 'jogador_vermelho':
        leftLimit = limite_esquerdo
        rightLimit = 0
    else:
        leftLimit = 0
        rightLimit = limite_direito

    jogador = estado_jogo[nome]
    x = jogador.xcor()
    y = jogador.ycor()

    if x - RAIO_JOGADOR < leftLimit:
        jogador.setx(leftLimit + RAIO_JOGADOR)
    elif x + RAIO_JOGADOR > rightLimit:
        jogador.setx(rightLimit - RAIO_JOGADOR)

    if y - RAIO_JOGADOR < limite_inferior:
        jogador.sety(limite_inferior + RAIO_JOGADOR)
    elif y + RAIO_JOGADOR > limite_superior:
        jogador.sety(limite_superior - RAIO_JOGADOR)


def verifica_colisoes_ambiente(estado_jogo):
    verifyBallColisions(estado_jogo)
    verifyPlayerColisions(estado_jogo, 'jogador_vermelho')
    verifyPlayerColisions(estado_jogo, 'jogador_azul')

    '''
    Função responsável por verificar se há colisões com os limites do ambiente,
    atualizando a direção da bola. Não se esqueça de considerar que nas laterais,
    fora da zona das balizas, a bola deverá inverter a direção onde atingiu o limite.
    '''


def geraLinha(estado_jogo, nome):
    arr = estado_jogo['var'][nome]
    s = str()
    for i in arr:
        s += f"{i[0]},{i[1]};"
    s = s[0:len(s) - 1]
    s += "\n"
    return s


def geraFicheiro(estado_jogo):
    nome = f"replay_golo_jv_{estado_jogo['pontuacao_jogador_vermelho']}_ja_{estado_jogo['pontuacao_jogador_azul']}.txt"
    f = open(nome, 'w')
    f.write(geraLinha(estado_jogo, 'bola'))
    f.write(geraLinha(estado_jogo, 'jogador_vermelho'))
    f.write(geraLinha(estado_jogo, 'jogador_azul'))
    f.close()


def reiniciarJogo(estado_jogo):
    update_board(estado_jogo)
    estado_jogo['bola']['objecto'].goto(BOLA_START_POS[0], BOLA_START_POS[1])
    estado_jogo['bola']['direcao_x'] = random.random() * 2 - 1
    estado_jogo['bola']['direcao_y'] = random.random() * 2 - 1

    x = random.randint(int(limite_esquerdo + LADO_MENOR_AREA), int(-LARGURA_JANELA / 4))
    y = random.randint(int(-START_POS_BALIZAS), int(START_POS_BALIZAS))
    estado_jogo['jogador_vermelho'].goto(x, y)

    x = random.randint(int(LARGURA_JANELA / 4), int(limite_direito - LADO_MENOR_AREA))
    y = random.randint(int(-START_POS_BALIZAS), int(START_POS_BALIZAS))
    estado_jogo['jogador_azul'].goto(x, y)

    guarda_posicoes_para_var(estado_jogo)
    geraFicheiro(estado_jogo)

    estado_jogo['var']['bola'].clear()
    estado_jogo['var']['jogador_vermelho'].clear()
    estado_jogo['var']['jogador_azul'].clear()
    guarda_posicoes_para_var(estado_jogo)


def verifica_golo_jogador_vermelho(estado_jogo):
    bola = estado_jogo['bola']['objecto']
    if bola.xcor() > limite_direito:
        estado_jogo['pontuacao_jogador_vermelho'] += 1
        reiniciarJogo(estado_jogo)
    '''
    Função responsável por verificar se um determinado jogador marcou golo.
    Para fazer esta verificação poderá fazer uso das constantes:
    LADO_MAIOR_AREA e
    START_POS_BALIZAS.
    Note que sempre que há um golo, deverá atualizar a pontuação do jogador,
    criar um ficheiro que permita fazer a análise da jogada pelo VAR,
    e reiniciar o jogo com a bola ao centro.
    O ficheiro para o VAR deverá conter todas as informações necessárias
    para repetir a jogada, usando as informações disponíveis no objeto
    estado_jogo['var']. O ficheiro deverá ter o nome

    replay_golo_jv_[TotalGolosJogadorVermelho]_ja_[TotalGolosJogadorAzul].txt

    onde [TotalGolosJogadorVermelho], [TotalGolosJogadorAzul]
    deverão ser substituídos pelo número de golos marcados pelo jogador vermelho
    e azul, respectivamente. Este ficheiro deverá conter 3 linhas, estruturadas
    da seguinte forma:
    Linha 1 - coordenadas da bola;
    Linha 2 - coordenadas do jogador vermelho;
    Linha 3 - coordenadas do jogador azul;

    Em cada linha, os valores de xx e yy das coordenadas são separados por uma
    ',', e cada coordenada é separada por um ';'.
    '''


def verifica_golo_jogador_azul(estado_jogo):
    bola = estado_jogo['bola']['objecto']
    if bola.xcor() < limite_esquerdo:
        estado_jogo['pontuacao_jogador_azul'] += 1
        reiniciarJogo(estado_jogo)
    '''
    Função responsável por verificar se um determinado jogador marcou golo.
    Para fazer esta verificação poderá fazer uso das constantes:
    LADO_MAIOR_AREA e
    START_POS_BALIZAS.
    Note que sempre que há um golo, deverá atualizar a pontuação do jogador,
    criar um ficheiro que permita fazer a análise da jogada pelo VAR,
    e reiniciar o jogo com a bola ao centro.
    O ficheiro para o VAR deverá conter todas as informações necessárias
    para repetir a jogada, usando as informações disponíveis no objeto
    estado_jogo['var']. O ficheiro deverá ter o nome

    replay_golo_jv_[TotalGolosJogadorVermelho]_ja_[TotalGolosJogadorAzul].txt

    onde [TotalGolosJogadorVermelho], [TotalGolosJogadorAzul]
    deverão ser substituídos pelo número de golos marcados pelo jogador vermelho
    e azul, respectivamente. Este ficheiro deverá conter 3 linhas, estruturadas
    da seguinte forma:
    Linha 1 - coordenadas da bola;
    Linha 2 - coordenadas do jogador vermelho;
    Linha 3 - coordenadas do jogador azul;

    Em cada linha, os valores de xx e yy das coordenadas são separados por uma
    ',', e cada coordenada é separada por um ';'.
    '''


def verifica_golos(estado_jogo):
    verifica_golo_jogador_vermelho(estado_jogo)
    verifica_golo_jogador_azul(estado_jogo)


def invX(estado_jogo):
    # Inverte parcialmente a direção x
    x = estado_jogo['bola']['direcao_x']
    if x < 0:
        estado_jogo['bola']['direcao_x'] = random.random()
    elif x >= 0:
        estado_jogo['bola']['direcao_x'] = random.random() * - 1


def invY(estado_jogo):
    # Inverte parcialmente a direção y
    y = estado_jogo['bola']['direcao_y']
    if y < 0:
        estado_jogo['bola']['direcao_y'] = random.random()
    elif y >= 0:
        estado_jogo['bola']['direcao_y'] = random.random() * - 1


def verifica_toque_jogador_azul(estado_jogo):
    bola = estado_jogo['bola']['objecto']
    jogador = estado_jogo['jogador_azul']
    last = estado_jogo['lastColisionTimer']
    if jogador.distance(bola) <= DEFAULT_TURTLE_SIZE and time.time() - last > DEBOUNCE_INTERVAL:
        estado_jogo['lastColisionTimer'] = time.time()

        invX(estado_jogo)
        invY(estado_jogo)
    '''
    Função responsável por verificar se o jogador tocou na bola.
    Sempre que um jogador toca na bola, deverá mudar a direção desta.
    '''


def verifica_toque_jogador_vermelho(estado_jogo):
    bola = estado_jogo['bola']['objecto']
    jogador = estado_jogo['jogador_vermelho']
    last = estado_jogo['lastColisionTimer']
    if jogador.distance(bola) <= DEFAULT_TURTLE_SIZE and time.time() - last > DEBOUNCE_INTERVAL:
        estado_jogo['lastColisionTimer'] = time.time()

        invX(estado_jogo)
        invY(estado_jogo)
    '''
    Função responsável por verificar se o jogador tocou na bola.
    Sempre que um jogador toca na bola, deverá mudar a direção desta.
    '''


def guarda_posicoes_para_var(estado_jogo):
    estado_jogo['var']['bola'].append(estado_jogo['bola']['objecto'].pos())
    estado_jogo['var']['jogador_vermelho'].append(estado_jogo['jogador_vermelho'].pos())
    estado_jogo['var']['jogador_azul'].append(estado_jogo['jogador_azul'].pos())


def main():
    estado_jogo = init_state()
    setup(estado_jogo, True)
    t.hideturtle()
    while True:
        guarda_posicoes_para_var(estado_jogo)
        estado_jogo['janela'].update()
        if estado_jogo['bola'] is not None:
            movimenta_bola(estado_jogo)
        verifica_colisoes_ambiente(estado_jogo)
        verifica_golos(estado_jogo)
        if estado_jogo['jogador_vermelho'] is not None:
            verifica_toque_jogador_azul(estado_jogo)
        if estado_jogo['jogador_azul'] is not None:
            verifica_toque_jogador_vermelho(estado_jogo)


if __name__ == '__main__':
    main()