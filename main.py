import pygame
import random 
import math 
from pygame import mixer
from sys import exit 

from button import Button 
from cat_sprite import CatSprite
from word import Word 

cat_images = ['cat_img\cat1.png',
              'cat_img\cat2.png', 
              'cat_img\cat3.png',
              'cat_img\cat4.jpg',
              'cat_img\cat5.jpg']


def read_file(filename):
    with open (filename) as f:
        wordList = [word.strip() for word in f]
    return wordList

# return a random word from the wordlist
def get_word(lst):
    return lst[random.randint(0, len(lst) - 1)]

wordList = read_file('words.txt')

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
        pygame.display.set_caption("Menu")
        self.icon = pygame.image.load('cat.jpg')
        pygame.display.set_icon(self.icon)
        
        # play bg music
        mixer.init()
        mixer.music.load('meow.mp3')
        mixer.music.play(-1) # to loop music infinitely
        
        # typing sound
        self.button_sound = pygame.mixer.Sound("press_button.mp3")
        
        # buttons
        self.start_button = Button('start_button.png', 400, 300, 0.5)
        self.exit_button = Button('exit_button.png', 400, 400, 0.5)
        
        self.scroll = 0
        self.cat_bg = pygame.image.load('cat_img\\cats.png').convert_alpha()
        self.cat_bg_width = self.cat_bg.get_width()
        self.cat_bg_rect = self.cat_bg.get_rect()
    
    # cre: https://github.com/russs123/pygame_tutorials/blob/main/Infinite_Background/scroll_tut.py 
    def draw_cat(self):
        # calculate the number of images to fill in the screen
        tiles = math.ceil(self.WIDTH / self.cat_bg_width) + 1

        for i in range(tiles):
            self.screen.blit(self.cat_bg, (i*self.cat_bg_width + self.scroll, self.HEIGHT - self.cat_bg.get_height()))
        
        self.scroll -= 1

        # reset
        if abs(self.scroll) > self.cat_bg_width:
            self.scroll = 0
        
                        
    def draw_background(self):
        pygame.draw.rect(self.screen, self.CUSTARD, (0, self.HEIGHT - 100, self.WIDTH, 100), 0) # (x, y, width, height) 
    
    def draw_text(self, text, font_name, size, pos: tuple, color, align = 'center', is_bold= False):
        text_font = pygame.font.SysFont(font_name, size, bold = is_bold)
        text_sur = text_font.render(text, True, color) 
        rect = text_sur.get_rect()
        
        if align == 'center':
            rect.center = pos 
        elif align == 'topleft':
            rect.topleft = pos 
        elif align == 'bottomleft':
            rect.bottomleft = pos 
        
        self.screen.blit(text_sur, rect)
    
        
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
    
    def display_wpm (self):
        self.wpm = int(self.total_char/5)/(self.duration/60)
        wpm_sur = self.font.render(f'WPM: {self.wpm}', True, self.CUSTARD)
        sur_center = ((self.WIDTH - wpm_sur.get_width())//2,
                        (self.HEIGHT - wpm_sur.get_height())//2)
        self.screen.blit(wpm_sur, sur_center)
    
    def display_menu(self):
        self.draw_text('PawPrints', "Courier New",  50, (400, 100), self.CUSTARD, "center", True)
        self.start_button.draw(self.screen)
        self.exit_button.draw(self.screen)
        pygame.display.set_caption('Menu')
    
    def play(self):
        # reset game state
        self.running = True
        self.start = pygame.time.get_ticks()
        self.score = 0
        self.total_char = 0
        
        word = Word(get_word(wordList), self.WIDTH, self.HEIGHT)

        while self.running:
            # clear the screen after each display/loop
            self.screen.fill(self.BACKGROUND_COLOR)
            self.draw_background()
            self.display_timer()
            self.display_score() 
            
            word.display_word(self.screen)
            pygame.display.update()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                    
                if event.type == pygame.KEYDOWN: 
                    # if Tab is pressed => skip word
                    if event.key == pygame.K_TAB:
                        word = Word(get_word(wordList), self.WIDTH, self.HEIGHT)
                        continue
                                           
                    # if there's sth to type and the char is correct
                    if word.untyped and event.unicode == word.untyped[0]:
                        self.total_char += 1
                        word.remove_typed()
                        

                        if word.is_empty():
                            self.score += 1 
                            # reinitialize a new word 
                            word = Word(get_word(wordList), self.WIDTH, self.HEIGHT)
        self.screen.fill(self.BACKGROUND_COLOR)
        self.display_wpm()
        pygame.display.update()
        pygame.time.delay(3000)
        
        
    def run(self):
        while self.running:
            self.screen.fill(self.BACKGROUND_COLOR)
            self.draw_cat()
            self.display_menu()
            pygame.display.update()
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                
            
            if self.start_button.is_pressed():
                self.button_sound.play()
                self.play()
            elif self.exit_button.is_pressed():
                
                exit()
                
if __name__ == '__main__':
    TypingGame().run()