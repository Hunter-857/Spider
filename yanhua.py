import pygame
from math import *
from pygame.locals import *

import random


class Fireworks:

    def __init__(self, pos, color, light, size, move):
        self.pos = list(pos)
        self.color = list(color)
        self.light = light
        self.size = size

        self.move = list(move)

    def force(self, force):
        self.move[0] += force[0]
        self.move[1] += force[1]

        self.move[0] *= force[2]
        self.move[1] *= force[2]

    def update(self):
        self.pos[0] += self.move[0]
        self.pos[1] += self.move[1]

    def render(self, fenster, glitter):
        glitter = (glitter and random.randint(40, 100) / 100) or 1
        c = rund(mult(self.color, self.light * glitter))
        rad = int(round(self.light * self.size))
        rad += rad < 1
        # print(c)

        pygame.draw.circle(fenster, c, rund(self.pos), rad)


def summon(fws, pos, pre_move=[0, 0]):
    mix.stop()
    # anz = random.randint(30, 250)
    anz = random.randint(200, 350)
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    for i in range(anz):
        ang = random.randint(0, 360)
        speed = random.randint(100, 1000) / 250

        move = (cos(radians(ang)) * speed + pre_move[0],
                sin(radians(ang)) * speed + pre_move[1])

        light = random.randint(60, 100) / 100
        size = random.randint(300, 400) / 30

        fws.append(Fireworks(pos, (r, g, b), light, size, move))

    # Sound abspielen
    l, r = (0.2 + 0.8 * (ww - pos[0]) / ww, 0.2 + 0.8 * pos[0] / ww)
    mix.set_volume(l, r)

    mix.play(sound)

    return fws


def rund(liste):
    new = []
    for i in liste:
        new.append(int(round(i)))

    return new


def mult(color, multi):
    new = list(color)
    new[0] *= multi
    new[1] *= multi
    new[2] *= multi

    return new


pygame.init()

sound = pygame.mixer.Sound("fire.mp3")
mix = pygame.mixer.Channel(0)
mix.set_volume(1, 1)

bg = (0, 0, 0)
ww, wh = (1200, 800)
fenster = pygame.display.set_mode((ww, wh))
# pygame.display.set_caption("[Leertaste] für Pause; [c] für automatisches Feuerwerk")


fws = []  # firework particles
rockets = []
force = [0, 0.02, 0.985]

max_counter = random.randint(0, 200)
counter = max_counter

auto = True
pause = False

run = 1
clock = pygame.time.Clock()

while run:
    pygame.display.set_caption("#豫鲁二踢脚战役  #炮仗一响黄金万两 鲁豫事变")
    counter -= (auto and not pause)

    if counter <= 0:  # neues erstellen
        # pos = [random.randint(ww*1/4, ww*3/4), random.randint(wh*1/4, wh*3/5)]
        move = [random.randint(-100, 100) / 100, -random.randint(600, 1500) / 110]
        pos = [random.randint(ww * 2 / 5, ww * 3 / 5), wh]

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        # 随机生成的还没有爆炸的离子
        rockets.append(Fireworks(pos, (r, g, b), 1, 10, move))

        # fuse = random.randint(50, 150) # Zuendschnur
        fuse = random.randint(50, 80)
        rockets[-1].fuse = fuse

        # fws = summon(fws, pos)

        max_counter = random.randint(10, 100)
        counter = max_counter

    for e in pygame.event.get():
        if e.type == QUIT:
            run = 0
        if e.type == KEYDOWN:
            if e.key == K_c:
                auto = not auto
            if e.key == K_SPACE:
                pause = not pause
            if e.key == K_v:
                fws = []
                rockets = []

        if e.type == MOUSEBUTTONDOWN:
            fws = summon(fws, e.pos)

    fenster.fill(bg)
    dellist1 = []
    dellist2 = []

    for i, rocket in enumerate(rockets):
        if not pause:
            rocket.force(force)
            rocket.update()

        rocket.render(fenster, False)
        rocket.fuse -= not pause

        if rocket.fuse < 0:
            dellist1.append(i)
            # explosion erschaffen
            fws = summon(fws, rocket.pos, rocket.move)

    for i, f in enumerate(fws):
        if not pause:
            f.force(force)
            f.update()

        f.render(fenster, True and not pause)

        f.light -= (not pause) * random.randint(0, 150) / 7500

        if f.light < 0:
            dellist2.append(i)

    dellist1.reverse()
    dellist2.reverse()

    for d in dellist1:
        del rockets[d]
    for d in dellist2:
        del fws[d]

    pygame.display.update()
    clock.tick(80)

pygame.quit()
