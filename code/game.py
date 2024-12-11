import pygame
import pytmx
import pyscroll
from player import Player


class Game:

    def __init__(self):
        self.map = "world"

        self.screen = pygame.display.set_mode((1550, 900))
        pygame.display.set_caption("pluton")

        tmx_data = pytmx.util_pygame.load_pygame("../maps/carte_jeux.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2



        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))


        self.group = pyscroll.PyscrollGroup(map_layer= map_layer, default_layer = 9)
        self.group.add(self.player)

        enter_grotte = tmx_data.get_object_by_name("enter_grotte")
        self.enter_grotte_rect = pygame.Rect(enter_grotte.x, enter_grotte.y, enter_grotte.width, enter_grotte.height)



    def handle_input(self):


        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')

        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')

        if pressed[pygame.K_SPACE]:
            if self.player.nombre_de_saut == 1:
                self.player.nombre_de_saut += 1
                self.player.a_sauter = True


    def switch_grotte(self):
        self.map = "grotte"

        # Charger la carte clasique
        tmx_data = pytmx.util_pygame.load_pygame("../maps/grotte_jeux.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # Les collisions
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner les différents calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=9)
        self.group.add(self.player)

        # Porte de la maison
        exit_grotte = tmx_data.get_object_by_name("exit_grotte")
        self.exit_grotte_rect = pygame.Rect(exit_grotte.x, exit_grotte.y, exit_grotte.width, exit_grotte.height)

        # Intérieur
        spawn_grotte_point = tmx_data.get_object_by_name("spawn_player")
        self.player.position[0] = spawn_grotte_point.x
        self.player.position[1] = spawn_grotte_point.y


    def switch_world(self):
        self.map = "world"

        # Charger la carte clasique
        tmx_data = pytmx.util_pygame.load_pygame("../maps/carte_jeux.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # Les collisions
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner les différents calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=9)
        self.group.add(self.player)


        enter_grotte = tmx_data.get_object_by_name("enter_grotte")
        self.enter_grotte_rect = pygame.Rect(enter_grotte.x, enter_grotte.y, enter_grotte.width, enter_grotte.height)

        # Intérieur
        spawn_world_point = tmx_data.get_object_by_name("enter_grotte_exit")
        self.player.position[0] = spawn_world_point.x
        self.player.position[1] = spawn_world_point.y





    def update(self):
        self.group.update()

        # Vérifier l'entrer de la maison
        if self.map == "world" and self.player.feet.colliderect(self.enter_grotte_rect):
            self.switch_grotte()

        if self.map == "grotte" and self.player.feet.colliderect(self.exit_grotte_rect):
            self.switch_world()

        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()
                self.player.move_sureleve()
                self.player.nombre_de_saut = 1




    def run(self):

        clock = pygame.time.Clock()

        running = True
        while running:
            self.player.save_location()

            self.handle_input()
            self.player.sauter()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

            pygame.display.flip()