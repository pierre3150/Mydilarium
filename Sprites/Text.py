

class Text():
    '''affiche du text à l'endroit souhaité'''
# constructeur
    def __init__(self, x, y, text, color) -> None:
        self.x, self.y = x, y
        self.text = text
        self.color = color

    def getText(self):
        return self.text

    def update(self, keys):
        pass

    @property
    def draw(self):
        return self.x, self.y, self.text, self.color