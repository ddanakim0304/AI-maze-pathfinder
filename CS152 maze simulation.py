import pygame
import random
import heapq

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 40
GRID_WIDTH = 15
GRID_HEIGHT = 15
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Simulation with A* Pathfinding")

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

def generate_maze():
    grid = [[Cell(x, y) for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
    stack = []
    current = grid[0][0]
    current.visited = True

    # Standard depth-first maze generation with random choices for creating the initial maze
    while True:
        unvisited = []
        x, y = current.x, current.y

        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and not grid[nx][ny].visited:
                unvisited.append(grid[nx][ny])

        if unvisited:
            next_cell = random.choice(unvisited)
            stack.append(current)
            
            if next_cell.x > current.x:
                current.walls['right'] = False
                next_cell.walls['left'] = False
            elif next_cell.x < current.x:
                current.walls['left'] = False
                next_cell.walls['right'] = False
            elif next_cell.y > current.y:
                current.walls['bottom'] = False
                next_cell.walls['top'] = False
            else:
                current.walls['top'] = False
                next_cell.walls['bottom'] = False

            current = next_cell
            current.visited = True
        elif stack:
            current = stack.pop()
        else:
            break

    # Randomly remove additional walls to create more paths ("holes")
    for _ in range(GRID_WIDTH * GRID_HEIGHT):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        direction = random.choice(['top', 'right', 'bottom', 'left'])

        # Remove the chosen wall if it's not already removed and if the neighboring cell exists
        if direction == 'top' and y > 0:
            grid[x][y].walls['top'] = False
            grid[x][y-1].walls['bottom'] = False
        elif direction == 'right' and x < GRID_WIDTH - 1:
            grid[x][y].walls['right'] = False
            grid[x+1][y].walls['left'] = False
        elif direction == 'bottom' and y < GRID_HEIGHT - 1:
            grid[x][y].walls['bottom'] = False
            grid[x][y+1].walls['top'] = False
        elif direction == 'left' and x > 0:
            grid[x][y].walls['left'] = False
            grid[x-1][y].walls['right'] = False

    # Goal cell
    goal = grid[GRID_WIDTH // 2][GRID_HEIGHT // 2]
    goal.walls = {'top': False, 'right': False, 'bottom': False, 'left': False}

    return grid


def draw_maze(grid):
    screen.fill(WHITE)
    for row in grid:
        for cell in row:
            x, y = cell.x * CELL_SIZE, cell.y * CELL_SIZE
            if cell.walls['top']:
                pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y))
            if cell.walls['right']:
                pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE))
            if cell.walls['bottom']:
                pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE))
            if cell.walls['left']:
                pygame.draw.line(screen, BLACK, (x, y), (x, y + CELL_SIZE))

def heuristic(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return dx + dy

def get_neighbors(grid, node):
    x, y = node
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
            if dx == 1 and not grid[x][y].walls['right']:
                neighbors.append((nx, ny))
            elif dx == -1 and not grid[x][y].walls['left']:
                neighbors.append((nx, ny))
            elif dy == 1 and not grid[x][y].walls['bottom']:
                neighbors.append((nx, ny))
            elif dy == -1 and not grid[x][y].walls['top']:
                neighbors.append((nx, ny))
    return neighbors

def a_star(grid, start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    visited = set()

    while frontier:
        current = heapq.heappop(frontier)[1]
        visited.add(current)

        if current == goal:
            break

        for next in get_neighbors(grid, current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current

        # Visualize the search process
        draw_maze(grid)
        draw_search_process(start, goal, visited, frontier, came_from, cost_so_far)
        pygame.display.flip()
        pygame.time.wait(50)
    
    # Reconstruct path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path, visited

def draw_search_process(start, goal, visited, frontier, came_from, cost_so_far):
    # Draw visited cells
    for cell in visited:
        pygame.draw.rect(screen, YELLOW, (cell[0] * CELL_SIZE + 5, cell[1] * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10))
        # Calculate Manhattan distance from the goal
        manhattan_distance = heuristic(cell, goal)
        font = pygame.font.Font(None, 20)
        text = font.render(f"M: {manhattan_distance}", True, BLACK)
        screen.blit(text, (cell[0] * CELL_SIZE + 10, cell[1] * CELL_SIZE + 20))

    # Draw frontier cells
    for _, cell in frontier:
        pygame.draw.rect(screen, PURPLE, (cell[0] * CELL_SIZE + 5, cell[1] * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10))
        # Draw heuristic calculation
        heuristic_value = heuristic(cell, goal) + cost_so_far.get(cell, 0)
        font = pygame.font.Font(None, 20)
        text = font.render(f"H: {heuristic_value}", True, BLACK)
        screen.blit(text, (cell[0] * CELL_SIZE + 10, cell[1] * CELL_SIZE + 20))

    # Draw start and goal
    pygame.draw.rect(screen, GREEN, (start[0] * CELL_SIZE, start[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (goal[0] * CELL_SIZE, goal[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw current path
    current = goal
    while current in came_from and came_from[current] is not None:
        pygame.draw.line(screen, BLUE, 
                         (current[0] * CELL_SIZE + CELL_SIZE // 2, current[1] * CELL_SIZE + CELL_SIZE // 2),
                         (came_from[current][0] * CELL_SIZE + CELL_SIZE // 2, came_from[current][1] * CELL_SIZE + CELL_SIZE // 2),
                         5)
        current = came_from[current]

def draw_restart_button():
    font = pygame.font.Font(None, 36)
    text = font.render("Restart", True, WHITE, BLACK)
    button_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 30))
    screen.blit(text, button_rect)
    return button_rect

def check_button_click(button_rect, pos):
    return button_rect.collidepoint(pos)

def main():
    grid = generate_maze()

    # Randomly choose one of the four corner positions as the start
    start = random.choice([(0, 0), (0, GRID_HEIGHT - 1), (GRID_WIDTH - 1, GRID_HEIGHT - 1), (GRID_WIDTH - 1, 0)])
    
    goal = (GRID_WIDTH // 2, GRID_HEIGHT // 2)

    path, visited = a_star(grid, start, goal)

    running = True
    path_index = 0
    clock = pygame.time.Clock()
    cost_so_far = {}  # Initialize the cost_so_far dictionary

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the restart button is clicked
                if check_button_click(restart_button_rect, pygame.mouse.get_pos()):
                    # Regenerate the maze
                    grid = generate_maze()
                    start = random.choice([(0, 0), (0, GRID_HEIGHT - 1), (GRID_WIDTH - 1, GRID_HEIGHT - 1), (GRID_WIDTH - 1, 0)])  # Randomize start again
                    path, visited = a_star(grid, start, goal)
                    path_index = 0  # Reset the path index

        # Draw maze and restart button
        draw_maze(grid)
        restart_button_rect = draw_restart_button()  # Draw the button each frame

        # Draw search process and final path
        draw_search_process(start, goal, visited, [], {}, cost_so_far)

        for i in range(path_index):
            x, y = path[i]
            pygame.draw.rect(screen, BLUE, (x * CELL_SIZE + 5, y * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10))

        pygame.display.flip()

        if path_index < len(path):
            path_index += 1

        clock.tick(10)  # Limit to 10 frames per second

    pygame.quit()


if __name__ == "__main__":
    main()