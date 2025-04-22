import pygame
import random 
import math 
from pygame import mixer
from sys import exit 

from button import Button 
from word import Word 

def read_file(filename):
    with open (filename) as f:
        wordList = [word.strip() for word in f]
    return wordList

# return a random word from the wordlist
def get_word(lst):
    return lst[random.randint(0, len(lst) - 1)]

wordList = read_file('asset/words.txt')

class TypingGame:
    def __init__ (self):
        self.HEIGHT = 600
        self.WIDTH = 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.running = True 
        self.score = 0
        self.wpm = 0
        self.total_char = 0
        self.word = Word(get_word(wordList), self.WIDTH, self.HEIGHT)
        
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
        self.icon = pygame.image.load('asset/cat.jpg')
        pygame.display.set_icon(self.icon)
        
        # play bg music
        mixer.init()
        mixer.music.load('asset/meow.mp3')
        mixer.music.set_volume(0.1)
        mixer.music.play(-1) # to loop music infinitely
        
        # typing sound
        self.button_sound = pygame.mixer.Sound("asset/press_button.mp3")
        self.key_sound = pygame.mixer.Sound("asset/key_typed.mp3")
        self.key_sound.set_volume(0.1)
        # buttons
        self.start_button = Button('asset/start_button.png', 400, 300, 0.5)
        self.exit_button = Button('asset/exit_button.png', 400, 400, 0.5)
        self.restart_button = Button('asset/restart_button.png', 400, 300, 0.15)
        
        # scrolling cat bg
        self.scroll = 0
        self.cat_bg = pygame.image.load('asset/cats.png').convert_alpha()
        self.cat_bg_width = self.cat_bg.get_width()
        self.cat_bg_rect = self.cat_bg.get_rect()
    
    # cre: https://github.com/russs123/pygame_tutorials/blob/main/Infinite_Background/scroll_tut.py 
    def draw_cat(self):
        # calculate the number of images to fill in the screen
        tiles = math.ceil(self.WIDTH / self.cat_bg_width) + 1 # 1 as buffer

        for i in range(tiles):
            self.screen.blit(self.cat_bg, (i*self.cat_bg_width + self.scroll, self.HEIGHT - self.cat_bg.get_height()))
        
        # scroll bg to the left
        self.scroll -= 1

        # reset
        if abs(self.scroll) > self.cat_bg_width: #img off screen
            self.scroll = 0
        
                        
    def draw_background(self):
        pygame.draw.rect(self.screen, self.CUSTARD, (0, self.HEIGHT - 100, self.WIDTH, 100), 0) # (x, y, width, height) 
        self.display_score()
        self.display_timer()
    
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
            return False
        
        else:
            return True # time's up
    
    def display_score(self):
        score_surface = self.font.render(f'Score: {self.score}', True, self.BACKGROUND_COLOR)
        score_rect = score_surface.get_rect(bottomleft=(self.WIDTH - 250, self.HEIGHT - 20))  
        self.screen.blit(score_surface, score_rect)
    
    def calculate_wpm (self):
        self.wpm = int(self.total_char/5)/(self.duration/60)
    
    def display_menu(self):
        self.draw_text('PawPrints', "Comic Sans",  80, (400, 100), self.CUSTARD, "center", True)
        self.start_button.draw(self.screen)
        self.exit_button.draw(self.screen)
        pygame.display.set_caption('Menu')
    
    def restart(self):
        self.running = True
        self.start = pygame.time.get_ticks()
        self.score = 0
        self.total_char = 0
        self.word = Word(get_word(wordList), self.WIDTH, self.HEIGHT)

    def run(self):
        state = 'menu'

        while True:
            self.screen.fill(self.BACKGROUND_COLOR)
            self.clock.tick(60) # limit the speed and frames
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            
            if state == 'menu':
                self.draw_cat()
                self.display_menu()
                self.start_button.draw(self.screen)
                self.exit_button.draw(self.screen)
                pygame.display.set_caption('Menu')
                pygame.display.update()
            
                if self.start_button.is_pressed():
                    self.button_sound.play()
                    state = 'play'
                    self.restart()
                elif self.exit_button.is_pressed():
                    exit()
            
            elif state == 'play':
                self.screen.fill(self.BACKGROUND_COLOR)
                pygame.display.set_caption("Play")
                self.draw_background() # yellow rect, score and timer
                time_up = self.display_timer()
                self.word.display_word(self.screen)
                pygame.display.update()
                
                for event in events:
                    if event.type == pygame.KEYDOWN: 
                        self.key_sound.play()
                        # if Tab is pressed => skip word
                        if event.key == pygame.K_TAB:
                            self.word = Word(get_word(wordList), self.WIDTH, self.HEIGHT)
                            continue                
                        # if there's sth to type and the char is correct
                        if self.word.untyped and event.unicode == self.word.untyped[0]:
                            self.total_char += 1
                            self.word.remove_typed()

                            if self.word.is_empty():
                                self.score += 1 
                                # reinitialize a new word 
                                self.word = Word(get_word(wordList), self.WIDTH, self.HEIGHT)
                        
                if time_up:
                    state = 'game_over'
                    
            elif state == 'game_over':
                self.screen.fill(self.BACKGROUND_COLOR)
                self.scroll -= 1
                self.draw_cat()
                self.calculate_wpm()
                self.draw_text(f'WPM: {self.wpm}', "Courier New", 50, (400,100), self.CUSTARD, 'center', True )
                self.draw_text(f'Score: {self.score}', 'Courier New', 50, (400, 150), self.CUSTARD, 'center', True)
                
                self.restart_button.draw(self.screen)
                self.exit_button.draw(self.screen)
                pygame.display.set_caption('Game Over')
                pygame.display.update()
                
                if self.restart_button.is_pressed():
                    self.restart()
                    self.button_sound.play()
                    state = 'play'        

                elif self.exit_button.is_pressed():
                    exit()
                
if __name__ == '__main__':
    TypingGame().run()
