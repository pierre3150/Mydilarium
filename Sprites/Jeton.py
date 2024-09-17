import pyxel

class Jeton():
    ''' affiche une texture à l'endroit souhaité'''
# constructeur
    def __init__(self, x, y, img, x_texture, y_texture, width, height, element) -> None:
        self.x = x
        self.y = y
        self.img = img
        self.x_texture = x_texture
        self.y_texture = y_texture
        self.width = width
        self.height = height
        self.speed_scrolling = 3
        self.element = element

    def getElement(self):
        return self.element
    
    def getPos(self):
        return self.x, self.y
    
    def Complete(self): # change le design du jeton en vert
        self.x_texture, self.y_texture = 8, 40
    
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
        return self.x, self.y, self.img, self.x_texture, self.y_texture, self.width, self.height
    

