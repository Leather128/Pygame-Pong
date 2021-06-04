import pygame, os, random

# My modules #
import colors, fonts, paths

from ball import PongBall
from paddle import Paddle
from difinfo import DifficultyInfo as difficulties

# The main function where everything runs #
def main():
    def resetArena(pointReset):
        ball.position.x = screen_Width / 2 - ball.size
        ball.position.y = screen_Height / 2
        ball.velocity.x = ball_speed
        ball.velocity.y = random.randint(-1, 1)

        paddle_left.position.y = screen_Height / 2 - paddle_size_y / 2
        paddle_right.position.y = screen_Height / 2 - paddle_size_y / 2

        if pointReset:
            points[0] = 0
            points[1] = 0

    def hitPaddle():
        ball.velocity.x = ball.velocity.x - (ball.velocity.x * 2)
        ball.velocity.y = random.randint(-1 - selected_difficulty, 1 + selected_difficulty) + ball.velocity.y - (ball.velocity.y * 2)
        pygame.mixer.Sound.play(ball_hit)

    # Starting pygame #
    pygame.init()

    # Window Settings #
    screen_Width, screen_Height, max_FrameRate = 640, 480, 30
    game_Title, bg_Color, icon = "Pong!", colors.BLACK, "pong_icon"

    # Setting up the screen #
    screen = pygame.display.set_mode((screen_Width, screen_Height))
    pygame.display.set_caption(game_Title)
    screen.fill(bg_Color)
    pygame.display.set_icon(pygame.image.load(paths.findPath(["images"], icon, "png")))

    # Main Variables #
    clock = pygame.time.Clock()
    points = [0, 0]
    ball_speed = 5

    ball = PongBall((320, 240), 20, colors.WHITE)

    paddle_speed = 10
    ai_speed = 9

    paddle_size_x = 20
    paddle_size_y = 100

    paddle_right = Paddle((screen_Width - paddle_size_x, screen_Height / 2 - paddle_size_y / 2), (paddle_size_x, paddle_size_y), colors.WHITE)
    paddle_left = Paddle((0, screen_Height / 2 - paddle_size_y / 2), (paddle_size_x, paddle_size_y), colors.WHITE)

    selected_difficulty = 1
    difficulty_string = "Fair"
    selection_screen = True

    # Fonts #
    pixel = pygame.font.Font(paths.findPath(["fonts"], fonts.pixel_font, "ttf"), 32)

    # Sounds #
    ball_hit = pygame.mixer.Sound(paths.findPath(["sounds"], "ball-hit", "wav"))
    score = pygame.mixer.Sound(paths.findPath(["sounds"], "score", "wav"))
    select = pygame.mixer.Sound(paths.findPath(["sounds"], "menu-select", "wav"))

    # Window Loop #
    running = True

    pygame.key.set_repeat(100)

    while running:
        # Caps the framerate #
        clock.tick(max_FrameRate)

        # Delta time for making things consistent #
        dt = clock.get_time()
        
        # Refreshes the screen with the background color #
        screen.fill(bg_Color)

        # Event handling #
        for event in pygame.event.get():
            # If you hold a key #
            if event.type == pygame.KEYDOWN:
                if not selection_screen:
                    # Paddle Movement #
                    if event.key == pygame.K_w:
                        paddle_right.position.y -= (paddle_speed / 10) * dt

                        if paddle_right.position.y < 0:
                            paddle_right.position.y = 0

                    if event.key == pygame.K_s:
                        paddle_right.position.y += (paddle_speed / 10) * dt

                        if paddle_right.position.y > screen_Height - paddle_right.size.y:
                            paddle_right.position.y = screen_Height - paddle_right.size.y

            if event.type == pygame.KEYUP:
                if selection_screen:
                    if event.key == pygame.K_RETURN:
                        resetArena(True)
                        selection_screen = False
                        pygame.mixer.Sound.play(select)

                    if event.key == pygame.K_UP:
                        selected_difficulty -= 1
                        pygame.mixer.Sound.play(select)

                    if event.key == pygame.K_DOWN:
                        selected_difficulty += 1
                        pygame.mixer.Sound.play(select)

                    if event.key == pygame.K_ESCAPE:
                        running = False
                else:
                    if event.key == pygame.K_ESCAPE:
                        resetArena(True)
                        selection_screen = True
                        pygame.mixer.Sound.play(select)

            # If you quit the program with the window's x button #
            if event.type == pygame.QUIT:
                # Stop running this loop #
                running = False

        # Draw UI before everything else so nothing goes behind it #

        # Difficulty Select #
        if selection_screen:
            if selected_difficulty < 0:
                selected_difficulty = len(difficulties) - 1
            elif selected_difficulty > len(difficulties) - 1:
                selected_difficulty = 0

            for x in range(0, len(difficulties)):
                string_val = difficulties[x][0]

                if x == selected_difficulty:
                    string_val = ">" + string_val + "<"

                    paddle_speed = difficulties[x][2][0]
                    ai_speed = difficulties[x][2][1]
                    difficulty_string = difficulties[x][0]

                text = pixel.render(string_val, True,  difficulties[x][1], bg_Color)
                text_rect = text.get_rect()
                text_rect.center = (630 // 2, (400 + (x * 100)) // 2)
                screen.blit(text, text_rect)

            splash = pixel.render("-- Difficulty Select --", True, colors.WHITE, bg_Color)
            splash_rect = splash.get_rect()
            splash_rect.center = (630 // 2, 200 // 2)
            screen.blit(splash, splash_rect)

            version_num = pixel.render("v0.0.1", True, colors.GREY, bg_Color)
            version_num_rect = version_num.get_rect()
            version_num_rect.center = (0, 0)
            version_num_rect.x = 0
            version_num_rect.y = screen_Height - version_num_rect.height
            screen.blit(version_num, version_num_rect)

        # Score Text #
        if not selection_screen:
            score_text = pixel.render(str(points[0]) + " - " + str(points[1]), True, colors.WHITE, bg_Color)
            score_text_rect = score_text.get_rect()
            score_text_rect.center = (630 // 2, 50 // 2)
            screen.blit(score_text, score_text_rect)

            selected = pixel.render("Difficulty: " + difficulty_string, True, colors.GREY, bg_Color)
            selected_rect = selected.get_rect()

            selected_rect.center = (0, 0)
            selected_rect.x = 0
            selected_rect.y = screen_Height - selected_rect.height

            screen.blit(selected, selected_rect)

        # Drawing Paddles To The Screen #
        if not selection_screen:
            pygame.draw.rect(screen, paddle_right.color, pygame.Rect(paddle_right.position.x, paddle_right.position.y, paddle_right.size.x, paddle_right.size.y))
            pygame.draw.rect(screen, paddle_left.color, pygame.Rect(paddle_left.position.x, paddle_left.position.y, paddle_left.size.x, paddle_left.size.y))

        # Draws the ball to the screen #
        if not selection_screen:
            pygame.draw.circle(screen, ball.color, ball.position, ball.size)

        # Adds the velocity of the ball to the ball's movement #
        if not selection_screen:
            ball.position.x += (ball.velocity.x / 10) * dt
            ball.position.y += (ball.velocity.y / 10) * dt

        # Ball Collision #
        # We use a rectangular hit box for simplicity #

        if not selection_screen:
            if paddle_right.is_touching(ball):
                hitPaddle()
            elif paddle_left.is_touching(ball):
                hitPaddle()

        # Ball Outside Checks #

        # Checks if the ball is out of bounds on the right side #
        if ball.position.x >= screen_Width + ball.size:
            points[0] += 1
            resetArena(False)
            pygame.mixer.Sound.play(score)
        # Checks if the ball is out of bounds on the right side #
        elif ball.position.x <= 0 - ball.size:
            points[1] += 1
            resetArena(False)
            pygame.mixer.Sound.play(score)

        # Ball Screen Check #
        if not selection_screen:
            if ball.position.y < 0 + ball.size:
                ball.position.y = 0 + ball.size
                ball.velocity.y = random.randint(-5, 5)

                if not ball.velocity.y <= 0:
                    pygame.mixer.Sound.play(ball_hit)
            elif ball.position.y > screen_Height - ball.size:
                ball.position.y = screen_Height - ball.size
                ball.velocity.y = random.randint(-5, 5)

                if not ball.velocity.y <= 0:
                    pygame.mixer.Sound.play(ball_hit)

        # Move Left Paddle #
        if not selection_screen:
            if ball.position.y > paddle_left.position.y:
                paddle_left.position.y += (ai_speed / 10) * dt

            if ball.position.y < paddle_left.position.y:
                paddle_left.position.y -= (ai_speed / 10) * dt

        # Left Paddle Screen Check #
        if paddle_left.position.y < 0:
            paddle_left.position.y = 0
        elif paddle_left.position.y > screen_Height - paddle_left.size.y:
            paddle_left.position.y = screen_Height - paddle_left.size.y
        
        # Updates the display #
        pygame.display.update()
    
    pygame.quit()

main()