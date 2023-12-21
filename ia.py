from pygame.math import Vector2
import random

class IA:
    def __init__(self):
        self.directions = [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]

    def get_next_move(self, snake, fruit):
        # Direction de la tête du serpent vers la pomme
        to_fruit = fruit.pos - snake.body[0]

        # Direction en fonction de la position relative de la pomme
        if to_fruit.x > 0:
            next_direction = Vector2(1, 0)
        elif to_fruit.x < 0:
            next_direction = Vector2(-1, 0)
        elif to_fruit.y > 0:
            next_direction = Vector2(0, 1)
        elif to_fruit.y < 0:
            next_direction = Vector2(0, -1)
        else:
            # Si la tête est déjà sur la pomme, elle choisie une direction aléatoire
            next_direction = random.choice(self.directions)

        return next_direction