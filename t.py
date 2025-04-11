import pygame
from sys import exit
import random 


pygame.init()
pygame.font.init()

# Screen size
HEIGHT = 800
WIDTH = 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # tuple

# Screen caption + icon
pygame.display.set_caption("Typing")
icon = pygame.image.load('cartoon.jpg')
pygame.display.set_icon(icon)

# font
font = pygame.font.SysFont("Somic Sans MS", 50)


# Clock object
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()

def draw_background():
    pygame.draw.rect(screen, (243, 171, 46), (0, HEIGHT - 100, WIDTH, 100), 0 ) #(x, y, width, height)

def draw_countdown(countdown_time):
    seconds_passed = (pygame.time.get_ticks() - start_ticks)//1000 # in milliseconds
    time_left = countdown_time - seconds_passed

        # display on screen
    if time_left > 0:
        mins_left, seconds_left = divmod(time_left, 60)
        countdown_surface = font.render(f'{mins_left:02d}:{seconds_left:02d}', True, (243, 171, 46))  # returns the quotient and remainder
    else:
        countdown_surface = font.render(f"Boom!", True, (243, 171, 46))
        
    screen.blit(countdown_surface , (20,20))



def get_word(filename):
    # read words from text file
    with open(filename) as f:
        word_list = [word.rstrip('\n') for word in f]
        f.close()
    list_length = len(word_list)
    
    # to get the index 
    i = random.randint(0, list_length - 1)
    return word_list[i]

# display the rest to be typed
def remove_head(word):
    return word[1:]

def is_empty(word):
    return not word


def run():
    while True:
        screen.fill((32,32,32))
        countdown_time = 60

        draw_background()
        draw_countdown(countdown_time)
        word = get_word("words.txt")
        display_word = font.render(word, True, (243, 171, 46))
        screen.blit(display_word, (WIDTH/2, HEIGHT/2))

        pygame.display.update()  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            if event.type == pygame.KEYDOWN:
                if chr(event.key) == word[0]:
                    word = remove_head(word)
                    if is_empty(word):
                        word = get_word("words.txt")


run()