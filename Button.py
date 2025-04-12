import pygame
from sys import exit
import random 

pygame.init()
pygame.font.init()

# Screen size
HEIGHT = 400
WIDTH = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Screen caption + icon
pygame.display.set_caption("Typing")
icon = pygame.image.load('cartoon.jpg')
pygame.display.set_icon(icon)

# Font
font = pygame.font.SysFont("Comic Sans MS", 50)

# Colors
YELLOW = (243, 171, 46)
GRAY = (100, 100, 100)
BACKGROUND_COLOR = (32, 32, 32)

# Clock & timer
clock = pygame.time.Clock()
countdown_time = 60  # seconds
start_ticks = pygame.time.get_ticks()


def draw_background():
    pygame.draw.rect(screen, YELLOW, (0, HEIGHT - 100, WIDTH, 100))


def draw_countdown():
    seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = countdown_time - seconds_passed

    if time_left > 0:
        mins_left, seconds_left = divmod(time_left, 60)
        countdown_surface = font.render(f'{mins_left:02d}:{seconds_left:02d}', True, YELLOW)
    else:
        countdown_surface = font.render("Boom!", True, YELLOW)

    screen.blit(countdown_surface, (20, 20))
    return time_left > 0


def get_word(filename):
    with open(filename) as f:
        word_list = [word.strip() for word in f]
    return random.choice(word_list)


def run():
    word = get_word("words.txt")
    current_input = ""

    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_background()
        game_running = draw_countdown()

        if not game_running:
            pygame.display.update()
            continue

        # Draw the original word in gray
        full_word_surface = font.render(word, True, GRAY)
        screen.blit(full_word_surface, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

        # Draw the typed part in yellow
        typed_surface = font.render(current_input, True, YELLOW)
        screen.blit(typed_surface, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    current_input = current_input[:-1]
                else:
                    # get keyboard input
                    char = event.unicode
                    
                    # Only accept if the next char matches
                    if len(current_input) < len(word) and char == word[len(current_input)]:
                        current_input += char

                    if current_input == word:
                        word = get_word("words.txt")
                        current_input = ""

        clock.tick(60)


run()
