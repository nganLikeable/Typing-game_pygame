import pygame
from sys import exit 
import random 

class TypingGame:
    def __init__ (self):
        self.HEIGHT = 600
        self.WIDTH = 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.running = True 
        self.score = 0
        self.wpm = 0
        self.total_char = 0
        
        pygame.font.init()
        self.font = pygame.font.SysFont("Comic Sans MS", 50)

        self.clock = pygame.time.Clock()
        self.start = pygame.time.get_ticks()
        self.duration = 60
        
        # colors
        self.BACKGROUND_COLOR = (32,32,32)
        self.CUSTARD = (243, 171, 46)
        self.GRAY = (100, 100, 100)

        pygame.init()
        
        pygame.display.set_caption("CatType")
        self.icon = pygame.image.load('cat.jpg')
        pygame.display.set_icon(self.icon)

    def draw_background(self):
        pygame.draw.rect(self.screen, self.CUSTARD, (0, self.HEIGHT - 100, self.WIDTH, 100), 0)

    def display_timer(self):
        seconds_passed = (pygame.time.get_ticks() - self.start) // 1000
        time_left = self.duration - seconds_passed
        
        if time_left > 0:
            mins_left, secs_left = divmod(time_left, 60)
            timer_surface = self.font.render(f'{mins_left:02d}:{secs_left:02d}', True, self.BACKGROUND_COLOR)
        else:
            timer_surface = self.font.render("Kaboom", True, self.CUSTARD)
        
        timer_rect = timer_surface.get_rect(bottomleft=(20, self.HEIGHT - 20))
        self.screen.blit(timer_surface, timer_rect)

    def display_score(self):
        score_surface = self.font.render(f'Score: {self.score}', True, self.BACKGROUND_COLOR)
        score_rect = score_surface.get_rect(bottomleft=(self.WIDTH - 250, self.HEIGHT - 20))  
        self.screen.blit(score_surface, score_rect)

    def display_split_word(self, full_word, cur_word):
        typed_length = len(full_word) - len(cur_word)
        typed_part = full_word[:typed_length]
        untyped_part = cur_word

        typed_surface = self.font.render(typed_part, True, (50, 205, 50))  # Lime green
        untyped_surface = self.font.render(untyped_part, True, self.CUSTARD)

        total_width = typed_surface.get_width() + untyped_surface.get_width()
        x_start = (self.WIDTH - total_width) // 2
        y = (self.HEIGHT - typed_surface.get_height()) // 2

        self.screen.blit(typed_surface, (x_start, y))
        self.screen.blit(untyped_surface, (x_start + typed_surface.get_width(), y))

    def read_file(self, filename):
        with open (filename) as f:
            wordList = [word.strip() for word in f]
        return wordList

    def get_word(self, lst):
        return lst[random.randint(0, len(lst) - 1)]

    def remove_typed(self, word):
        return word[1:]

    def is_empty(self, word):
        return len(word) == 0

    def calculate_wpm (self):
        return int(self.total_char / 5) / (self.duration / 60)

    def display_wpm (self):
        wpm_sur = self.font.render(f'WPM: {self.calculate_wpm()}', True, self.CUSTARD)
        sur_center = ((self.WIDTH - wpm_sur.get_width()) // 2,
                      (self.HEIGHT - wpm_sur.get_height()) // 2)
        self.screen.blit(wpm_sur, sur_center)

    def run(self):
        lst = self.read_file("words.txt")
        word = self.get_word(lst)
        cur_word = word

        while self.running:
            self.screen.fill(self.BACKGROUND_COLOR)
            self.draw_background()
            self.display_timer()
            self.display_score()
            self.display_split_word(word, cur_word)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.KEYDOWN:
                    if cur_word and event.unicode == cur_word[0]:
                        self.total_char += 1
                        cur_word = self.remove_typed(cur_word)

                        if self.is_empty(cur_word):
                            self.score += 1 
                            word = self.get_word(lst)
                            cur_word = word


TypingGame().run()
