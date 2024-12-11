import pygame
import os
import random


# inicializando o pygame e colocando título na janela
pygame.init()
pygame.display.set_caption('Clash of Tanks')

# constantes de tamanho da tela
TELA_LARGURA = 1400
TELA_ALTURA = 800

# constantes de dimensões de imagem
DIM_TANQUE = (100, 50)
DIM_CANO = (80, 110)
DIM_MURO = (50, 140)
DIM_FENO = (50, 50)
DIM_NUVEM = (110, 75)
DIM_BALA = (50, 50)

# constantes de imagens
IMG_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('img', 'background.png')), (TELA_LARGURA, TELA_ALTURA))
IMG_TANQUE_LEFT = pygame.transform.scale(pygame.image.load(os.path.join('img', 'tanque_left.png')), DIM_TANQUE)
IMG_TANQUE_RIGHT = pygame.transform.scale(pygame.image.load(os.path.join('img', 'tanque_right.png')), DIM_TANQUE)
IMG_CANO_LEFT = pygame.transform.scale(pygame.image.load(os.path.join('img', 'cano_left.png')), DIM_CANO)
IMG_CANO_RIGHT = pygame.transform.scale(pygame.image.load(os.path.join('img', 'cano_right.png')), DIM_CANO)
IMG_BALA = pygame.transform.scale(pygame.image.load(os.path.join('img', 'bala.png')), DIM_BALA)
IMG_NUVEM = pygame.transform.scale(pygame.image.load(os.path.join('img', 'nuvem.png')), DIM_NUVEM)
IMG_NUVEM.set_alpha(220)
IMG_NUVEM_ARAMIS = pygame.transform.scale(pygame.image.load(os.path.join('img', 'nuvem_aramis.png')), DIM_NUVEM)
IMG_NUVEM_ARAMIS.set_alpha(220)
IMG_MURO = pygame.transform.scale(pygame.image.load(os.path.join('img', 'muro.png')),DIM_MURO)
IMG_CORACAO = pygame.image.load(os.path.join('img', 'coracao.png'))
IMG_CORACAO_VAZIO = pygame.image.load(os.path.join('img', 'coracao_vazio.png'))
IMG_BOOM = pygame.image.load(os.path.join('img', 'boom.png'))
IMG_BOOM_FINAL = pygame.image.load(os.path.join('img', 'boom.png'))
IMG_FENO = [
        pygame.transform.scale(pygame.image.load(os.path.join('img', 'feno.png')), DIM_FENO),
        pygame.transform.scale(pygame.image.load(os.path.join('img', 'feno1.png')), DIM_FENO),
        pygame.transform.scale(pygame.image.load(os.path.join('img', 'feno2.png')), DIM_FENO),
        pygame.transform.scale(pygame.image.load(os.path.join('img', 'feno3.png')), DIM_FENO)
]

# altura do chão para colisão
ALTURA_CHAO = 490

# definir uma fonte para os textos
pygame.font.init()
FONTE = pygame.font.SysFont('stencil', 50)


class Tanque:
    def __init__(self, x, lado, cano):
        self.x = x
        self.y = ALTURA_CHAO + 10
        self.lado = lado
        self.velocidade = 3
        self.cano = cano
        self.imagem = IMG_TANQUE_LEFT if lado == 'l' else IMG_TANQUE_RIGHT

    def mover(self, direcao):
        # deslocando para o lado certo
        if direcao == 'l':
            self.x -= self.velocidade
        if direcao == 'r':
            self.x += self.velocidade

    # desenhar o tanque na tela
    def desenhar(self, tela):
        # cria o retângulo para inserir a imagem na tela com a posição topleft
        rect_tanque = self.imagem.get_rect(topleft=(self.x, self.y))
        # desenha as imagens do cano e do tanque na tela
        self.cano.desenhar(tela, rect_tanque)
        tela.blit(self.imagem, rect_tanque.topleft)

    def atirar(self, tela):
        bala = Bala(self.x, self.y, self.lado)
        bala.desenhar(tela)

    # pegar máscara de pixels para a colisão
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)
    

class Cano:
    def __init__(self, lado, angulo):
        self.angulo = angulo
        self.imagem = IMG_CANO_LEFT if lado == 'l' else IMG_CANO_RIGHT

    def mover(self, direcao):
        if direcao == 'up':
            if self.angulo <= 75:
                self.angulo += 1
        if direcao == 'down':
            if self.angulo >= -75:
                self.angulo -= 1

    def desenhar(self, tela, rect_tanque):
        # alinha o centro inferior do cano ao centro superior do tanque
        rect_cano = self.imagem.get_rect(center=(rect_tanque.midtop[0], rect_tanque.midtop[1] + 10))
        # aplica rotação na imagem do cano (sem alterar o centro inferior)
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        rect_cano_rotacionado = imagem_rotacionada.get_rect(center=rect_cano.center)
        # desenha o cano rotacionado
        tela.blit(imagem_rotacionada, rect_cano_rotacionado.topleft)

    # pegar máscara de pixels para a colisão
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Bala:
    def __init__(self, x, y, lado):
        self.x = x
        self.y = y
        self.lado = lado
        self.velocidade = 0
        self.tempo = 0
        self.imagem = IMG_BALA

    def mover(self):
        # calcular o deslocamento
        self.tempo += 1
        # fórmula do sorvetão - S = S0 + V0.t + 1/2.a.t^2
        deslocamento = 1.2 * (self.tempo**2) + self.velocidade * self.tempo

        # deslocando a bala
        self.x += deslocamento
        self.y += deslocamento
        self.x = self.x

    def desenhar(self, tela):
        # cria o retângulo para inserir a imagem na tela com a posição topleft
        rect_bala = self.imagem.get_rect(topleft=(self.x, self.y))
        # desenha a imagem na tela
        tela.blit(self.imagem, rect_bala.topleft)

    # pegar máscara de pixels para a colisão
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Nuvem:
    def __init__(self):
        self.x = -200
        self.y = random.randint(100, 250)
        self.velocidade = 1.5
        self.imagem = IMG_NUVEM_ARAMIS if random.randint(0,10) == 1 else IMG_NUVEM

    def mover(self):
        self.x += self.velocidade
    
    def desenhar(self, tela):
        # cria o retângulo para inserir a imagem na tela com a posição topleft
        rect_nuvem = self.imagem.get_rect(topleft=(self.x, self.y))
        # desenha a imagem na tela
        tela.blit(self.imagem, rect_nuvem.topleft)


class Muro:
    def __init__(self):
        self.x = (TELA_LARGURA / 2) - 25
        self.y = (TELA_ALTURA / 2) + 11
        self.imagem = IMG_MURO

    def desenhar(self, tela):
        # cria o retângulo para inserir a imagem na tela com a posição topleft
        rect_muro = self.imagem.get_rect(topleft=(self.x, self.y))
        # desenha a imagem na tela
        tela.blit(self.imagem, rect_muro.topleft)

    # pegar máscara de pixels para a colisão
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Feno:
    TEMPO_ANIMACAO = 15
    TEMPO_DESLOCAMENTO = 100

    def __init__(self):
        self.x = -50
        self.y = 650
        self.velocidade = 1.5
        self.imagem = IMG_FENO[0]
        self.contagem_imagem = 0
        self.contagem_deslocamento = 0

    def mover(self):
        # retornar ao incio da tela
        if self.x > 1500:
            if random.randint(1,2) == 1:
                self.x = -50

        # movimento horizontal
        self.x += self.velocidade

        # movimento vertical
        self.contagem_deslocamento += 1
        if self.contagem_deslocamento < self.TEMPO_DESLOCAMENTO:
            self.y -= random.uniform(0, 1.3)
        elif self.contagem_deslocamento < self.TEMPO_DESLOCAMENTO*2:
            self.y += random.uniform(0, 1.3)
        elif self.contagem_deslocamento == self.TEMPO_DESLOCAMENTO*2:
            self.contagem_deslocamento = 0

    def mudar_imagens(self):
        # definir qual imagem do pássaro vai aparecer
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = IMG_FENO[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = IMG_FENO[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = IMG_FENO[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = IMG_FENO[3]
        elif self.contagem_imagem == self.TEMPO_ANIMACAO*4:
            self.contagem_imagem = 0

    def desenhar(self, tela):
        # cria o retângulo para inserir a imagem na tela com a posição topleft
        rect_bala = self.imagem.get_rect(topleft=(self.x, self.y))
        # desenha a imagem na tela
        tela.blit(self.imagem, rect_bala.topleft)
        # troca de imagem
        self.mudar_imagens()
        

def desenhar_tela(tela, muro: Muro, feno: Feno, nuvens: list[Nuvem], tanque_left: Tanque, tanque_right: Tanque, balas: list[Bala]):
    # background
    tela.blit(IMG_BACKGROUND, (0, 0))
    # muro
    muro.desenhar(tela)
    # feno
    feno.desenhar(tela)
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
    feno = Feno()
    nuvens = [Nuvem()]
    cano_left = Cano(lado='l', angulo=0)
    cano_right = Cano(lado='r', angulo=0)
    tanque_left = Tanque(x=300, lado='l', cano=cano_left)
    tanque_right = Tanque(x=1000, lado='r', cano=cano_right)
    balas = []
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(60)

        # interações pelo teclado
        for evento in pygame.event.get():
            # se fechar a janela do jogo
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()

        teclas = pygame.key.get_pressed()

        # Movimentação tanque esquerda
        # Tanque
        if teclas[pygame.K_d]:
            tanque_left.mover(direcao='r')
        if teclas[pygame.K_a]:
            tanque_left.mover(direcao='l')
        # Cano
        if teclas[pygame.K_w]:
            cano_left.mover(direcao='up')
        if teclas[pygame.K_s]:
            cano_left.mover(direcao='down')
        # Tiro
        if teclas[pygame.K_SPACE]:
            tanque_left.atirar(tela)

        # Movimentação tanque direita
        # Tanque
        if teclas[pygame.K_RIGHT]:
            tanque_right.mover(direcao='r')
        if teclas[pygame.K_LEFT]:
            tanque_right.mover(direcao='l')
        # Cano
        if teclas[pygame.K_UP]:
            cano_right.mover(direcao='down')
        if teclas[pygame.K_DOWN]:
            cano_right.mover(direcao='up')
        # Tiro
        if teclas[pygame.K_RSHIFT]:
            tanque_right.atirar(tela)

        # movendo os componentes da tela
        for bala in balas:
            bala.mover()
        for nuvem in nuvens:
            nuvem.mover()
        feno.mover()

        # desenhando a tela
        desenhar_tela(tela, muro, feno, nuvens, tanque_left, tanque_right, balas)


if __name__ == '__main__':
    main()
