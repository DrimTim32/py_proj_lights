from Drawing.Maps import Map


class Game:
    def __init__(self, screen):
        self.map = Map()
        self.screen = screen
        self.dupa = 'dupa'

    def update(self):
        self.map.prepare(self.screen)
        self.map.draw(self.screen)
