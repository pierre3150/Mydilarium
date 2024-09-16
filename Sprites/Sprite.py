import pyxel

class Sprite():
    ''' affiche une texture à l'endroit souhaité'''
# constructeur
    def __init__(self, x, y, img, x_texture, y_texture, width, height) -> None:
        self.x = x
        self.y = y
        self.img = img
        self.x_texture = x_texture
        self.y_texture = y_texture
        self.width = width
        self.height = height

    def animation(self, texture_1, texture_2):
        ''' switch d'une texture à l'autre toutes les quarts secondes'''
        if (self.x_texture, self.y_texture) == texture_1:
            if pyxel.frame_count %15 == 0:
                self.x_texture, self.y_texture = texture_2[0], texture_2[1]
        elif (self.x_texture, self.y_texture) == texture_2:
            if pyxel.frame_count %15 == 0:
                self.x_texture, self.y_texture = texture_1[0], texture_1[1]
        else:
            self.x_texture, self.y_texture = texture_1[0], texture_1[1] # on affiche la première texture qui fait débuter l'animation
        
    def update(self, keys):
        pass

    @property
    def draw(self):
        return self.x, self.y, self.img, self.x_texture, self.y_texture, self.width, self.height
    

