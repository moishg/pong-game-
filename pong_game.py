import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors - Dark background with bright contrast colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)

# Themes
THEMES = {
    "dark": {
        "background": BLACK,
        "foreground": WHITE,
        "accent": CYAN,
    },
    "light": {
        "background": WHITE,
        "foreground": BLACK,
        # Use black accent on a light background for maximum contrast
        "accent": BLACK,
    },
}

# Paddle settings
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7

# Ball settings
BALL_SIZE = 15
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Score to win
WINNING_SCORE = 7


class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 0

    def move(self):
        self.rect.y += self.speed
        # Keep paddle on screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self, screen, color=WHITE):
        pygame.draw.rect(screen, color, self.rect)


class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, 
                                HEIGHT // 2 - BALL_SIZE // 2, 
                                BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X * random.choice([-1, 1])
        self.speed_y = BALL_SPEED_Y * random.choice([-1, 1])

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = BALL_SPEED_X * random.choice([-1, 1])
        self.speed_y = BALL_SPEED_Y * random.choice([-1, 1])

    def draw(self, screen, color=CYAN):
        pygame.draw.ellipse(screen, color, self.rect)


class PongGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.theme = "dark"
        pygame.display.set_caption(self._window_caption())
        self.clock = pygame.time.Clock()
        
        # Create paddles
        self.player_paddle = Paddle(30, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.computer_paddle = Paddle(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        
        # Create ball
        self.ball = Ball()
        
        # Scores
        self.player_score = 0
        self.computer_score = 0
        
        # Font
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        
        # Game state
        self.game_over = False
        self.winner = None

    def _window_caption(self):
        return f"Pong Game ({self.theme.capitalize()} Mode)"

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        pygame.display.set_caption(self._window_caption())

    def _colors(self):
        return THEMES[self.theme]

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player_paddle.speed = -PADDLE_SPEED
        elif keys[pygame.K_DOWN]:
            self.player_paddle.speed = PADDLE_SPEED
        else:
            self.player_paddle.speed = 0

    def update_computer_ai(self):
        # Simple AI: follow the ball
        if self.computer_paddle.rect.centery < self.ball.rect.centery:
            self.computer_paddle.speed = PADDLE_SPEED - 1  # Slightly slower than player
        elif self.computer_paddle.rect.centery > self.ball.rect.centery:
            self.computer_paddle.speed = -(PADDLE_SPEED - 1)
        else:
            self.computer_paddle.speed = 0

    def check_collisions(self):
        # Ball collision with paddles
        if self.ball.rect.colliderect(self.player_paddle.rect):
            self.ball.speed_x = abs(self.ball.speed_x)  # Ensure ball goes right
            # Add some variation based on where ball hits paddle
            hit_pos = (self.ball.rect.centery - self.player_paddle.rect.centery) / PADDLE_HEIGHT
            self.ball.speed_y += hit_pos * 2
        
        if self.ball.rect.colliderect(self.computer_paddle.rect):
            self.ball.speed_x = -abs(self.ball.speed_x)  # Ensure ball goes left
            # Add some variation based on where ball hits paddle
            hit_pos = (self.ball.rect.centery - self.computer_paddle.rect.centery) / PADDLE_HEIGHT
            self.ball.speed_y += hit_pos * 2

    def check_scoring(self):
        # Check if ball went off screen
        if self.ball.rect.left <= 0:
            self.computer_score += 1
            self.ball.reset()
            self.check_game_over()
        elif self.ball.rect.right >= WIDTH:
            self.player_score += 1
            self.ball.reset()
            self.check_game_over()

    def check_game_over(self):
        if self.player_score >= WINNING_SCORE:
            self.game_over = True
            self.winner = "Player"
        elif self.computer_score >= WINNING_SCORE:
            self.game_over = True
            self.winner = "Computer"

    def draw(self):
        colors = self._colors()

        # Draw background
        self.screen.fill(colors["background"])
        
        # Draw center line
        for i in range(0, HEIGHT, 40):
            pygame.draw.rect(self.screen, colors["foreground"], (WIDTH // 2 - 2, i, 4, 20))
        
        # Draw paddles and ball
        self.player_paddle.draw(self.screen, colors["foreground"])
        self.computer_paddle.draw(self.screen, colors["foreground"])
        # In light mode, cyan has low contrast on white; use the foreground color instead.
        ball_color = colors["accent"] if self.theme == "dark" else colors["foreground"]
        self.ball.draw(self.screen, ball_color)
        
        # Draw scores
        player_text = self.font.render(str(self.player_score), True, colors["foreground"])
        computer_text = self.font.render(str(self.computer_score), True, colors["foreground"])
        self.screen.blit(player_text, (WIDTH // 4, 30))
        self.screen.blit(computer_text, (3 * WIDTH // 4 - computer_text.get_width(), 30))
        
        # Draw game over screen
        if self.game_over:
            game_over_text = self.font.render(f"{self.winner} Wins!", True, colors["accent"])
            restart_text = self.small_font.render("Press R to Restart or Q to Quit", True, colors["foreground"])
            self.screen.blit(game_over_text, 
                           (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            self.screen.blit(restart_text, 
                           (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
        
        pygame.display.flip()

    def reset_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.game_over = False
        self.winner = None
        self.ball.reset()
        self.player_paddle.rect.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.computer_paddle.rect.y = HEIGHT // 2 - PADDLE_HEIGHT // 2

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.toggle_theme()
                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.reset_game()
                        elif event.key == pygame.K_q:
                            running = False

            if not self.game_over:
                self.handle_input()
                self.update_computer_ai()
                
                # Move everything
                self.player_paddle.move()
                self.computer_paddle.move()
                self.ball.move()
                
                # Check collisions and scoring
                self.check_collisions()
                self.check_scoring()
            
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = PongGame()
    game.run()
