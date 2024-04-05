import foosball_alunos


def loadInfo(ficheiro, dicio, elemento):
    arr = ficheiro.readline().split(';')
    for i in arr:
        s = i.split(',')
        dicio[elemento].append((float(s[0]), float(s[1])))


def le_replay(nome_ficheiro):
    dicio = {
        'bola': [],
        'jogador_vermelho': [],
        'jogador_azul': []
    }

    f = open(nome_ficheiro, 'r')
    loadInfo(f, dicio, 'bola')
    loadInfo(f, dicio, 'jogador_vermelho')
    loadInfo(f, dicio, 'jogador_azul')
    f.close()

    '''
    Função que recebe o nome de um ficheiro contendo um replay, e que deverá 
    retornar um dicionário com as seguintes chaves:
    bola - lista contendo tuplos com as coordenadas xx e yy da bola
    jogador_vermelho - lista contendo tuplos com as coordenadas xx e yy da do jogador\_vermelho
    jogador_azul - lista contendo tuplos com as coordenadas xx e yy da do jogador\_azul
    '''
    return dicio


def main():
    estado_jogo = foosball_alunos.init_state()
    foosball_alunos.setup(estado_jogo, False)
    replay = le_replay('replay_golo_jv_1_ja_0.txt')
    for i in range(len(replay['bola'])):
        estado_jogo['janela'].update()

        estado_jogo['jogador_vermelho'].setpos(replay['jogador_vermelho'][i])
        estado_jogo['jogador_azul'].setpos(replay['jogador_azul'][i])
        estado_jogo['bola']['objecto'].setpos(replay['bola'][i])
    estado_jogo['janela'].exitonclick()


if __name__ == '__main__':
    main()