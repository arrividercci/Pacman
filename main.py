import pygame
import random
from collections import deque

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 30
ITEM_WALL = 1
ITEM_EMPTY = 0
ITEM_PILL = 2

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Ghost:
    def __init__(self, start_pos, level):
        self.position = start_pos
        self.level = level

    def get_neighbors(self, pos):
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for direction in directions:
            neighbor_pos = (pos[0] + direction[0], pos[1] + direction[1])
            if (0 <= neighbor_pos[0] < len(self.level) and
                    0 <= neighbor_pos[1] < len(self.level[0]) and
                    self.level[neighbor_pos[0]][neighbor_pos[1]] != ITEM_WALL):
                neighbors.append(neighbor_pos)
        return neighbors

    def bfs(self, target):
        queue = deque([self.position])
        visited = set()
        visited.add(self.position)
        parent = {self.position: None}

        while queue:
            current = queue.popleft()

            if current == target:
                break

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    parent[neighbor] = current

        path = []
        step = target
        while step:
            path.append(step)
            step = parent[step]

        path.reverse()
        return path

    def move_towards(self, target):
        path = self.bfs(target)
        if len(path) > 1:
            self.position = path[1]

    def dfs(self, target):
        stack = [self.position]
        visited = set()
        visited.add(self.position)
        parent = {self.position: None}

        while stack:
            current = stack.pop()

            if current == target:
                break

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    stack.append(neighbor)
                    visited.add(neighbor)
                    parent[neighbor] = current

        path = []
        step = target
        while step:
            path.append(step)
            step = parent[step]

        path.reverse()
        return path


class Game:
    def __init__(self):
        self.levels = [
            [
                [1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 3, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 1, 1, 1, 1, 1, 2, 1],
                [1, 2, 2, 2, 2, 2, 1, 2, 1],
                [1, 2, 1, 1, 1, 1, 1, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1]
            ],
            [
                [1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 3, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 1, 1, 1, 1, 1, 2, 1],
                [1, 2, 2, 2, 1, 1, 1, 2, 1],
                [1, 2, 1, 2, 2, 2, 1, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1]
            ],
            [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
                [1, 2, 1, 2, 2, 2, 2, 2, 2, 1, 2, 1],
                [1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1],
                [1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1],
                [1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1],
                [1, 2, 1, 2, 2, 2, 2, 2, 2, 1, 2, 1],
                [1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ],
            [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 3, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1],
                [1, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 1],
                [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
                [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1],
                [1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
        ]

        self.current_level = 0
        self.level = self.levels[self.current_level]
        self.pacman_position = [1, 1]
        self.ghosts = self.spawn_ghosts()
        self.direction = None
        self.pacman_move_delay = 0
        self.pacman_move_interval = 300
        self.ghost_move_delay = 0
        self.ghost_move_interval = 500

    def spawn_ghosts(self):
        ghosts = []
        num_ghosts = 1 if self.current_level < 2 else 2
        for _ in range(num_ghosts):
            ghost_position = self.find_spawn_position()
            ghosts.append(Ghost(start_pos=ghost_position, level=self.level))
        return ghosts

    def find_spawn_position(self):
        possible_positions = []
        for row in range(len(self.level)):
            for col in range(len(self.level[0])):
                if self.level[row][col] == ITEM_PILL or self.level[row][col] == ITEM_EMPTY:
                    if (row, col) != tuple(self.pacman_position):
                        possible_positions.append((row, col))
        return random.choice(possible_positions) if possible_positions else (1, 1)

    def check_pills(self):
        for row in self.level:
            if ITEM_PILL in row:
                return True
        return False

    def draw(self):
        screen.fill((0, 0, 0))

        for row in range(len(self.level)):
            for col in range(len(self.level[0])):
                if self.level[row][col] == ITEM_WALL:
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif self.level[row][col] == ITEM_PILL:
                    pygame.draw.circle(screen, (0, 255, 0),
                                       (col * CELL_SIZE + CELL_SIZE // 2,
                                        row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
                elif self.level[row][col] == ITEM_EMPTY:
                    pygame.draw.rect(screen, (0, 0, 0),
                                     (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for ghost in self.ghosts:
            pygame.draw.rect(screen, (255, 0, 0),
                             (ghost.position[1] * CELL_SIZE, ghost.position[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.draw.circle(screen, (255, 255, 0),
                           (self.pacman_position[1] * CELL_SIZE + CELL_SIZE // 2,
                            self.pacman_position[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

        pygame.display.flip()

    def move_pacman(self):
        if self.direction:
            new_position = self.pacman_position[:]
            if self.direction == 'UP':
                new_position[0] -= 1
            elif self.direction == 'DOWN':
                new_position[0] += 1
            elif self.direction == 'LEFT':
                new_position[1] -= 1
            elif self.direction == 'RIGHT':
                new_position[1] += 1

            if (0 <= new_position[0] < len(self.level) and
                    0 <= new_position[1] < len(self.level[0]) and
                    self.level[new_position[0]][new_position[1]] != ITEM_WALL):
                self.pacman_position = new_position

                if self.level[new_position[0]][new_position[1]] == ITEM_PILL:
                    self.level[new_position[0]][new_position[1]] = ITEM_EMPTY

    def move_ghosts(self):
        for i, ghost in enumerate(self.ghosts):
            if i == 0:
                ghost.move_towards(tuple(self.pacman_position))
            else:
                future_position = self.predict_pacman_position(steps=1)
                neighbors = ghost.get_neighbors(ghost.position)
                if future_position in neighbors:
                    ghost.move_towards(future_position)
                else:
                    ghost.move_towards(tuple(self.pacman_position))

    def predict_pacman_position(self, steps=1):
        pacman_pos = list(self.pacman_position)
        if self.direction == 'UP':
            pacman_pos[1] -= steps
        elif self.direction == 'DOWN':
            pacman_pos[1] += steps
        elif self.direction == 'LEFT':
            pacman_pos[0] -= steps
        elif self.direction == 'RIGHT':
            pacman_pos[0] += steps

        pacman_pos[0] = max(0, min(pacman_pos[0], len(self.level[0]) - 1))
        pacman_pos[1] = max(0, min(pacman_pos[1], len(self.level) - 1))

        if self.level[pacman_pos[1]][pacman_pos[0]] == 1:
            return tuple(self.pacman_position)

        return tuple(pacman_pos)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.direction = 'UP'
                    elif event.key == pygame.K_DOWN:
                        self.direction = 'DOWN'
                    elif event.key == pygame.K_LEFT:
                        self.direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT:
                        self.direction = 'RIGHT'

            self.pacman_move_delay += 1
            if self.pacman_move_delay >= self.pacman_move_interval:
                self.move_pacman()
                self.pacman_move_delay = 0

            self.ghost_move_delay += 1
            if self.ghost_move_delay >= self.ghost_move_interval:
                self.move_ghosts()
                self.ghost_move_delay = 0

            if not self.check_pills():
                print("Congratulations! You've completed the level.")
                self.current_level += 1
                if self.current_level < len(self.levels):
                    self.level = self.levels[self.current_level]
                    self.pacman_position = [1, 1]
                    self.ghosts = self.spawn_ghosts()
                else:
                    print("You've completed all levels! Game Over.")
                    running = False

            if self.is_game_over():
                print("Game Over! The ghost caught Pacman.")
                running = False

            self.draw()

        pygame.quit()

    def is_game_over(self):
        return any(self.pacman_position == list(ghost.position) for ghost in self.ghosts)

if __name__ == "__main__":
    game = Game()
    game.run()
