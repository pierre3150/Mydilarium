import pyxel

class Jeton():
    ''' affiche une texture à l'endroit souhaité'''
# constructeur
    def __init__(self, x, y, img, x_texture, y_texture, width, height, scale, text, index) -> None:
        self.x = x
        self.y = y
        self.img = img
        self.x_texture = x_texture
        self.y_texture = y_texture
        self.width = width
        self.height = height
        self.speed_scrolling = 3
        self.text = text
        self.index = index
        self.scale = scale

    def getText(self):
        return self.text
    
    def getNb(self):
        return self.index
    
    def getPos(self):
        return self.x, self.y
    
    def Complete(self): # change le design du jeton en vert
        if self.y_texture == 40:
            self.x_texture, self.y_texture = self.x_texture+8, 40
        if self.y_texture == 48:
            if self.x_texture < 8:
                self.x_texture, self.y_texture = self.x_texture+8, 48

    def isComplete(self):
        return self.x_texture == 8 and self.y_texture == 40 or self.x_texture == 8 and self.y_texture == 48
    
    def update(self, keys):
        if keys['UP'] and pyxel.pget(pyxel.width//2, pyxel.height//2-14)!=0:
            self.y += self.speed_scrolling
        elif keys['DOWN'] and pyxel.pget(pyxel.width//2, pyxel.height//2+10)!=0:
            self.y -= self.speed_scrolling
        elif keys['LEFT'] and pyxel.pget(pyxel.width//2-10, pyxel.height//2)!=0:
            self.x += self.speed_scrolling  
        elif keys['RIGHT'] and pyxel.pget(pyxel.width//2+14, pyxel.height//2)!=0:
            self.x -= self.speed_scrolling 

    @property
    def draw(self):
        return self.x, self.y, self.img, self.x_texture, self.y_texture, self.width, self.height, self.scale
    

