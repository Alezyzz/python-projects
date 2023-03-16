import pygame
import sys
pygame.init()


WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

font = pygame.font.Font(None, 36)

# Define menu items
menu_items = [
    {"text": "Play 2-Player Pong", "selected": False},
    {"text": "Instructions", "selected": False},
    {"text": "Quit", "selected": False}
]

# Define function for displaying the menu
def display_menu():
    # Clear the screen
    WIN.fill((0, 0, 0))

    # Display the menu items
    for i, item in enumerate(menu_items):
        text_color = (255, 255, 255)
        if item["selected"]:
            text_color = (255, 0, 0)
        text = font.render(item["text"], True, text_color)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + i*50))
        WIN.blit(text, text_rect)

    # Update the display
    pygame.display.update()

# Define function for handling menu selection
def handle_menu_selection():
    while True:
        # Wait for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    # Play Pong
                    return 1
                elif event.key == pygame.K_2:
                    # Show instructions
                    return 2
                elif event.key == pygame.K_3:
                    # Quit
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for i, item in enumerate(menu_items):
                    text = font.render(item["text"], True, (255, 255, 255))
                    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + i*50))
                    if text_rect.collidepoint(pos):
                        if i == 0:
                            # Play Pong
                            return 1
                        elif i == 1:
                            # Show instructions
                            return 2
                        elif i == 2:
                            # Quit
                            sys.exit()
                # If the mouse click is not on a menu item, do nothing
                pass

        # Check for mouse hover over menu items
        pos = pygame.mouse.get_pos()
        for i, item in enumerate(menu_items):
            text = font.render(item["text"], True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + i*50))
            if text_rect.collidepoint(pos):
                item["selected"] = True
            else:
                item["selected"] = False

        # Display the menu
        display_menu()

# Display the menu and wait for user selection
display_menu()
selection = handle_menu_selection()

# Handle the user's selection
if selection == 1:
# Play Pong
    # Frames Per Second in the game
    FPS = 60

    # Color RGB
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
    BALL_RADIUS = 7

    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    WINNING_SCORE = 10

    class Paddle:
        COLOR = WHITE

        # Speed of the paddles
        VEL = 4

        def __init__(self, x, y, width, height):
            self.x = self.original_x = x
            self.y = self.original_y = y
            self.width = width
            self.height = height

        def draw(self, win):
            pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

        def move(self, up = True):
            if up:
                self.y -= self.VEL
            else:
                self.y += self.VEL
        
        def reset(self):
            self.x = self.original_x
            self.y = self.original_y

    class Ball:
        MAX_VEL = 5
        COLOR = RED

        def __init__(self, x, y, radius):
            self.x = self.original_x = x
            self.y = self.original_y = y
            self.radius = radius
            self.x_vel = self.MAX_VEL
            self.y_vel = 0

        def draw(self, win):
            pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

        def move(self):
            self.x += self.x_vel
            self.y += self.y_vel

        def reset(self):
            self.x = self.original_x
            self.y = self.original_y
            self.y_vel = 0
            self.x_vel *= -1

    def draw(win, paddles, ball, left_score, right_score):
        # Filling the entire window with black color
        win.fill(BLACK)

        # Drawing the score table
        left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
        right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
        win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
        win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

        # Drawing the paddles in the window
        for paddle in paddles:
            paddle.draw(win)

        # Drawing a line in the middle
        for i in range(10, HEIGHT, HEIGHT//20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))
        
        # Drawing the ball
        ball.draw(win)
        pygame.display.update()

    def handle_collision(ball, left_paddle, right_paddle):
        if ball.y + ball.radius >= HEIGHT:
            ball.y_vel *= -1
        elif ball.y - ball.radius <= 0:
            ball.y_vel *= -1

        if ball.x_vel < 0:
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
                if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                    ball.x_vel *= -1

                    middle_y = left_paddle.y + left_paddle.height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel

        else:
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
                if ball.x + ball.radius >= right_paddle.x:
                    ball.x_vel *= -1

                    middle_y = right_paddle.y + right_paddle.height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel

    # Movement keys of the paddles
    def handle_paddle_movement(keys, left_paddle, right_paddle):
        # K_w and K_s is the W and S on the keyboard, and makes it so the paddles can't go out of the window
        if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
            left_paddle.move(up = True)
        if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
            left_paddle.move(up = False)

        # K_UP and K_DOWN is the up and down arrow on the keyboard
        if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
            right_paddle.move(up = True)
        if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
            right_paddle.move(up = False)

    def main():
        run = True
        clock = pygame.time.Clock()

        # Posistion of the paddles
        left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

        ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)

        left_score = 0
        right_score = 0


        while run:
            clock.tick(FPS)
            draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            handle_paddle_movement(keys, left_paddle, right_paddle)

            ball.move()
            handle_collision(ball, left_paddle, right_paddle)

            if ball.x < 0:
                right_score += 1
                ball.reset()
            elif ball.x > WIDTH:
                left_score += 1
                ball.reset()

            won = False
            if left_score >= WINNING_SCORE:
                ball.reset()
                left_paddle.reset()
                right_paddle.reset()
                win_text = "Left Player Won"
                won = True
            elif right_score >= WINNING_SCORE:
                ball.reset()
                left_paddle.reset()
                right_paddle.reset()
                win_text = "Right Player Won!"
                won = True
            
            if won:
                text = SCORE_FONT.render (win_text, 1, GREEN)
                WIN.blit(text, (WIDTH//2 - text.get_width() //2, HEIGHT//2 - text.get_height()//2))
                pygame.display.update()
                pygame.time.delay(5000)
                left_score = 0
                right_score = 0

elif selection == 2:
    # Show instructions
    # Add your code here
    pass
elif selection == 3:
    # Quit
    sys.exit()

if __name__ == '__main__':
    main()