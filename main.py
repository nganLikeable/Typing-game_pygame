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
        
        self.clock = pygame.time.Clock()
    
    def draw_background(self):
        pygame.draw.rect(self.screen, self.CUSTARD, (0, self.HEIGHT - 100, self.WIDTH, 100), 0) # (x, y, width, height)
    
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
    
    def read_file(self, filename):
        with open (filename) as f:
            wordList = [word.strip() for word in f]
        return wordList

    # return a random word from the wordlist
    def get_word(self, lst):
        return lst[random.randint(0, len(lst) - 1)]
    
    # remove the typed letter
    def remove_typed(self, word):
        return word[1:]
    
    def is_empty(self, word):
        return len(word) == 0
    
    def display_word(self, word):
        word_surface = self.font.render(f"{word}", True, self.CUSTARD)
        self.screen.blit(word_surface, (self.WIDTH//2, self.HEIGHT//2))
    
    def run(self):
        while self.running:
            # clear the screen after each display/loop
            self.screen.fill(self.BACKGROUND_COLOR)
            self.draw_background()
            self.display_timer()
            self.display_score()

            pygame.display.update()
            
            lst = self.read_file("words.txt")
            word = self.get_word(lst)
            self.display_word(word)
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                
                # get keyboard input letter
                if event.type == pygame.KEYDOWN:
                    char = event.unicode

                    
                    
TypingGame().run()
