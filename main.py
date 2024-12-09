import pygame
import os


# constantes de tamanho da tela
TELA_LARGURA = 500
TELA_ALTURA = 800

# constantes de imagens
IMG_BACKGROUND = pygame.image.load(os.path.join('img', 'background.png'))
IMG_TANQUE_LEFT = pygame.image.load(os.path.join('img', 'tanque_left.png'))
IMG_TANQUE_RIGHT = pygame.image.load(os.path.join('img', 'tanque_right.png'))
IMG_CANO_LEFT = pygame.image.load(os.path.join('img', 'cano_left.png'))
IMG_CANO_RIGHT = pygame.image.load(os.path.join('img', 'cano_right.png'))
IMG_BALA = pygame.image.load(os.path.join('img', 'bala.png'))
IMG_NUVEM = pygame.image.load(os.path.join('img', 'nuvem.png'))
IMG_NUVEM_ARAMIS = pygame.image.load(os.path.join('img', 'nuvem_aramis.png'))
IMG_MURO = pygame.image.load(os.path.join('img', 'muro.png'))
IMG_CORACAO = pygame.image.load(os.path.join('img', 'coracao.png'))
IMG_CORACAO_VAZIO = pygame.image.load(os.path.join('img', 'coracao_vazio.png'))
IMG_BOOM = pygame.image.load(os.path.join('img', 'boom.png'))
IMG_BOOM_FINAL = pygame.image.load(os.path.join('img', 'boom.png'))

# altura do chão para colisão
ALTURA_CHAO = 200

# definir uma fonte para os textos
pygame.font.init()
FONTE = pygame.font.SysFont('stencil', 50)


class Tanque:
    def __init__(self, pos_x, lado, cano):
        self.x = pos_x
        self.y = ALTURA_CHAO
        self.cano = cano
        self.imagem = IMG_TANQUE_LEFT if lado == 'l' else IMG_TANQUE_RIGHT


class Cano:
    def __init__(self, lado, angulo):
        self.imagem = IMG_CANO_LEFT if lado == 'l' else IMG_CANO_RIGHT


class Bala:
    pass


class Nuvem:
    pass


class Muro:
    def __init__(self):
        self.x = TELA_LARGURA / 2


def desenhar_tela(tela, muro: Muro, nuvens: list[Nuvem], tanque_left: Tanque, tanque_right: Tanque, balas: list[Bala]):
    # background
    tela.blit(IMG_BACKGROUND, (0, 0))
    # muro
    muro.desenhar(tela)
    # nuvens
    for nuvem in nuvens:
        nuvem.desenhar(tela)
    # tanques
    tanque_left.desenhar(tela)
    tanque_right.desenhar(tela)
    # balas
    for bala in balas:
        bala.desenhar()
    # atualizar a tela
    pygame.display.update()


def main():
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    muro = Muro()
    nuvens = [Nuvem()]
    tanque_left = Tanque()
    tanque_right = Tanque()
    balas = []
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        # interações pelo teclado
        for evento in pygame.event.get():
            # se fechar a janela do jogo
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_d:
                    tanque_left.mover(direcao='r')
                if evento.key == pygame.K_a:
                    tanque_left.mover(direcao='l')
                if evento.key == pygame.K_SPACE:
                    tanque_left.atirar()

                if evento.key == pygame.K_RIGHT:
                    tanque_right.mover(direcao='r')
                if evento.key == pygame.K_LEFT:
                    tanque_right.mover(direcao='l')
                if evento.key == pygame.K_RSHIFT:
                    tanque_right.atirar()

        # movendo os componentes da tela
        for bala in balas:
            bala.mover()

        # TODO lógica de adição, movimentação e remoção das nuvens
        for nuvem in nuvens:
            nuvem.mover()

        # desenhando a tela
        desenhar_tela(tela, muro, nuvens, tanque_left, tanque_right, balas)


if __name__ == '__main__':
    main()
