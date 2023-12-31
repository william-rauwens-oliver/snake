import pygame
import sys
import random
from pygame.math import Vector2
from ia import IA

# j'ai décidé d'utilisé des classes pour organiser et encapsuler la logique spécifique à chaque composant du jeu Snake, améliorant ainsi la lisibilité, la maintenabilité et la modularité du code tout en apprenant à quoi les classes servent.

# Classe responsable du sélecteur de mode de jeu
class GameModeSelector:
    def __init__(self):
        self.directions = [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]
        self.selected_mode = None
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font("Font/Outwrite.ttf", 50)

# Exécuter le sélecteur de mode
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
                    elif event.key == pygame.K_b:
                        self.show_scores()

            self.draw_selector()
            pygame.display.flip()

     # Fonction pour dessiner le sélecteur de mode à l'écran
    def draw_selector(self):
        screen.fill((175, 215, 70))

        title_text = self.title_font.render("Snake", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 50))
        title_rect_shadow = title_rect.copy()
        title_rect_shadow.x += 2
        title_rect_shadow.y += 2
        title_text_shadow = self.title_font.render("Snake", True, (255, 255, 255))
        screen.blit(title_text_shadow, title_rect_shadow)
        screen.blit(title_text, title_rect)

        # Rectangles avec un fond vert foncé et un espace entre eux
        rect_width, rect_height = 500, 50
        space_between_rects = 20
        border_radius = 10
        solo_rect = pygame.Rect((screen.get_width() - rect_width) // 2, (screen.get_height() - rect_height) // 2 - 25, rect_width, rect_height)
        ai_rect = pygame.Rect((screen.get_width() - rect_width) // 2, (screen.get_height() - rect_height) // 2 + rect_height + space_between_rects, rect_width, rect_height)

        pygame.draw.rect(screen, (56, 74, 12), solo_rect, border_radius=border_radius)
        pygame.draw.rect(screen, (56, 74, 12), ai_rect, border_radius=border_radius)

        # Affiche le texte sur les rectangles
        text_solo = self.font.render("Appuyez sur 's' pour jouer seul", True, (255, 255, 255))
        text_ia = self.font.render("Appuyez sur 'i' pour l'IA", True, (255, 255, 255))
        solo_text_rect = text_solo.get_rect(center=solo_rect.center)
        ai_text_rect = text_ia.get_rect(center=ai_rect.center)
        screen.blit(text_solo, solo_text_rect)
        screen.blit(text_ia, ai_text_rect)

        # Option pour afficher les scores avec ombre noire
        scores_text = self.font.render("Appuyez sur 'b' pour afficher les scores", True, (255, 255, 255))
        scores_rect = scores_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))

        # Ajout de l'ombre noire
        scores_rect_shadow = scores_rect.copy()
        scores_rect_shadow.x += 2
        scores_rect_shadow.y += 2
        scores_text_shadow = self.font.render("Appuyez sur 'b' pour afficher les scores", True, (0, 0, 0))

        screen.blit(scores_text_shadow, scores_rect_shadow)
        screen.blit(scores_text, scores_rect)

        pygame.display.update()

    def show_scores(self):
        score_screen = ScoreScreen()
        score_screen.run()
        
# Gestion du serpent
class Snake:

    # Corps du serpent
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

    # Tete serpent
    def graphic_head(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down

    # Queu Serpent
    def graphic_tail(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down

    # Corps serpent
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

# Gestion de la direction du serpent
    def move_snake(self):
        self.control()
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

# Contrôler le serpent avec les touches du clavier
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

# Parametre Fruit (pomme)
class Fruit:
    def __init__(self):
        self.randomize()

# Fonction du dessin de la pomme
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

# Fonction pour générer aléatoirement la position de la pomme
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

# classe principale du jeu
class MainGame:
    def __init__(self, mode):
        self.snake = Snake()
        self.fruit = Fruit()
        self.mode = mode
        self.score = 0
        self.total_apples_eaten = 0
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

# Vérification si il y a une collision avec la pomme
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.score += 1
            self.total_apples_eaten += 1

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

# Actions à effectuer en cas de fin de jeu
    def game_over(self):
        self.save_score()
        self.snake.reset()
        self.score = 0
        self.total_apples_eaten = 0

    def save_score(self):
        # Ajout d'une vérification pour éviter d'écrire un score de zéro
        if self.total_apples_eaten > 0:
            final_score_text = f'Total Apples Eaten: {self.total_apples_eaten}'
            with open('scores.txt', 'a') as file:
                file.write(f'{final_score_text}\n')

# Dessiner l'herbe sur le fond du jeu
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

# Dessiner le score à l'écran
    def draw_score(self):
        score_text = str(self.score)
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

# Définition de la classe d'écran des scores
class ScoreScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font("Font/Outwrite.ttf", 50)
        self.background = pygame.image.load("images/fond_scores.jpg").convert()
        self.delete_button_rect = pygame.Rect((screen.get_width() // 2 + 150, screen.get_height() // 4, 200, 50))
        self.delete_button_clicked = False

    def run(self):
        scores = self.load_scores()

# Gestion des actions (quitter, touches du clavier, clics de souris)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_d:
                        self.delete_scores()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        if self.delete_button_rect.collidepoint(event.pos):
                            self.delete_button_clicked = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.delete_button_clicked and self.delete_button_rect.collidepoint(event.pos):
                            self.delete_scores()
                            self.delete_button_clicked = False

            screen.blit(self.background, (0, 0))
            title_text = self.title_font.render("Scores :", True, (0, 128, 0))
            title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))
            title_shadow = self.title_font.render("Scores :", True, (0, 0, 0))
            title_rect_shadow = title_shadow.get_rect(center=(title_rect.centerx + 2, title_rect.centery + 2))
            screen.blit(title_shadow, title_rect_shadow)
            screen.blit(title_text, title_rect)
            y_position = screen.get_height() // 3
            for score in scores:
                score_text = self.font.render(score.strip(), True, (255, 255, 255))
                score_rect = score_text.get_rect(center=(screen.get_width() // 2, y_position))
                score_shadow = self.font.render(score.strip(), True, (0, 0, 0))
                score_rect_shadow = score_shadow.get_rect(center=(score_rect.centerx + 2, score_rect.centery + 2))
                screen.blit(score_shadow, score_rect_shadow)
                screen.blit(score_text, score_rect)
                y_position += 40

            # Ajouter le bouton "Delete Scores" à droite du titre "Scores"
            delete_text = self.font.render("Delete Scores", True, (255, 255, 255))
            pygame.draw.rect(screen, (56, 74, 12), self.delete_button_rect, border_radius=10)
            delete_rect = delete_text.get_rect(center=self.delete_button_rect.center)
            screen.blit(delete_text, delete_rect)

            pygame.display.flip()

# Initialise les scores lors de l'affichage
    def load_scores(self):
        with open('scores.txt', 'r') as file:
            scores = file.readlines()
        return scores
    
# Supprime les scores
    def delete_scores(self):
        with open('scores.txt', 'w') as file:
            file.write('')

# Pygame initialisation
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
main_game = None 

# Boucle à travers les scores et les affiche avec une couleur blanche (255, 255, 255)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if mode_selector.selected_mode == "Solo":
            # Gestion des touches du clavier pour le mode "Solo"
            if event.type == pygame.KEYDOWN and not main_game.snake.direction:
                if event.key == pygame.K_UP:
                    print("UP key pressed")
                    main_game.snake.direction = Vector2(0, -1)
                elif event.key == pygame.K_DOWN:
                    print("DOWN key pressed")
                    main_game.snake.direction = Vector2(0, 1)
                elif event.key == pygame.K_LEFT:
                    print("LEFT key pressed")
                    main_game.snake.direction = Vector2(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    print("RIGHT key pressed")
                    main_game.snake.direction = Vector2(1, 0)

    if mode_selector.selected_mode:
        if main_game is None:
            if mode_selector.selected_mode == "Solo":
                main_game = MainGame("Solo")
            elif mode_selector.selected_mode == "IA":
                main_game = MainGame("IA")

        main_game.update()

        screen.fill((175, 215, 70))
        main_game.draw_objects()
        pygame.display.update()
        clock.tick(10)