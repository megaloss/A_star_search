import pygame
import random
from queue import PriorityQueue
import time
pygame.init()
WIDTH = 600
HEIGHT = 600
GRAY = (55, 55, 55)
WHITE = (255, 255, 255)
BLUE = (0, 0, 155)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (100, 55, 0)
win = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("comicsans", 30, True)
pygame.display.set_caption("Search1")
clock = pygame.time.Clock()
width = 9
height = 9


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.blocked = False
        self.neighbors = []
        self.start = False
        self.target = False

    def block(self):
        self.blocked = True

    def get_neighbors(self, grid):

        if self.x > 0 and not grid[self.x-1][self.y].blocked:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.x < WIDTH/10-1 and not grid[self.x+1][self.y].blocked:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.y > 0 and not grid[self.x][self.y-1].blocked:
            self.neighbors.append(grid[self.x][self.y-1])
        if self.y < HEIGHT/10-1 and not grid[self.x][self.y+1].blocked:
            self.neighbors.append(grid[self.x][self.y+1])

    def get_dist(self, other):
        return abs(self.x-other.x)+abs(self.y-other.y)


def create_grid(lines, cols):
    grid = []
    for col in range(cols):
        grid.append([])
        for line in range(lines):
            point = Point(col, line)
            grid[col].append(point)
    return grid


def draw_grid():
    for i in range(0, WIDTH, 10):
        pygame.draw.line(win, GRAY, (i, 0), (i, WIDTH))
        pygame.draw.line(win, GRAY, (0, i), (WIDTH, i))
        pygame.display.update()


def draw_maze(grid):
    for line in grid:
        for point in line:
            if point.blocked:
                draw_point(point, RED)
                pygame.display.update()


def draw_point(point, color):

    pygame.draw.rect(win, color, (point.x*10+2, point.y*10+2, 7, 7), 0)
    pygame.display.update()


def create_maze(grid, num=30, length=30):
    for _ in range(num):
        ln = random.randint(0, length)
        dir_x, dir_y = random.choice([(0, 1), (1, 0)])
        start_x, start_y = (random.randint(0, len(grid)), random.randint(0, len(grid[0])))
        end_x, end_y = (start_x + ln * dir_x, start_y + ln * dir_y)
        for i in range(start_x, min(60, end_x+1)):
            for j in range(start_y, min(60, end_y+1)):
                grid[i][j].block()
    return grid


def create_point(grid):
    while True:
        x, y = (random.randint(0, 59), random.randint(0, 59))
        if not grid[x][y].blocked:
            point = grid[x][y]
            return point


def reconstruct_path(came_from, current):

    while current in came_from:
        current = came_from[current]
        draw_point(current, GREEN)


def main():
    # prepare a maze
    draw_grid()
    grid = create_grid(WIDTH//10, HEIGHT//10)
    grid = create_maze(grid, 20, 50)
    draw_maze(grid)
    target = create_point(grid)
    target.target = True
    start = create_point(grid)
    start.start = True
    draw_point(target, GREEN)
    draw_point(start, YELLOW)
    time.sleep(3)

    # start here
    for line in grid:
        for point in line:
            point.get_neighbors(grid)
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {point: float("inf") for row in grid for point in row}
    g_score[start] = 0
    f_score = {point: float("inf") for row in grid for point in row}
    f_score[start] = start.get_dist(target)
    open_set_hash = {start}

    while not open_set.empty():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Get the point closest to the target
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == target:
            reconstruct_path(came_from, target)
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:  # we found shorter path to this point - update scores for the point
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + neighbor.get_dist(target)
                if neighbor not in open_set_hash and neighbor != start:  # if we have not been here yet
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != target:
                        draw_point(neighbor, BLUE)  # visited

        if current != start and current != target:
            draw_point(current, ORANGE)  # checked all it's neighbors
    print('NOT FOUND !')


main()
time.sleep(7)
