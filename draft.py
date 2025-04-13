# display the entire word - in blurry mode
def display_word(self, word):
    word_sur = self.font.render(f"{word}", True, (165, 165, 165 ))
    sur_center = ((self.WIDTH - word_sur.get_width())/2, 
                                    (self.HEIGHT - word_sur.get_height())/2)
    self.screen.blit(word_sur, sur_center)
    
# display the rest to be typed 
def display_cur_word(self, cur_word):
    cur_sur = self.font.render(f"{cur_word}", True, self.CUSTARD)
    sur_center = ((self.WIDTH - cur_sur.get_width())/2, 
                                    (self.HEIGHT - cur_sur.get_height())/2)
    self.screen.blit(cur_sur, sur_center)
