import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# stwórz klasę -> kostka węża
class Cube(object):
    rows = 20
    def __init__(self, start, dirnx=1, dirny=0, color=(0, 0, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)


    def draw(self, surface, eyes=False):
        dis = size // rows
        rw = self.pos[0]
        cm = self.pos[1]
        pygame.draw.rect(surface, self.color, (rw * dis + 1, cm * dis +1, dis - 2, dis - 2))

        if eyes:
            center = dis//2
            radius = 3
            circle_middle = (rw * dis + center - radius - 2, cm * dis + 8)
            circle_middle2 = (rw * dis + dis  - radius * 2, cm * dis + 8)
            pygame.draw.circle(surface, (255, 255, 255), circle_middle, radius)
            pygame.draw.circle(surface, (255, 255, 255), circle_middle2, radius)
# stwórz klasę -> wąż

class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            # zamknij gre po naciśnięciu krzyżyka
            if event.type == pygame.QUIT:
                pygame.quit()


            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_RIGHT]:
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_UP]:
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_DOWN]:
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) -1:
                    self.turns.pop(p)

            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.body = []  # Wyczyść ciało węża
        self.head = Cube(pos)  # Utwórz nową głowę węża
        self.body.append(self.head)  # Dodaj głowę do ciała węża
        self.dirnx = 0
        self.dirny = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

# stwórz funkcję rysowania siatki
def draw_grid(w, rows, surface):
    size_between = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + size_between
        y = y + size_between
        pygame.draw.line(surface, (255, 255, 255), (x,0), (x,w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

# stwórz funkcję rysowania okna
def draw_window(surface):
    surface.fill((0, 255, 0))
    s.draw(surface)
    apple.draw(surface)
    draw_grid(size, rows, surface)
    pygame.display.update()
                    # stwórz funkcję rysowania jabłuszka
def random_apple(snake):
    position = snake.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x,y), position))) > 0:
            continue
        else:
            break
    return (x, y)


            #  stwórz funkcję dla okna informacyjnego
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", 1)
    root.withdraw()
    messagebox.showinfo(subject, content)

    try:
        root.destroy()
    except:
        pass


def main():
    global size, rows, s, apple
    size = 500 #obszar gry
    rows = 20

    window = pygame.display.set_mode((size,size))

    s = Snake((0, 0, 0), (10,10))
    apple = Cube(random_apple(s), color=(255, 0, 0))
    # jeżeli True gra działa
    flag = True
    clock = pygame.time.Clock()

    while flag:

        pygame.time.delay(50)      # im mniejsza wartość delay tym gra szybsza
        clock.tick(10)             # im mniej tym gra wolniejsza
        s.move()
        if s.body[0].pos == apple.pos:
            s.add_cube()
            apple = Cube(random_apple(s), color=(255, 0, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x+1:])):
                message_box('GAME OVER', 'Czy chcesz zagrać ponownie?')
                s.reset((10,10))

        draw_window(window)




main()