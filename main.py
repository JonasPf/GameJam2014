import pygame
import math
from math import atan2, degrees, pi

MAX_SPEED = 10
SPEED_INCREMENT = 0.5
SPEED_DECREMENT = 0.5
BUMP_SPEED = 15
BUMP_SPEED_DECREMENT = 1
START_FUEL = 99
BUMP_DAMAGE = 10


class Asteroid(pygame.sprite.Sprite):

    def __init__(self, location, picture):
        super(Asteroid, self).__init__()
        self.image = pygame.image.load(picture)
        self.rect = pygame.rect.Rect(location, self.image.get_size())

    def draw(self, surface, view_x, view_y):
        x = self.rect.x
        y = self.rect.y
        view_position = (x - view_x, y - view_y)
        surface.blit(self.image, view_position)

class Planet(pygame.sprite.Sprite):

    def __init__(self, location, picture):
        super(Planet, self).__init__()
        self.image = pygame.image.load(picture)
        self.rect = pygame.rect.Rect(location, self.image.get_size())

    def draw(self, surface, view_x, view_y):
        x = self.rect.x
        y = self.rect.y
        view_position = (x - view_x, y - view_y)
        surface.blit(self.image, view_position)

class Player(pygame.sprite.Sprite):

    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('gfx/spaceship.png')

        self.rect = pygame.rect.Rect(location, self.image.get_size())

        self.fuel = START_FUEL
        self.speed = 0.0
        self.bump = False

        self.dx = 0
        self.dy = 0

    def draw(self, surface, view_x, view_y):
        r = surface.get_rect()
        screen_w = r.w
        screen_h = r.h

        pos_x = (screen_w / 2) - (self.image.get_rect().x / 2)
        pos_y = (screen_h / 2) - (self.image.get_rect().y / 2)

        surface.blit(self.image, (pos_x, pos_y))

    def update(self, dt, game):
        if self.bump:
            # if bump -> reduce speed quickly

            self.rect.x += self.dx * self.speed;
            self.rect.y += self.dy * self.speed;

            self.speed -= BUMP_SPEED_DECREMENT

            if self.speed <= 0:
                self.speed = 0
                self.bump = False
        else:
            key = pygame.key.get_pressed()

            mouse_x, mouse_y = pygame.mouse.get_pos()

            screen_rect = screen.get_rect()
            half_screen_w = screen_rect.w / 2
            half_screen_h = screen_rect.h / 2

            self.dx = mouse_x - half_screen_w
            self.dy = mouse_y - half_screen_h

            # normalize
            sq = math.sqrt(self.dx ** 2 + self.dy ** 2)
            self.dx = self.dx / sq
            self.dy = self.dy / sq

            if key[pygame.K_UP]:
                self.speed += SPEED_INCREMENT
            else:
                self.speed -= SPEED_DECREMENT

            if self.speed < 0:
                self.speed = 0
            if self.speed > MAX_SPEED:
                self.speed = MAX_SPEED

            self.rect.x += self.dx * self.speed;
            self.rect.y += self.dy * self.speed;

        #####################################
        # collision

        for s in game.stuff:
            if pygame.sprite.collide_rect(s, self):
                self.bump = True
                self.speed = BUMP_SPEED
                # reverse direction
                self.dx = self.dx * -1
                self.dy = self.dy * -1

                self.fuel -= BUMP_DAMAGE

                print "FUEL: {}".format(self.fuel)


class Game(object):

    def __init__(self):
        print "Initializing"

    def main(self, screen):
        clock = pygame.time.Clock()

        player = Player((5,5))

        self.stuff = []
        self.stuff.append(Asteroid((-50,5), 'gfx/asteroid.png'))
        self.stuff.append(Asteroid((300, 300), 'gfx/planet.png'))

        screen_rect = screen.get_rect()
        half_screen_w = screen_rect.w / 2
        half_screen_h = screen_rect.h / 2

        while 1:
            dt = clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and \
                        event.key == pygame.K_ESCAPE:
                    return


            player.update(dt, self)

            screen.fill((200, 200, 200))

            for s in self.stuff:
                s.draw(screen, player.rect.x - half_screen_w, player.rect.y - half_screen_h)
            player.draw(screen, 0, 0)

            pygame.display.flip()



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    Game().main(screen)
