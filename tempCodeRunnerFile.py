    def run(self):
        lst = self.read_file("words.txt")
        word = self.get_word(lst)
        
        while self.running:
            self.screen.fill(self.BACKGROUND_COLOR)
            self.draw_background()
            self.display_timer()
            self.display_score()

            self.display_word(word)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.KEYDOWN:
                    # Only continue if there’s something to type
                    if word and event.unicode == word[0]:
                        word = self.remove_typed(word)

                        if self.is_empty(word):
                            self.score += 1
                            word = self.get_word(lst)
