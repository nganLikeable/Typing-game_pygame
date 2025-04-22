import pygame 

class Button: 
    def __init__(self, image, x, y, scale = 1.0):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(center = (x, y))
        
        # change size of image button
        img_width = self.image.get_width()
        img_height = self.image.get_height()
        new_width = int(img_width * scale)
        new_height = int(img_height *scale)
        self.image = pygame.transform.smoothscale(self.image, (new_width, new_height))
        self.rect = self.image.get_rect(center=(x,y))
        self.pressed = False 
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def is_pressed(self):
        # coordinate of mouse 
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0] # boolean val, checks if the left mouse is being held down: 0: left, 1: mid, 2: right
        
        # checks if the mouse is hovering the button 
        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed and not self.pressed: # if the left mouse but is pressed now and not pressed before => prevent multiple frames
                self.pressed = True 
                return True 
        
        # if the mouse cursor is released
        if not mouse_pressed:
            self.pressed = False 
        return False
