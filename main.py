import sys
import pygame
import math
from math import atan2, degrees, pi
import level

MAX_SPEED = 30
# MAX_SPEED = 10
SPEED_INCREMENT = 0.5
SPEED_DECREMENT = 0.5
BUMP_SPEED = 15
BUMP_SPEED_DECREMENT = 1
START_FUEL = 50
BUMP_DAMAGE = 10

FUEL_HIGH = 70
FUEL_MEDIUM = 40

MAX_FUEL = 400

FUEL_INCREMENT = 1
FUEL_DECREMENT = 0.1

TEXT_TIME = 20

# START_X = -10000
# START_Y = -2000
START_X = -800
START_Y = -400


class Space(pygame.sprite.Sprite):

    def __init__(self, location, picture):
        super(Space, self).__init__()
        self.image = picture
        self.rect = pygame.rect.Rect(location, self.image.get_size())

    def draw(self, surface, view_x, view_y):
        x = self.rect.x
        y = self.rect.y
        view_position = (x - view_x, y - view_y)
        surface.blit(self.image, view_position)

class Obstacle(pygame.sprite.Sprite):

    def __init__(self, location, picture, deadly=False):
        super(Obstacle, self).__init__()
        self.image = picture
        self.deadly = deadly

        rect = picture.get_rect()
        location = (location[0] - (rect.w / 2), location[1] - (rect.h / 2))

        self.rect = pygame.rect.Rect(location, self.image.get_size())

    def draw(self, surface, view_x, view_y):
        x = self.rect.x
        y = self.rect.y
        view_position = (x - view_x, y - view_y)
        surface.blit(self.image, view_position)

class Character(pygame.sprite.Sprite):

    def __init__(self, location, picture, text):
        super(Character, self).__init__()
        self.image = picture
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.text = text
        self.text_time = 0

    def draw(self, surface, view_x, view_y):
        x = self.rect.x
        y = self.rect.y
        view_position = (x - view_x, y - view_y)
        surface.blit(self.image, view_position)

    def draw_text(self, surface, view_x, view_y, font):

        if self.text_time > 0:
            x = self.rect.x
            y = self.rect.y
            view_position = (x - view_x, y - view_y)

            width = 0

            for t in self.text:
                size = font.size(t)
                width = max(size[0], width)

            height = len(self.text) * 20

            view_position = (view_position[0], view_position[1] - (height / 2) + 100)

            pygame.draw.rect(surface, (200,200,200), pygame.Rect(view_position[0], view_position[1], width, height))

            for ix, t in enumerate(self.text):
                label = font.render(t, 1, (0,0,0))
                view_position = (view_position[0], view_position[1] + (20 * ix))
                surface.blit(label, view_position)

    def update(self):
        if self.text_time > 0:
            self.text_time -= 1

class Recharge(pygame.sprite.Sprite):

    def __init__(self, location, picture):
        super(Recharge, self).__init__()
        self.image = picture
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

        rads = atan2(self.dx, self.dy)
        rads += pi
        degs = degrees(rads)

        rotated = pygame.transform.rotate(self.image, degs)

        # need to offset it a little because rotation changes the size
        orig_rect = self.image.get_rect()
        rotated_rect = rotated.get_rect()

        dw = (rotated_rect.w - orig_rect.w) / 2.0
        dh = (rotated_rect.h - orig_rect.h) / 2.0

        surface.blit(rotated, (pos_x - dw, pos_y - dh))

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
            if sq != 0:
                self.dx = self.dx / sq
                self.dy = self.dy / sq

            if key[pygame.K_UP] or pygame.mouse.get_pressed()[0]:
                self.speed += SPEED_INCREMENT

                accel = pygame.mixer.Channel(5)

                if accel.get_busy() == 0:
                    accel.play(game.sound['accel'])
            else:
                self.speed -= SPEED_DECREMENT
                game.sound['accel'].stop()

            if self.speed < 0:
                self.speed = 0
            if self.speed > MAX_SPEED:
                self.speed = MAX_SPEED

            if self.speed > 0:
                self.fuel -= FUEL_DECREMENT

            self.rect.x += self.dx * self.speed;
            self.rect.y += self.dy * self.speed;

        #####################################
        # collision
        #####################################

        for s in game.obstacles:
            if pygame.sprite.collide_rect(s, self) and pygame.sprite.collide_mask(s, self):
                if s.deadly:
                    self.fuel = 0
                    break

                self.bump = True
                self.speed = BUMP_SPEED
                # reverse direction
                self.dx = self.dx * -1
                self.dy = self.dy * -1

                self.fuel -= BUMP_DAMAGE

                game.sound['bump'].play()

        for s in game.recharge:
            if pygame.sprite.collide_rect(s, self):
                self.fuel += FUEL_INCREMENT

                if self.fuel > MAX_FUEL:
                    self.fuel = MAX_FUEL

                game.sound['recharge'].play()

        for s in game.character:
            if pygame.sprite.collide_rect(s, self):
                if s.text_time <= 0:
                    game.sound['voice'].play()

                s.text_time = TEXT_TIME

class Game(object):

    def __init__(self):
        print "Initializing"

    def fuel_colour(self):
        if self.player.fuel > FUEL_HIGH:
            return (0,255,0)
        elif self.player.fuel > FUEL_MEDIUM:
            return (255,255,0)
        else:
            return (255,0,0)

    def main(self, screen):
        clock = pygame.time.Clock()

        # pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

        self.player = Player((START_X,START_Y))

        self.background = []

        self.pictures = {}
        self.pictures['space'] = pygame.image.load('gfx/space.png')
        self.pictures['asteroid'] = pygame.image.load('gfx/asteroid.png')
        self.pictures['planet'] = pygame.image.load('gfx/planet.png')
        self.pictures['recharger'] = pygame.image.load('gfx/recharge.png')
        self.pictures['recharger_big'] = pygame.image.load('gfx/recharge_big.png')
        self.pictures['character'] = pygame.image.load('gfx/character.png')
        self.pictures['character_small'] = pygame.image.load('gfx/character_small.png')
        self.pictures['character_medium'] = pygame.image.load('gfx/character_medium.png')
        self.pictures['bigwhite8'] = pygame.image.load('gfx/Big_White_8.png')
        self.pictures['mediumred6'] = pygame.image.load('gfx/Medium_Red_6_Large.png')
        self.pictures['smallgreen6'] = pygame.image.load('gfx/Small_Green_6.png')
        self.pictures['bigblue3'] = pygame.image.load('gfx/Big_Blue_3.png')
        self.pictures['smallgold3'] = pygame.image.load('gfx/Small_Gold_3.png')
        self.pictures['mediumblue2'] = pygame.image.load('gfx/Medium_Blue_NoWater_2.png')
        self.pictures['smallred2'] = pygame.image.load('gfx/Small_Red_2.png')
        self.pictures['mediumwhite2'] = pygame.image.load('gfx/Medium_White_2.png')
        self.pictures['elysium'] = pygame.image.load('gfx/Elysium.png')
        self.pictures['sun'] = pygame.image.load('gfx/Sun.png')


        smallfont = pygame.font.Font("font.ttf", 15)
        smallfont.set_bold(True)



        space_rect = self.pictures['space'].get_rect()
        for x in range(-10, 10):
            for y in range(-10, 10):
                sx = x * space_rect.w
                sy = y * space_rect.h

                self.background.append(Space((sx, sy), self.pictures['space']))

        self.obstacles = level.create_obstacles(self.pictures)
        self.character = level.create_characters(self.pictures)
        self.recharge = level.create_rechargers(self.pictures)

        self.sound = {}
        self.sound['bump'] = pygame.mixer.Sound('sound/ship_bump.wav')
        self.sound['recharge'] = pygame.mixer.Sound('sound/refuel.wav')
        self.sound['voice'] = pygame.mixer.Sound('sound/VoiceTextSound.wav')
        self.sound['accel'] = pygame.mixer.Sound('sound/thrusters.wav')
        self.sound['gameover'] = pygame.mixer.Sound('sound/PowerDown.wav')

        screen_rect = screen.get_rect()
        half_screen_w = screen_rect.w / 2
        half_screen_h = screen_rect.h / 2

        myfont = pygame.font.Font("font.ttf", 30)
        myfont.set_bold(True)

        self.debug = False

        while 1:
            dt = clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN and \
                        event.key == pygame.K_ESCAPE:
                    return True
                if event.type == pygame.KEYUP and \
                        event.key == pygame.K_d:
                    self.debug = not self.debug


            self.player.update(dt, self)

            for s in self.character:
                s.update()

            screen.fill((200, 200, 200))

            for s in self.background:
                s.draw(screen, self.player.rect.x - half_screen_w, self.player.rect.y - half_screen_h)

            for s in self.obstacles:
                s.draw(screen, self.player.rect.x - half_screen_w, self.player.rect.y - half_screen_h)

            self.player.draw(screen, 0, 0)

            label = myfont.render("Fuel: {}".format(int(self.player.fuel)), 1, self.fuel_colour())
            screen.blit(label, (10, 10))

            label = myfont.render("Coordinates: {}/{}".format(int(self.player.rect.x / 100), int(self.player.rect.y / 100)), 1, (90,90,90))
            # label = myfont.render("Coordinates: {}/{}".format(int(self.player.rect.x), int(self.player.rect.y)), 1, (90,90,90))
            screen.blit(label, (10, 40))

            for s in self.character:
                s.draw_text(screen, self.player.rect.x - half_screen_w, self.player.rect.y - half_screen_h, smallfont)

            if self.debug:
                for s in self.recharge:
                    s.draw(screen, self.player.rect.x - half_screen_w, self.player.rect.y - half_screen_h)

                for s in self.character:
                    s.draw(screen, self.player.rect.x - half_screen_w, self.player.rect.y - half_screen_h)

            pygame.display.flip()

            if self.player.fuel <= 0:
                self.sound['gameover'].play()
                break;

        return False


class GameOver(object):

    def main(self, screen):
        clock = pygame.time.Clock()

        myfont = pygame.font.Font("font.ttf", 30)
        myfont.set_bold(True)

        while 1:
            dt = clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN and \
                        event.key == pygame.K_ESCAPE:
                    return True
                if event.type == pygame.KEYDOWN and \
                        event.key == pygame.K_r:
                    return False

            screen.fill((200, 200, 200))

            label = myfont.render("Game Over", 1, (0,0,0))
            screen.blit(label, (10, 100))

            label = myfont.render("Press 'R' to restart", 1, (0,0,0))
            screen.blit(label, (10, 150))

            pygame.display.flip()

class GameStart(object):

    def main(self, screen):
        clock = pygame.time.Clock()

        myfont = pygame.font.Font("font.ttf", 30)
        myfont.set_bold(True)

        smallfont = pygame.font.Font("font.ttf", 15)
        smallfont.set_bold(True)


        cover = pygame.image.load('gfx/Cover.png')

        while 1:
            dt = clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN and \
                        event.key == pygame.K_ESCAPE:
                    return True
                if event.type == pygame.KEYDOWN:
                    return False

            screen.fill((0, 0, 0))

            screen.blit(cover, (200, 100))

            label = myfont.render("Early Access: Search for Elysium", 1, (200,200,200))
            screen.blit(label, (10, 100))

            label = smallfont.render("Find the hidden world of Elysium!", 1, (200,200,200))
            screen.blit(label, (10, 420))

            label = smallfont.render("Watch your fuel tank! Refuel with water.", 1, (200,200,200))
            screen.blit(label, (10, 450))

            label = smallfont.render("Talk to the aliens to get hints, but sometimes they are wrong and", 1, (200,200,200))
            screen.blit(label, (10, 480))

            label = smallfont.render("coordinates are always a bit off. Go to the middle points.", 1, (200,200,200))
            screen.blit(label, (10, 495))

            label = myfont.render("Press a key to start", 1, (200,200,200))
            screen.blit(label, (10, 540))

            pygame.display.flip()



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800,600))

    pygame.mouse.set_visible(False)
    pygame.display.init()

    if len(sys.argv) > 1 and sys.argv[1] == '-fullscreen':   
        pygame.display.toggle_fullscreen()

    quit = False
    while not quit:
        quit = GameStart().main(screen)

        if not quit:
            quit = Game().main(screen)
    
        if not quit:
            quit = GameOver().main(screen)
