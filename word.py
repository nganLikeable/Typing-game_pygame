import pygame 
import random

class Word:
    def __init__ (self, word, WIDTH, HEIGHT):
        self.word = word
        self.untyped = word
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 50)
        self.CUSTARD = (243, 171, 46)
        self.GRAY = (165,165,165)
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
    
    def display_word(self, screen):
        typed_length = len(self.word) - len(self.untyped)
        typed_pt = self.word[:typed_length]
        
        # render each part in its according color 
        typed_sur = self.font.render(typed_pt, True, self.CUSTARD)
        untyped_sur = self.font.render(self.untyped, True,self.GRAY)
        
        # get the total width for the display, so that 2 elements align perfectly
        typed_width = typed_sur.get_width()
        untyped_width = untyped_sur.get_width()
        total_width = typed_width + untyped_width 
        
        # the x-coor to begin drawing full word
        x_start = (self.WIDTH - total_width)//2
        y = (self.HEIGHT - typed_sur.get_height())//2
        
        # blit both 
        screen.blit(typed_sur, (x_start, y))
        screen.blit(untyped_sur, (x_start + typed_width, y))
        
    
    # remove the typed letter
    def remove_typed(self):
        if self.untyped:
            self.untyped = self.untyped[1:]
    
    def is_empty(self):
        return len(self.untyped) == 0