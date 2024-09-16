import pyxel

class App:
    def __init__(self):
        pyxel.init(64, 64)
        pyxel.run(self.update, self.draw)

    def update(self):
        # update des éléments du jeu
        pass 
    
    def draw(self):
        # afficher les éléments du jeu
        pyxel.cls(0)
        pyxel.rect(self.x, 0, 8, 8, 9) 

App()