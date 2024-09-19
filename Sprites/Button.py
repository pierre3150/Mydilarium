import pyxel

class Button():
    ''' affiche une texture à l'endroit souhaité'''
# constructeur
    def __init__(self, x, y, img, x_texture, y_texture, width, height, scale, reponse) -> None:
        self.x = x
        self.y = y
        self.img = img
        self.x_texture = x_texture
        self.y_texture = y_texture
        self.width = width
        self.height = height
        self.reponse = reponse
        self.text = ''
        self.scale = scale

    def setText(self, text):
        self.text = text
    
    def getText(self):
        return self.text
    
    def getReponse(self):
        return self.reponse

    def getPos(self):
        return self.x, self.y
        
    def update(self, keys):
        pass

    @property
    def draw(self):
        return self.x, self.y, self.img, self.x_texture, self.y_texture, self.width, self.height, self.scale
    

