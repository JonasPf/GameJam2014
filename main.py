import pygame
from math import atan2, degrees, pi

MAX_SPEED = 0.08
SPEED_INCREMENT = 0.0015
SPEED_DECREMENT = 0.0015

def angle(pos, origin):
    dx = pos[0] - origin[0]
    dy = pos[1] - origin[1]
    rads = atan2(-dy,dx)
    rads %= 2*pi
    degs = degrees(rads)

    return degs

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

        self.fuel = 99
        self.speed = 0.0

        self.direction_x = 0
        self.direction_y = 0

        self.direction_deg = 0

    def draw(self, surface, view_x, view_y):
        r = surface.get_rect()
        screen_w = r.w
        screen_h = r.h

        pos_x = (screen_w / 2) - (self.image.get_rect().x / 2)
        pos_y = (screen_h / 2) - (self.image.get_rect().y / 2)

        surface.blit(self.image, (pos_x, pos_y))

    def update(self, dt, game):
        key = pygame.key.get_pressed()

        if key[pygame.K_UP]:
            self.speed += SPEED_INCREMENT
        else:
            self.speed -= SPEED_DECREMENT

        if self.speed < 0:
            self.speed = 0
        if self.speed > MAX_SPEED:
            self.speed = MAX_SPEED


        

        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_center_x = self.rect.x + (self.rect.w / 2)
        player_center_y = self.rect.y + (self.rect.h / 2)

        screen_rect = screen.get_rect()
        half_screen_w = screen_rect.w / 2
        half_screen_h = screen_rect.h / 2

        self.direction_deg = angle((mouse_x, mouse_y), (half_screen_w, half_screen_h))        


        print self.direction_deg

        if mouse_x > half_screen_w:
            self.direction_x = 1

        if mouse_x < half_screen_w:
            self.direction_x = -1

        if mouse_y > half_screen_h:
            self.direction_y = 1

        if mouse_y < half_screen_h:
            self.direction_y = -1



        # if mouse_x < self.rect.x or mouse_x > self.rect.x + self.rect.w:
        #     if mouse_x > player_center_x:
        #         self.direction_x = 1
        #     elif mouse_x < player_center_x:
        #         self.direction_x = -1

        # if mouse_y < self.rect.y or mouse_y > self.rect.y + self.rect.h:
        #     if mouse_y > player_center_y:
        #         self.direction_y = 1
        #     elif mouse_y < player_center_y:
        #         self.direction_y = -1

        # v1 = ( half_screen_w, half_screen_h );
        # v2 = ( mouse_x, mouse_y );
        # dir = v2 - v1;
        dx = mouse_x - half_screen_w
        # dx.normalize()
        dy = mouse_y - half_screen_h
        # dy.normalize()


        # dir.normalize();
        self.rect.x += dx * self.speed;
        self.rect.y += dy * self.speed;

        # self.rect.x += self.speed * dt * self.direction_x
        # self.rect.y += self.speed * dt * self.direction_y

class Game(object):

    def __init__(self):
        print "Initializing"

    def main(self, screen):
        clock = pygame.time.Clock()

        player = Player((5,5))

        stuff = []
        stuff.append(Asteroid((5,5), 'gfx/asteroid.png'))
        stuff.append(Asteroid((300, 300), 'gfx/planet.png'))

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

            for s in stuff:
                s.draw(screen, player.rect.x - half_screen_w, player.rect.y - half_screen_h)
            player.draw(screen, 0, 0)

            pygame.display.flip()



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    Game().main(screen)
