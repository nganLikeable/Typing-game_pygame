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
    
    def display_score(self):
        score_surface = self.font.render(f'Score: {self.score}', True, self.BACKGROUND_COLOR)
        score_rect = score_surface.get_rect(bottomleft=(self.WIDTH - 250, self.HEIGHT - 20))  
        self.screen.blit(score_surface, score_rect)
    
    # display entire word + typed word (blurry and plain colors)
    def display_word(self, full_word, untyped_pt):
        typed_length = len(full_word) - len(untyped_pt)
        typed_pt = full_word[:typed_length]
        
        # render each part in its according color 
        typed_sur = self.font.render(typed_pt, True, self.CUSTARD)
        untyped_sur = self.font.render(untyped_pt, True,((165, 165, 165)))
        
        # get the total width for the display, so that 2 elements align perfectly
        typed_width = typed_sur.get_width()
        untyped_width = untyped_sur.get_width()
        total_width = typed_width + untyped_width 
        
        # the x-coor to begin drawing full word
        x_start = (self.WIDTH - total_width)//2
        y = (self.HEIGHT - typed_sur.get_height())//2
        
        # blit both 
        self.screen.blit(typed_sur, (x_start, y))
        self.screen.blit(untyped_sur, (x_start + typed_width, y))
        
    
        
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
    
    
    def display_wpm (self):
        self.wpm = int(self.total_char/5)/(self.duration/60)
        
        wpm_sur = self.font.render(f'WPM: {self.wpm}', True, self.CUSTARD)
        sur_center = ((self.WIDTH - wpm_sur.get_width())//2,
                        (self.HEIGHT - wpm_sur.get_height())//2)
        self.screen.blit(wpm_sur, sur_center)
    
    # def game_over(self):
        
    
    
    def run(self):
        lst = self.read_file("words.txt")
        word = self.get_word(lst)
        untyped_word = word

        while self.running:
            # clear the screen after each display/loop
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
                    # if Tab is pressed => skip word
                    if event.key == pygame.K_TAB:
                        word = self.get_word(lst)
                        untyped_word = word 
                        continue
                                           
                    # if there's sth to type and the char is correct
                    if untyped_word and event.unicode == untyped_word[0]:
                        self.total_char += 1
                        untyped_word = self.remove_typed(untyped_word)
                        

                        if self.is_empty(untyped_word):
                            self.score += 1 
                            # reinitialize a new word 
                            word = self.get_word(lst)
                            untyped_word = word
                    

                    
                    
TypingGame().run()
