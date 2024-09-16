import pyxel
from Sprites.Player import Player
from Sprites.Sprite import Sprite
from Sprites.Text import Text

class App:
# constructeur
    def __init__(self):
        # initialisation des variables de base du jeu etc
        self.STATE = 'WAITING' # temporairement mis à PLAYING par défaut pour tests les fonctionnalités du jeu
        self.cold_key = 14 # couleur transparente
        self.SPRITES = [] # liste des éléments de notre jeu à afficher
        self.TEXT = [] # liste des textes de notre jeu à afficher
        self.KEYS_PRESSED = {'UP':False, 'DOWN':False, 'LEFT':False, 'RIGHT':False}
        pyxel.init(64, 64) # dimension de la fenêtre
        pyxel.load('res.pyxres') # importation du fichier des textures
        pyxel.run(self.update, self.draw) # execution du jeu

# gestion des états de la partie
    def isState(self, state):
        '''test si la valeur de STATE est égale à celle entrée en argument'''
        return self.STATE == state
    
    def setState(self, state):
        '''change la valeur de state'''
        self.STATE = state

# Gestion des Sprites
    def addSprite(self, sprite):
        ''' ajouter un nouveau sprite à la liste des éléments à aficher '''
        self.SPRITES.append(sprite)

    def removeSprite(self, sprite):
        '''supprimer un sprite pour ne plus l'afficher'''
        self.SPRITES.remove(sprite)
    @property
    def getSprites(self):
        ''' retourne la liste de tous les sprites à afficher'''
        return self.SPRITES
    
# Gestion des Textes    
    def addText(self, text):
        ''' ajouter un nouveau texte à la liste des textes à aficher '''
        self.TEXT.append(text)

    def removeText(self, text):
        '''supprimer un texte pour ne plus l'afficher'''
        self.TEXT.remove(text)
    @property
    def getText(self):
        ''' retourne la liste de tous les textes à afficher'''
        return self.TEXT
    
# Gestion des déplacements
    def UP(self, bool):
        self.KEYS_PRESSED['UP'] = bool
    
    def DOWN(self, bool):
        self.KEYS_PRESSED['DOWN'] = bool

    def LEFT(self, bool):
        self.KEYS_PRESSED['LEFT'] = bool
    
    def RIGHT(self, bool):
        self.KEYS_PRESSED['RIGHT'] = bool

# Gestion global du jeu
    def update(self):
        '''update des éléments du jeu'''
        if self.isState('WAITING'):
            # création logo EPSI & texte indicatif 
            text = Text(pyxel.width//9, pyxel.height*2/3, "Space to Play", 7)
            self.addText(text)

        elif self.isState('PLAYING'):
        # on affiche des éléments de la partie quand elle débute
            if len(self.getSprites) == 0:
                player = Player(pyxel.width//2-4, pyxel.height//2-4, 0, 8, 0, 8, 8) # on crée un joueur
                self.addSprite(player)
        # déplacement 
            # UP
            if pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_UP):
                self.UP(True)
            else:
                self.UP(False)
            # DOWN
            if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
                self.DOWN(True)
            else:
                self.DOWN(False)
            # LEFT
            if pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_LEFT):
                self.LEFT(True)
            else:
                self.LEFT(False)
            # RIGHT
            if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
                self.RIGHT(True)
            else:
                self.RIGHT(False)
        # on update les sprites & les textes
            for s in self.getSprites:
                s.update(self.KEYS_PRESSED)
            for t in self.getText:
                t.update(self.KEYS_PRESSED)

        elif self.isState('FINISH'):
            pass

    def draw(self):
        pyxel.cls(14) # background noir
        '''on parcours les sprites et les textes et on les affiche'''
        for s in self.getSprites:
            pyxel.blt(s.draw[0], s.draw[1], s.draw[2], s.draw[3], s.draw[4], s.draw[5], s.draw[6], self.cold_key)
        for t in self.getText:
            pyxel.text(t.draw[0], t.draw[1], t.draw[2], t.draw[3])

App()