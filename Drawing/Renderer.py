class Renderer:
    def __init__(self, screen):
        self.screen = screen

    def render(self, objects):
        for renderable in objects:
            renderable.prepare(self.screen)
            renderable.draw(self.screen)
