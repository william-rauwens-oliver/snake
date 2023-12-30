from pygame.math import Vector2
import heapq, random

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash((self.position.x, self.position.y))

class IA:

# Initialise l'IA avec les directions possibles (droite, gauche, haut, bas)
    def __init__(self):
        self.directions = [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]

    def get_next_move(self, snake, fruit):
# L'IA trouve le chemin le plus court vers la pomme
        path = self.find_path(snake.body[0], fruit.pos, snake.body)
        
# L'IA choisi la prochaine direction en fonction du premier mouvement dans le chemin
        if path and len(path) > 1:
            next_direction = path[1] - path[0]
            return next_direction

# Si le chemin est vide ou n'a qu'un élément, l'IA choisi une direction aléatoire
        return random.choice(self.directions)

    def find_path(self, start, goal, obstacles):
        open_set = []
        closed_set = set()

        start_node = Node(start)
        goal_node = Node(goal)

        heapq.heappush(open_set, start_node)

        while open_set:
            current_node = heapq.heappop(open_set)

            if current_node.position == goal_node.position:
                path = []
                while current_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                return path[::-1]

# Parcours les directions possibles pour les voisins du nœud actuel
            closed_set.add(current_node)

            for direction in self.directions:
                neighbor_position = current_node.position + direction
                neighbor_node = Node(neighbor_position, current_node)

# Vérifie si le voisin est dans la grille et n'est pas un obstacle
                if (
                    0 <= neighbor_position.x < 20
                    and 0 <= neighbor_position.y < 20
                    and neighbor_node not in closed_set
                    and neighbor_position not in obstacles
                ):
                    neighbor_node.g = current_node.g + 1
                    neighbor_node.h = abs(neighbor_node.position.x - goal_node.position.x) + abs(
                        neighbor_node.position.y - goal_node.position.y
                    )

                    if neighbor_node not in open_set:
                        heapq.heappush(open_set, neighbor_node)

# Si la file de priorité est vide et l'objectif n'est pas atteint, retourne un chemin vide
        return []