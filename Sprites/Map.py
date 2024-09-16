import pyxel

class Map():
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
        self.speed_scrolling = 1
        
    def update(self, keys):
        # on fait défiler la map quand le joueur avance
        if keys['UP']:
            self.y += self.speed_scrolling
        elif keys['DOWN']:
            self.y -= self.speed_scrolling
        elif keys['LEFT']:
            self.x += self.speed_scrolling  
        elif keys['RIGHT']:
            self.x -= self.speed_scrolling 

    @property
    def draw(self):
        return self.x, self.y, self.img, self.x_texture, self.y_texture, self.width, self.height
    

