import pyxel
from Sprites.Player import Player
from Sprites.Map import Map
from Sprites.BLT import BLT
from Sprites.Text import Text

class App:
# constructeur
    def __init__(self):
        # initialisation des variables de base du jeu etc
        self.STATE = 'WAITING' # temporairement mis à PLAYING par défaut pour tests les fonctionnalités du jeu
        self.cold_key = 14 # couleur transparente
        self.SPRITES = [] # liste des éléments de notre jeu à afficher
        self.TSPRITES = [] # liste des éléments de notre jeu à afficher
        self.TEXT = [] # liste des textes de notre jeu à afficher
        self.MAP = [Map(480, 192, 0, 0, 0, 40, 16)]
        self.KEYS_PRESSED = {'UP':False, 'DOWN':False, 'LEFT':False, 'RIGHT':False}
        pyxel.init(256, 256) # dimension de la fenêtre
        pyxel.load('res.pyxres') # importation du fichier des textures
        pyxel.run(self.update, self.draw) # execution du jeu

# gestion des états de la partie
    def isState(self, state):
        '''test si la valeur de STATE est égale à celle entrée en argument'''
        return self.STATE == state
    
    def setState(self, state):
        '''change la valeur de state'''
        self.STATE = state

# Gestion des Textes Sprites
    def addTsprite(self, tsprite):
        ''' ajouter un nouveau texte sprite à la liste des éléments à aficher '''
        self.TSPRITES.append(tsprite)

    def removeTsprite(self, tsprite):
        '''supprimer un texte sprite pour ne plus l'afficher'''
        self.TSPRITES.remove(tsprite)
    @property
    def getTsprites(self):
        ''' retourne la liste de tous les texte sprites à afficher'''
        return self.TSPRITES

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

# gestion interaction
    def canInteract(self, posPlayer, posJetons:list):
        ''' détecte si le joueur est assez proche d'un jeton interaction '''
        jeton = False
        for pos in posJetons:
            player_x, player_y = posPlayer.getPos()[0], posPlayer.getPos()[1]
            jeton_x, jeton_y = pos.getPos()[0], pos.getPos()[1]
            if jeton_x-35 <= player_x+4 <= jeton_x+35 and jeton_y-35 <= player_y+4 <= jeton_y +35: 
                jeton = pos
        return jeton
    
#visualisation de la position du personnage        
    def Position(self, posPlayer):
        ''' détecte si le joueur est assez proche d'un jeton interaction '''
        player_x, player_y = posPlayer.getPos()[0], posPlayer.getPos()[1]
        return player_x, player_y

# Gestion global du jeu
    def update(self):
        '''update des éléments du jeu'''
        if self.isState('WAITING'):
        # texte indicatif 
            if len(self.getTsprites) == 0:
                x = BLT(pyxel.width/8.5, pyxel.height/1.7, 0, 16, 16, 207, 16)
                self.addTsprite(x)
        # détection de lancement de partie
            if pyxel.btn(pyxel.KEY_SPACE):
                self.removeTsprite(self.getTsprites[0])
                # on tp le joueur
                for m in self.MAP:
                    m.x = -470
                    m.y = 100
                self.setState('PLAYING') # on change l'état de la partie en PLAYING

        elif self.isState('PLAYING'):
        # on affiche des éléments de la partie quand elle débute
            if len(self.getSprites) == 0:
                player = Player(pyxel.width//2-4, pyxel.height//2-4, 0, 8, 0, 8, 8) # on crée un joueur
                self.addSprite(player)
                jeton_entree = BLT(0, pyxel.height//2, 0, 0, 40, 8, 8) # on crée des jetons interactions
                jeton_mydil = BLT(-518, pyxel.height//2+8, 0, 0, 40, 8, 8)
                self.addSprite(jeton_entree)
                self.addSprite(jeton_mydil)
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
        #Systéme d'horloge 
            if len(self.getText) == 0:
                text = Text(pyxel.width//1-47,3, "Heure:8-10h", 7)
                self.addText(text)       
        

        
        # Détection interaction
            target_jeton = self.canInteract(self.getSprites[0], self.getSprites[1:])
            if target_jeton in self.getSprites: # si on est assez proche d'un jeton
                if len(self.getText)==1:
                    self.addText(Text(pyxel.width//3, pyxel.height//2+20, "Press 'E' to interact", 7))
                    if pyxel.btn(pyxel.KEY_E):
                        joueur_x, joueur_y = self.Position(self.getSprites[0]) # on vient chercher la position du joueur
                        if joueur_x and joueur_y == 124: # on compare la aposition du joueur pour savoir quelle intéraction faire
                            if len(self.getTsprites) == 0:
                                x = BLT(pyxel.width/8.5, pyxel.height/1.7, 0, 16, 16, 207, 16)
                                self.addTsprite(x)
            else:
                if len(self.getText)>1:
                    self.removeText(self.getText[-1]) # supprime le dernier text

        # on update les sprites & les textes
            for s in self.getSprites:
                s.update(self.KEYS_PRESSED)
            for t in self.getText:
                t.update(self.KEYS_PRESSED)

        # on update la map
            for m in self.MAP:
                m.update(self.KEYS_PRESSED)

        elif self.isState('FINISH'):
            pass

    def draw(self):
        pyxel.cls(0) # background noir
        ''' on affiche la map'''
        for m in self.MAP:
            pyxel.bltm(m.draw[0], m.draw[1], m.draw[2], m.draw[3], m.draw[4], m.draw[5]*8, m.draw[6]*8, self.cold_key, 0, 4)
        
        '''on parcours les sprites et les textes et on les affiche'''
        for s in self.getSprites:
            pyxel.blt(s.draw[0], s.draw[1], s.draw[2], s.draw[3], s.draw[4], s.draw[5], s.draw[6], self.cold_key, 0, 4)
        for ts in self.getTsprites:
            pyxel.blt(ts.draw[0], ts.draw[1], ts.draw[2], ts.draw[3], ts.draw[4], ts.draw[5], ts.draw[6], self.cold_key, 0, 1)
        for t in self.getText:
            pyxel.text(t.draw[0], t.draw[1], t.draw[2], t.draw[3])











    #Horloge interne 

    
App()