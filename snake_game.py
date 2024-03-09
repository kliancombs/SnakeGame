import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH
GRID_HEIGHT = HEIGHT
FPS = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

font = pygame.font.Font(None, 36)


class Snake:
    """
    Base class to handle snake functionality
    """

    def __init__(self):
        self.size = 1
        self.body = [(WIDTH // 2 - GRID_SIZE, HEIGHT // 2)]  # Start slightly left of center
        self.direction = ""

    def move(self):
        """
        Method to move snake within the screen
        """
        head = self.body[0]
        x, y = head
        if self.direction == "UP":
            y -= GRID_SIZE
        elif self.direction == "DOWN":
            y += GRID_SIZE
        elif self.direction == "RIGHT":
            x += GRID_SIZE
        elif self.direction == "LEFT":
            x -= GRID_SIZE
        self.body.insert(0, (x, y))
        if len(self.body) > self.size:
            self.body.pop()

    def change_direction(self, new_direction):
        """
        Method to change direction of player within the screen

        Params:
            new_direction: str
        """
        if new_direction in ("UP", "DOWN", "RIGHT", "LEFT"):
            if (new_direction == "UP" and self.direction != "DOWN") or \
                (new_direction == "DOWN" and self.direction != "UP")or \
                (new_direction == "LEFT" and self.direction != "RIGHT") or\
                (new_direction == "RIGHT" and self.direction != "LEFT"):
                self.direction = new_direction

    def eat_food(self):
        """
        Method to increase snake size after eating food
        """
        self.size += 1

    def check_collision(self):
        """
        Method to check collision with self or walls

        Returns:
            bool
        """
        head = self.body[0]
        if (head[0] < 0) or (head[0] >= WIDTH) or (head[1] < 0) or (head[1] >= HEIGHT):
            return True
        if head in self.body[1:]:  # check collision with the rest of the body
            return True
        return False    

    def draw(self):
        """
        Method to draw the snake within the screen
        """
        for x, y in self.body:
            pygame.draw.rect(window, GREEN, (x, y, GRID_SIZE, GRID_SIZE))


class Food:
    """
    Base class to handle food generation
    """

    def __init__(self):
        self.position = self.generate_position()

    def generate_position(self):
        """
        Method to generate food position at random

        Returns:
            int, int
        """
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_SIZE - 1) * GRID_SIZE
        return x, y

    def draw(self):
        """
        Method to draw food within the screen
        """        
        pygame.draw.rect(
            window, RED,
            (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))


snake = Snake()
food = Food()

score = 0

running = True
clock = pygame.time.Clock()
game_over = False

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP:
        snake.change_direction("up")
      elif event.key == pygame.K_DOWN:
        snake.change_direction("DOWN")
      elif event.key == pygame.K_LEFT:
        snake.change_direction("LEFT")
      elif event.key == pygame.K_RIGHT:
        snake.change_direction("RIGHT")

    if not game_over:
        snake.move()

    if snake.body[0] == food.position:
      snake.eat_food()
      food.position = food.generate_position()
      score += 1

    if snake.check_collision():
      game_over = True

  window.fill(BLACK)

  snake.draw()
  food.draw()

  score_text = font.render(f"Score :{score}", True, WHITE)
  window.blit(score_text, (10, 10))

  if game_over:
    game_over_text = font.render("Game Over", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    window.blit(game_over_text, game_over_rect)

  pygame.display.update()
  clock.tick(FPS)

pygame.quit()