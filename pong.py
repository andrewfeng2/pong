import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Pong Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
RED = (255, 50, 50)
GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)

# Game objects
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 90

# Game variables
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 0
player_score = 0
opponent_score = 0
ai_difficulty = 0.8  # AI difficulty (0.0 to 1.0)
game_font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 24)
score_limit = 5  # First to reach this score wins
game_active = True  # Track if game is in active play state
countdown_timer = 0  # Timer for countdown between points

# Paddle positions
player = pygame.Rect(WIDTH - 20, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent = pygame.Rect(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_RADIUS, HEIGHT//2 - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)

# Particle system
particles = []
particle_colors = [(255, 255, 255), (200, 200, 255), (150, 150, 255)]

def create_particles(x, y, count=10):
    for _ in range(count):
        particles.append({
            'x': x,
            'y': y,
            'dx': random.uniform(-2, 2),
            'dy': random.uniform(-2, 2),
            'radius': random.uniform(2, 5),
            'alpha': 255,
            'color': random.choice(particle_colors)
        })

def update_particles():
    for particle in particles[:]:
        particle['x'] += particle['dx']
        particle['y'] += particle['dy']
        particle['alpha'] -= 5
        
        if particle['alpha'] <= 0:
            particles.remove(particle)

def draw_particles():
    for particle in particles:
        color = particle['color']
        alpha = int(particle['alpha'])
        surface = pygame.Surface((particle['radius']*2, particle['radius']*2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (*color, alpha), (particle['radius'], particle['radius']), particle['radius'])
        win.blit(surface, (particle['x'] - particle['radius'], particle['y'] - particle['radius']))

def ball_restart():
    global ball_speed_x, ball_speed_y, countdown_timer, game_active
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_speed_y = 7 * random.choice((1, -1))
    ball_speed_x = 7 * random.choice((1, -1))
    create_particles(WIDTH//2, HEIGHT//2, 20)
    
    # Set a countdown timer before the ball starts moving again
    countdown_timer = 60  # 1 second at 60 FPS
    game_active = False  # Pause gameplay briefly

def handle_input():
    global player_speed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.top > 0:
        player_speed = -7
    elif keys[pygame.K_DOWN] and player.bottom < HEIGHT:
        player_speed = 7
    else:
        player_speed = 0

def move_opponent_ai():
    global opponent_speed
    
    # Predict where the ball will be
    if ball_speed_x < 0:  # Ball is moving towards AI
        # Calculate time until ball reaches opponent's y-position
        time_to_reach = (opponent.centerx - ball.centerx) / -ball_speed_x if ball_speed_x != 0 else 0
        
        # Predict y-position
        predicted_y = ball.centery + (ball_speed_y * time_to_reach)
        
        # Add some randomness based on difficulty
        error = random.uniform(-100, 100) * (1 - ai_difficulty)
        target_y = predicted_y + error
        
        # Bound the target within the screen
        target_y = max(PADDLE_HEIGHT // 2, min(HEIGHT - PADDLE_HEIGHT // 2, target_y))
        
        # Move towards the predicted position
        if opponent.centery < target_y - 10:
            opponent_speed = min(7, (target_y - opponent.centery) * 0.1)
        elif opponent.centery > target_y + 10:
            opponent_speed = max(-7, (target_y - opponent.centery) * 0.1)
        else:
            opponent_speed = 0
    else:
        # When ball is moving away, return to center with some randomness
        if abs(opponent.centery - HEIGHT//2) > 50:
            opponent_speed = 3 if opponent.centery < HEIGHT//2 else -3
        else:
            opponent_speed = 0

def update_game():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, countdown_timer, game_active
    
    # Check if game is over (someone reached score limit)
    if player_score >= score_limit or opponent_score >= score_limit:
        return  # Don't update game if someone has won
    
    # Handle countdown timer
    if countdown_timer > 0:
        countdown_timer -= 1
        if countdown_timer == 0:
            game_active = True
        return
    
    # Only update game if active
    if not game_active:
        return
        
    # Move paddles
    player.y += player_speed
    opponent.y += opponent_speed
    
    # Keep paddles on screen
    if player.top <= 0:
        player.top = 0
    if player.bottom >= HEIGHT:
        player.bottom = HEIGHT
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= HEIGHT:
        opponent.bottom = HEIGHT

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
        create_particles(ball.centerx, ball.top if ball.top <= 0 else ball.bottom, 5)
        wall_sound.play()

    # Ball collision with paddles
    if ball.colliderect(player):
        # Calculate new angle based on where the ball hits the paddle
        relative_intersect_y = (player.centery - ball.centery) / (PADDLE_HEIGHT / 2)
        bounce_angle = relative_intersect_y * (math.pi/4)  # Max 45 degrees
        
        # Calculate new velocities
        speed = math.sqrt(ball_speed_x**2 + ball_speed_y**2) * 1.05  # Slight speed increase
        ball_speed_x = -speed * math.cos(bounce_angle)
        ball_speed_y = -speed * math.sin(bounce_angle)
        
        create_particles(ball.right, ball.centery, 10)
        paddle_sound.play()
        
    if ball.colliderect(opponent):
        # Similar angle calculation for opponent paddle
        relative_intersect_y = (opponent.centery - ball.centery) / (PADDLE_HEIGHT / 2)
        bounce_angle = relative_intersect_y * (math.pi/4)
        
        speed = math.sqrt(ball_speed_x**2 + ball_speed_y**2) * 1.05
        ball_speed_x = speed * math.cos(bounce_angle)
        ball_speed_y = -speed * math.sin(bounce_angle)
        
        create_particles(ball.left, ball.centery, 10)
        paddle_sound.play()

    # Score points
    if ball.left <= 0:
        player_score += 1
        score_sound.play()
        ball_restart()
    if ball.right >= WIDTH:
        opponent_score += 1
        score_sound.play()
        ball_restart()

def draw_game():
    # Background
    win.fill(BLACK)
    
    # Draw court lines
    pygame.draw.rect(win, GRAY, (0, 0, WIDTH, HEIGHT), 10)
    pygame.draw.aaline(win, LIGHT_GRAY, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    pygame.draw.circle(win, LIGHT_GRAY, (WIDTH//2, HEIGHT//2), 70, 1)
    
    # Draw paddles with gradient effect
    for i in range(PADDLE_HEIGHT):
        color_intensity = 150 + int(105 * (i / PADDLE_HEIGHT))
        pygame.draw.line(win, (color_intensity, 50, 50), 
                         (player.left, player.top + i), 
                         (player.right, player.top + i))
        pygame.draw.line(win, (50, 50, color_intensity), 
                         (opponent.left, opponent.top + i), 
                         (opponent.right, opponent.top + i))
    
    # Draw ball with glow effect
    glow_radius = BALL_RADIUS * 2
    glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
    for r in range(glow_radius, 0, -1):
        alpha = 100 if r == BALL_RADIUS else max(0, 50 - (glow_radius - r) * 10)
        pygame.draw.circle(glow_surface, (255, 255, 255, alpha), (glow_radius, glow_radius), r)
    win.blit(glow_surface, (ball.centerx - glow_radius, ball.centery - glow_radius))
    pygame.draw.circle(win, WHITE, ball.center, BALL_RADIUS)
    
    # Draw particles
    draw_particles()
    
    # Draw scores
    player_text = game_font.render(str(player_score), True, RED)
    win.blit(player_text, (WIDTH//2 + 30, 20))
    
    opponent_text = game_font.render(str(opponent_score), True, BLUE)
    win.blit(opponent_text, (WIDTH//2 - 50, 20))
    
    # Draw player labels
    player_label = small_font.render("PLAYER", True, RED)
    win.blit(player_label, (WIDTH - 80, HEIGHT - 30))
    
    ai_label = small_font.render("AI", True, BLUE)
    win.blit(ai_label, (30, HEIGHT - 30))
    
    # Draw difficulty indicator
    difficulty_text = small_font.render(f"AI Difficulty: {int(ai_difficulty * 100)}%", True, WHITE)
    win.blit(difficulty_text, (WIDTH//2 - 70, HEIGHT - 30))
    
    # Draw countdown if active
    if countdown_timer > 0:
        count = countdown_timer // 20 + 1  # Convert frames to visible number (3,2,1)
        if count <= 3:  # Only show 3,2,1
            count_text = game_font.render(str(count), True, WHITE)
            text_rect = count_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            win.blit(count_text, text_rect)
    
    # Draw game over message if someone reached score limit
    if player_score >= score_limit or opponent_score >= score_limit:
        winner = "PLAYER" if player_score >= score_limit else "AI"
        winner_color = RED if winner == "PLAYER" else BLUE
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        win.blit(overlay, (0, 0))
        
        # Draw winner text
        winner_text = game_font.render(f"{winner} WINS!", True, winner_color)
        text_rect = winner_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        win.blit(winner_text, text_rect)
        
        # Draw restart instructions
        restart_text = small_font.render("Press SPACE to play again", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        win.blit(restart_text, restart_rect)

def reset_game():
    global player_score, opponent_score, game_active
    player_score = 0
    opponent_score = 0
    game_active = True
    ball_restart()

# Load sounds - Simplified approach without numpy dependency
try:
    paddle_sound = pygame.mixer.Sound('sounds/paddle_hit.wav')
    wall_sound = pygame.mixer.Sound('sounds/wall_hit.wav')
    score_sound = pygame.mixer.Sound('sounds/score.wav')
except (FileNotFoundError, NotImplementedError):
    # Create empty sound objects if files don't exist or sound is not available
    class DummySound:
        def play(self):
            pass
    
    paddle_sound = DummySound()
    wall_sound = DummySound()
    score_sound = DummySound()

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Change AI difficulty with number keys
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, 
                            pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                ai_difficulty = (event.key - pygame.K_0) / 10.0
            elif event.key == pygame.K_0:
                ai_difficulty = 1.0
            # Reset game when space is pressed and game is over
            elif event.key == pygame.K_SPACE and (player_score >= score_limit or opponent_score >= score_limit):
                reset_game()

    # Only handle input and AI if game is not over
    if player_score < score_limit and opponent_score < score_limit:
        handle_input()
        move_opponent_ai()  # Using AI instead of simple following
        update_game()
        update_particles()
    else:
        # Still update particles when game is over for visual effect
        update_particles()
    
    draw_game()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()