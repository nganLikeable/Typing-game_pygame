import pygame
import random

class CatSprite(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, image_lst):
        super().__init__()
        self.org_image = pygame.image.load(random.choice(image_lst)).convert_alpha() # create a pixel perfect pygame
        self.image = pygame.transform.scale(self.org_image, (100,100))
        self.rect = self.image.get_rect()
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # pick random starting points from the left
        self.rect.x = random.randint(-800, 0)
        self.rect.y = random.randint(screen_height - 200, screen_height - 120)
        self.speed = random.uniform(0.3, 0.7) # pick a random float number 
        
    def update(self):
        self.rect.x += self.speed 
        if self.rect.left > self.screen_width:
            self.rect.x -= self.rect.width 
            self.rect.y = random.randint(self.screen_height - 200, self.screen_height - 120, )
            self.speed = random.uniform(0.3, 0.7)
        
