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
            # Si la tête est déjà sur la pomme, elle choisit la direction vers la pomme
            next_direction = self.direction_towards_fruit(snake.body[0], fruit.pos)

        # Vérifier que la direction choisie ne mène pas à la collision avec le corps
        if self.is_valid_direction(snake, next_direction):
            return next_direction
        else:
            # Si la direction choisie mène à la collision, choisir une direction parmi celles valides ou la première direction
            valid_directions = [d for d in self.directions if self.is_valid_direction(snake, d)]
            return random.choice(valid_directions) if valid_directions else self.directions[0]

    def is_valid_direction(self, snake, direction):
        # Nouvelle direction ne mène pas à la collision avec le corps du serpent
        next_head = snake.body[0] + direction
        return next_head not in snake.body[1:]

    def direction_towards_fruit(self, head, fruit_pos):
        to_fruit = fruit_pos - head

        # Choisir la direction en fonction de la position relative de la pomme
        if abs(to_fruit.x) > abs(to_fruit.y):
            return Vector2(1, 0) if to_fruit.x > 0 else Vector2(-1, 0)
        else:
            return Vector2(0, 1) if to_fruit.y > 0 else Vector2(0, -1)