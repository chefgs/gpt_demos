from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import pygame
import random
import threading

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

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
FPS = 60

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

def reset_game():
    global player_y, player_y_velocity, hurdles, tools, score, last_hurdle_time, last_tool_time
    player_y = SCREEN_HEIGHT - player_size - 20
    player_y_velocity = 0
    hurdles = []
    tools = []
    score = 0
    last_hurdle_time = 0
    last_tool_time = 0

def game_over_screen():
    global running
    running = False
    socketio.emit('game_over', {'message': 'Game Over! Press R to Restart'})

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start_game')
def start_game():
    global running
    running = True
    game_thread = threading.Thread(target=game_loop)
    game_thread.start()

@socketio.on('restart_game')
def restart_game():
    reset_game()
    start_game()

def game_loop():
    global player_y_velocity, last_hurdle_time, last_tool_time, score, running

    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.y + player_size >= SCREEN_HEIGHT - 20:
                    player_y_velocity = jump_power

        # Player Movement
        player_y_velocity += gravity
        player.y += player_y_velocity
        if player.y + player_size > SCREEN_HEIGHT - 20:
            player.y = SCREEN_HEIGHT - player_size - 20

        # Hurdle Logic
        current_time = pygame.time.get_ticks()
        if current_time - last_hurdle_time > hurdle_spawn_rate:
            hurdle_x = SCREEN_WIDTH
            hurdle_y = SCREEN_HEIGHT - hurdle_height - 20
            hurdles.append(pygame.Rect(hurdle_x, hurdle_y, hurdle_width, hurdle_height))
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

        # Emit game state to client
        game_state = {
            'player': {'x': player.x, 'y': player.y, 'size': player_size},
            'hurdles': [{'x': h.x, 'y': h.y, 'width': h.width, 'height': h.height} for h in hurdles],
            'tools': [{'x': t.x, 'y': t.y, 'size': tool_size} for t in tools],
            'score': score
        }
        socketio.emit('game_state', game_state)

        # Cap the Frame Rate
        clock.tick(FPS)

if __name__ == '__main__':
    socketio.run(app, debug=True)