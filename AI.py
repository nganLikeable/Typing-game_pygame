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
        self.duration = 10
        
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
        
            timer_rect = timer_surface.get_rect(bottomleft=(20, self.HEIGHT - 20))
            self.screen.blit(timer_surface, timer_rect)
        else:
            self.running = False
    
    def display_score(self):
        score_surface = self.font.render(f'Score: {self.score}', True, self.BACKGROUND_COLOR)
        score_rect = score_surface.get_rect(bottomleft=(self.WIDTH - 250, self.HEIGHT - 20))  
        self.screen.blit(score_surface, score_rect)
    
    def display_word(self, full_word, untyped_pt):
        typed_length = len(full_word) - len(untyped_pt)
        typed_pt = full_word[:typed_length]
        
        typed_sur = self.font.render(typed_pt, True, self.CUSTARD)
        untyped_sur = self.font.render(untyped_pt, True,((165, 165, 165)))
        
        typed_width = typed_sur.get_width()
        untyped_width = untyped_sur.get_width()
        total_width = typed_width + untyped_width 
        
        x_start = (self.WIDTH - total_width)//2
        y = (self.HEIGHT - typed_sur.get_height())//2
        
        self.screen.blit(typed_sur, (x_start, y))
        self.screen.blit(untyped_sur, (x_start + typed_width, y))
        
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
    
    def display_wpm (self):
        self.wpm = int(self.total_char/5)/(self.duration/60)
        
        wpm_sur = self.font.render(f'WPM: {self.wpm}', True, self.CUSTARD)
        sur_center = ((self.WIDTH - wpm_sur.get_width())//2,
                        (self.HEIGHT - wpm_sur.get_height())//2)
        self.screen.blit(wpm_sur, sur_center)
    
    def draw_button(self, text, x, y, width, height, color, hover_color):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(self.screen, hover_color, (x, y, width, height))
            if click[0] == 1:
                return True
        else:
            pygame.draw.rect(self.screen, color, (x, y, width, height))
        
        button_text = self.font.render(text, True, self.BACKGROUND_COLOR)
        button_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(button_text, button_rect)
        
        return False
    
    def game_over(self):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.display_wpm()
        game_over_surface = self.font.render('Game Over', True, self.CUSTARD)
        game_over_rect = game_over_surface.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 - 50))
        self.screen.blit(game_over_surface, game_over_rect)
        pygame.display.update()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            
            if self.draw_button('Restart', self.WIDTH//2 - 100, self.HEIGHT//2 + 50, 200, 50, self.CUSTARD, self.GRAY):
                self.reset_game()
                return
            
            pygame.display.update()
    
    def reset_game(self):
        self.score = 0
        self.wpm = 0
        self.total_char = 0
        self.start = pygame.time.get_ticks()
        self.running = True
        self.run()
    
    def run(self):
        lst = self.read_file("words.txt")
        word = self.get_word(lst)
        untyped_word = word

        while self.running:
            self.screen.fill(self.BACKGROUND_COLOR)
            self.draw_background()
            self.display_timer()
            self.display_score() 
            self.display_word(word, untyped_word)
            
            pygame.display.update()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                    
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_TAB:
                        word = self.get_word(lst)
                        untyped_word = word 
                        continue
                                           
                    if untyped_word and event.unicode == untyped_word[0]:
                        self.total_char += 1
                        untyped_word = self.remove_typed(untyped_word)
                        
                        if self.is_empty(untyped_word):
                            self.score += 1 
                            word = self.get_word(lst)
                            untyped_word = word
        
        self.game_over()

TypingGame().run()
