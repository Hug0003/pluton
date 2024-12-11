import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.sprite_sheet = pygame.image.load('../sprites/player.png')
        self.image = self.get_image(0,0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.images = {
            'left': self.get_image(0, 32),
            'right': self.get_image(0, 64)
        }
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.speed = 3
        self.saut = 0
        self.saut_montee = 0
        self.saut_descente = 6
        self.nombre_de_saut = 1
        self.a_sauter = False



    def sauter(self):
        if self.a_sauter:

            if self.saut_montee >= 1:
                self.saut_descente -= 1
                self.saut = self.saut_descente

            else:
                self.saut_montee += 1
                self.saut = self.saut_descente

            if self.saut_descente < 0:
                self.saut_montee = 0
                self.saut_descente = 6
                self.a_sauter = False


        self.position[1] = self.position[1] - (10 * (self.saut / 2 ))




    def save_location(self):
        self.old_position = self.position.copy()


    def change_animation(self, name):
        self.image = self.images[name]
        self.image.set_colorkey((0, 0, 0))

    def move_right(self):
        self.position[0] += 5

    def move_left(self):
        self.position[0] -= 5

    def move_down(self):
        self.position[1] += self.speed

    def move_sureleve(self):
        self.position[1] -= 5


    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.update()

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

