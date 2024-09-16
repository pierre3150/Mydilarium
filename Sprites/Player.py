import pyxel

class Player():

    def __init__(self, x, y, img, x_texture, y_texture, width, height):
        # caratéristiques du Player
        self.x = x
        self.y = y
        self.x_texture = x_texture
        self.y_texture = y_texture
        self.width = width
        self.height = height
        self.img = img

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
        # met à jour les textures du personnage en fonction de la touche pressée
        if keys['UP']:
            self.animation((0,16),(8,16))
        elif keys['DOWN']:
            self.animation((8,24),(8,32))
        elif keys['LEFT']:
            self.animation((0,24),(0,32))      
        elif keys['RIGHT']:
            self.animation((0,8),(0,0))
        else:
            self.x_texture, self.y_texture = 8, 8

    @property
    def draw(self):
        return self.x, self.y, self.img, self.x_texture, self.y_texture, self.width, self.height