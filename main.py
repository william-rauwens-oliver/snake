import pygame
import sys
import random
from pygame.math import Vector2
from ia import IA

# j'ai décidé d'utilisé des classes pour organiser et encapsuler la logique spécifique à chaque composant du jeu Snake, améliorant ainsi la lisibilité, la maintenabilité et la modularité du code tout en apprenant à quoi les classes servent.

class GameModeSelector:
    def __init__(self):
        self.directions = [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]
        self.selected_mode = None
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font("Font/Outwrite.ttf", 50)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.selected_mode = "Solo"
                        return
                    elif event.key == pygame.K_i:
                        self.selected_mode = "IA"
                        return

            self.draw_selector()
            pygame.display.flip()

    def draw_selector(self):
        screen.fill((175, 215, 70))

        # Utiliser la nouvelle police pour le titre
        title_text = self.title_font.render("Snake", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(title_text, title_rect)

        # Créer des rectangles avec un fond vert foncé et un espace entre eux
        rect_width, rect_height = 500, 50
        space_between_rects = 20
        border_radius = 10  
        solo_rect = pygame.Rect((screen.get_width() - rect_width) // 2, (screen.get_height() - rect_height) // 2 - 25, rect_width, rect_height)
        ai_rect = pygame.Rect((screen.get_width() - rect_width) // 2, (screen.get_height() - rect_height) // 2 + rect_height + space_between_rects, rect_width, rect_height)

        pygame.draw.rect(screen, (56, 74, 12), solo_rect, border_radius=border_radius)
        pygame.draw.rect(screen, (56, 74, 12), ai_rect, border_radius=border_radius)

        # Afficher le texte sur les rectangles
        text_solo = self.font.render("Appuyez sur 's' pour jouer seul", True, (255, 255, 255))
        text_ia = self.font.render("Appuyez sur 'i' pour l'IA", True, (255, 255, 255))

        solo_text_rect = text_solo.get_rect(center=solo_rect.center)
        ai_text_rect = text_ia.get_rect(center=ai_rect.center)

        screen.blit(text_solo, solo_text_rect)
        screen.blit(text_ia, ai_text_rect)

        pygame.display.update()
class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load('images/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('images/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('images/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('images/head_left.png').convert_alpha()
        self.tail_up = pygame.image.load('images/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('images/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('images/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('images/tail_left.png').convert_alpha()
        self.body_vertical = pygame.image.load('images/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('images/body_horizontal.png').convert_alpha()
        self.body_tl = pygame.image.load('images/body_tl.png').convert_alpha()
        self.body_bl = pygame.image.load('images/body_bl.png').convert_alpha()
        self.body_tr = pygame.image.load('images/body_tr.png').convert_alpha()
        self.body_br = pygame.image.load('images/body_br.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('son/crunch.wav')

    def draw_snake(self):
        self.graphic_head()
        self.graphic_tail()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                self.graphic_body(block, block_rect)

    def graphic_head(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down

    def graphic_tail(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down

    def graphic_body(self, block, block_rect):
        for index in range(1, len(self.body) - 1):
            previous_block = self.body[index + 1] - block
            next_block = self.body[index - 1] - block
            if previous_block.x == next_block.x:
                screen.blit(self.body_vertical, block_rect)
            elif previous_block.y == next_block.y:
                screen.blit(self.body_horizontal, block_rect)
            else:
                self.graphic_turns(block, previous_block, next_block, block_rect)

    def graphic_turns(self, block, previous, next, block_rect):
        if previous.x == -1 and next.y == -1 or previous.y == -1 and next.x == -1:
            screen.blit(self.body_tl, block_rect)
        elif previous.x == -1 and next.y == 1 or previous.y == 1 and next.x == -1:
            screen.blit(self.body_bl, block_rect)
        elif previous.x == 1 and next.y == -1 or previous.y == -1 and next.x == 1:
            screen.blit(self.body_tr, block_rect)
        elif previous.x == 1 and next.y == 1 or previous.y == 1 and next.x == 1:
            screen.blit(self.body_br, block_rect)

    def move_snake(self):
        self.control()  # Gestion de la direction du serpent
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction = Vector2(0, -1)
        elif keys[pygame.K_DOWN]:
            self.direction = Vector2(0, 1)
        elif keys[pygame.K_LEFT]:
            self.direction = Vector2(-1, 0)
        elif keys[pygame.K_RIGHT]:
            self.direction = Vector2(1, 0)

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)

class Fruit:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class MainGame:
    def __init__(self, mode):
        self.snake = Snake()
        self.fruit = Fruit()
        self.mode = mode
        if self.mode == "IA":
            self.ai = IA()

    def update(self):
        if self.mode == "IA":
            ai_direction = self.ai.get_next_move(self.snake, self.fruit)
            self.snake.direction = ai_direction
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_objects(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6,
                              apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

# Pygame initialization
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
apple = pygame.image.load('images/apple.png').convert_alpha()
game_font = pygame.font.Font(None, 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

mode_selector = GameModeSelector()
mode_selector.run()

if mode_selector.selected_mode == "Solo":
    main_game = MainGame("Solo")
elif mode_selector.selected_mode == "IA":
    main_game = MainGame("IA")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if mode_selector.selected_mode == "Solo":
            # Gestion des événements du clavier pour le mode "Solo"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    main_game.snake.direction = Vector2(0, -1)
                elif event.key == pygame.K_DOWN:
                    main_game.snake.direction = Vector2(0, 1)
                elif event.key == pygame.K_LEFT:
                    main_game.snake.direction = Vector2(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    main_game.snake.direction = Vector2(1, 0)

    main_game.update()

    screen.fill((175, 215, 70))
    main_game.draw_objects()
    pygame.display.update()
    clock.tick(10)