import pygame
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Automation Runner")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.SysFont('Arial', 24)

# Clock
clock = pygame.time.Clock()
FPS = 30

# Player
player_size = 50
player_x = 100
player_y = SCREEN_HEIGHT - player_size - 20
player_y_velocity = 0
gravity = 1
jump_power = -15
player = pygame.Rect(player_x, player_y, player_size, player_size)

# Hurdles
hurdle_width = 30
hurdle_height = 50
hurdles = []
hurdle_speed = 10
hurdle_spawn_rate = 1500  # in milliseconds
last_hurdle_time = 0

# Automation Tools (Points)
tool_size = 30
tools = []
tool_speed = 10
tool_spawn_rate = 2000  # in milliseconds
last_tool_time = 0

# Score
score = 0
level = 1
game_level = "easy"

def reset_game():
    global player_y, player_y_velocity, hurdles, tools, score, last_hurdle_time, last_tool_time, level, game_level
    player_y = SCREEN_HEIGHT - player_size - 20
    player_y_velocity = 0
    hurdles = []
    tools = []
    score = 0
    last_hurdle_time = 0
    last_tool_time = 0
    level = 1
    game_level = show_menu()

def game_over_screen():
    screen.fill(WHITE)
    game_over_text = font.render("Game Over! Press 'R' to Restart", True, BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    reset_game()

def draw_stickman(surface, x, y):
    # Head
    pygame.draw.circle(surface, BLACK, (x + 25, y + 10), 10)
    # Body
    pygame.draw.line(surface, BLACK, (x + 25, y + 20), (x + 25, y + 50), 2)
    # Arms
    pygame.draw.line(surface, BLACK, (x + 25, y + 30), (x + 15, y + 40), 2)
    pygame.draw.line(surface, BLACK, (x + 25, y + 30), (x + 35, y + 40), 2)
    # Legs
    pygame.draw.line(surface, BLACK, (x + 25, y + 50), (x + 15, y + 70), 2)
    pygame.draw.line(surface, BLACK, (x + 25, y + 50), (x + 35, y + 70), 2)

def show_menu():
    screen.fill(WHITE)
    title_text = font.render("Choose Game Level", True, BLACK)
    easy_text = font.render("1. Easy", True, BLACK)
    medium_text = font.render("2. Medium", True, BLACK)
    hard_text = font.render("3. Hard", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))
    screen.blit(easy_text, (SCREEN_WIDTH // 2 - easy_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
    screen.blit(medium_text, (SCREEN_WIDTH // 2 - medium_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(hard_text, (SCREEN_WIDTH // 2 - hard_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "easy"
                if event.key == pygame.K_2:
                    return "medium"
                if event.key == pygame.K_3:
                    return "hard"

def spawn_hurdle():
    global hurdle_spawn_rate
    hurdle_x = SCREEN_WIDTH
    if game_level == "easy":
        hurdle_y = SCREEN_HEIGHT - hurdle_height - 20
    else:
        hurdle_y = random.randint(50, SCREEN_HEIGHT - hurdle_height - 20)
    hurdles.append(pygame.Rect(hurdle_x, hurdle_y, hurdle_width, hurdle_height))
    if game_level == "hard":
        hurdle_spawn_rate = 1000  # Increase hurdle spawn rate for hard level

# Game Loop
running = True
game_level = show_menu()
while running:
    screen.fill(WHITE)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_y + player_size >= SCREEN_HEIGHT - 20:
                player_y_velocity = jump_power

    # Player Movement
    player_y_velocity += gravity
    player.y += player_y_velocity
    if player.y + player_size > SCREEN_HEIGHT - 20:
        player.y = SCREEN_HEIGHT - player_size - 20

    # Hurdle Logic
    current_time = pygame.time.get_ticks()
    if current_time - last_hurdle_time > hurdle_spawn_rate:
        spawn_hurdle()
        last_hurdle_time = current_time

    for hurdle in hurdles[:]:
        hurdle.x -= hurdle_speed
        if hurdle.x + hurdle_width < 0:
            hurdles.remove(hurdle)
        if player.colliderect(hurdle):
            game_over_screen()

    # Tool Logic
    if current_time - last_tool_time > tool_spawn_rate:
        tool_x = SCREEN_WIDTH
        tool_y = random.randint(50, SCREEN_HEIGHT - 50)
        tools.append(pygame.Rect(tool_x, tool_y, tool_size, tool_size))
        last_tool_time = current_time

    for tool in tools[:]:
        tool.x -= tool_speed
        if tool.x + tool_size < 0:
            tools.remove(tool)
        if player.colliderect(tool):
            tools.remove(tool)
            score += 10  # Increase score

    # Level Progression
    if score >= 200 * level:
        level += 1
        if level > 3:
            level = 3  # Cap the level at 3
        if level == 2:
            game_level = "medium"
        elif level == 3:
            game_level = "hard"
        reset_game()

    # Draw Player (Stickman)
    draw_stickman(screen, player.x, player.y)

    # Draw Hurdles
    for hurdle in hurdles:
        pygame.draw.rect(screen, RED, hurdle)

    # Draw Tools
    for tool in tools:
        pygame.draw.rect(screen, GREEN, tool)

    # Draw Score
    score_text = font.render(f"Score: {score} Level: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update Display
    pygame.display.flip()

    # Cap the Frame Rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()