import pyxel
import webbrowser
import os
from Sprites.Player import Player
from Sprites.Map import Map
from Sprites.Image import Image
from Sprites.Jeton import Jeton
from Sprites.Text import Text

path = os.path.join("web", "index.html")

class App:
# constructeur
    def __init__(self):
        # initialisation des variables de base du jeu etc
        self.STATE = 'WAITING' # temporairement mis à PLAYING par défaut pour tests les fonctionnalités du jeu
        self.cold_key = 14 # couleur transparente
        self.SPRITES = [] # liste des éléments de notre jeu à afficher
        self.TSPRITES = [] # liste des éléments de notre jeu à afficher
        self.TEXT = [] # liste des textes de notre jeu à afficher
        self.MAP = Map(480, 192, 0, 0, 0, 40, 16)
        self.INTERFACE = False # si une interface est ouverte dans le jeu
        self.TIME = '8H - Debut de la journee '
        self.task = 0 # Tâche actuelle
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
# complète une tâche et passe à la suivante
    def CompleteTask(self, jeton):
        if not jeton.isComplete():
            jeton.Complete()
            self.task += 1

# Gestion global du jeu
    def update(self):
        '''update des éléments du jeu'''
        if self.isState('WAITING'):
        # texte indicatif 
            if len(self.getTsprites) == 0:
                x = Image(pyxel.width/8.5, pyxel.height/1.7, 0, 16, 16, 207, 16, 1)
                self.addTsprite(x)
        # détection de lancement de partie
            if pyxel.btn(pyxel.KEY_SPACE):
                self.removeTsprite(self.getTsprites[0])
                # on tp le joueur
                self.MAP.x, self.MAP.y= -470, 100
                self.setState('PLAYING') # on change l'état de la partie en PLAYING

        elif self.isState('PLAYING'):
        # on affiche des éléments de la partie quand elle débute
            if len(self.getSprites) == 0:
                player = Player(pyxel.width//2-4, pyxel.height//2-4, 0, 8, 0, 8, 8) # on crée un joueur
                self.addSprite(player)

        # déplacement 
            # UP
            target_jeton = self.canInteract(self.getSprites[0], self.getSprites[1:])
            if not self.INTERFACE:
                if pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_O):
                    self.UP(True)
                else:
                    self.UP(False)
                # DOWN
                if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_L):
                    self.DOWN(True)
                else:
                    self.DOWN(False)
                # LEFT
                if pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_K):
                    self.LEFT(True)
                else:
                    self.LEFT(False)
                # RIGHT
                if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_M):
                    self.RIGHT(True)
                else:
                    self.RIGHT(False)       
        
            # Détection interaction
                if target_jeton in self.getSprites: # si on est assez proche d'un jeton
                    if len(self.getText)==0:
                        self.addText(Text(pyxel.width//3, pyxel.height//2+20, "Press 'E' to interact", 7))

                    if pyxel.btnp(pyxel.KEY_E):
                    # gestion des MENUS jetons interactions
                        if target_jeton.getNb() == 0:
                            bulle = Image(pyxel.width//2,pyxel.height*5/6, 2, 32, 200, 32, 32, 10)
                            
                            # on ouvre une page web
                            url = "file://" + os.path.abspath(path)
                            webbrowser.open(url)
                            
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//15, pyxel.height//1.48, target_jeton.getText(), 7))

                            # on complète la tâche
                            self.CompleteTask(target_jeton)
                            self.TIME = '8h15 - Se rendre au MyDil'

                        elif target_jeton.getNb() == 1:
                            bulle = Image(pyxel.width//2,pyxel.height*5/6, 2, 32, 200, 32, 32, 10)
                            self.addTsprite(bulle)
                            # on complète la tâche
                            self.CompleteTask(target_jeton)
                            self.TIME = '8h30 - Cours de Réseau'

                        elif target_jeton.getNb() == 2:
                            bulle = Image(pyxel.width//2,pyxel.height*5/6, 2, 32, 200, 32, 32, 10)
                            self.addTsprite(bulle)
                            # on complète la tâche
                            self.CompleteTask(target_jeton)
                            self.TIME = '9h30 - Cours de Réseau'

                        elif target_jeton.getNb() == 3:
                            bulle = Image(pyxel.width//2,pyxel.height*5/6, 2, 32, 200, 32, 32, 10)
                            self.addTsprite(bulle)
                            # on complète la tâche
                            self.CompleteTask(target_jeton)
                            self.TIME = '10h15 - Pause fléchette'

                        elif target_jeton.getNb() == 4:
                            bulle = Image(pyxel.width//2,pyxel.height*5/6, 2, 32, 200, 32, 32, 10)
                            self.addTsprite(bulle)
                            # on complète la tâche
                            self.CompleteTask(target_jeton)
                            self.TIME = '10h30 - Cours Sécurité Web'
                        
                        elif target_jeton.getNb() == 5:
                            bulle = Image(pyxel.width//2,pyxel.height*5/6, 2, 32, 200, 32, 32, 10)
                            self.addTsprite(bulle)
                            # on complète la tâche
                            self.CompleteTask(target_jeton)
                            self.TIME = '11h30 - Cours Sécurité Web'
                        
                        elif target_jeton.getNb() == 6:
                            bulle = Image(pyxel.width//2,pyxel.height*5/6, 2, 32, 200, 32, 32, 10)
                            self.addTsprite(bulle)
                            # on complète la tâche
                            self.CompleteTask(target_jeton)
                            self.TIME = '12h30 - Pause Dejeuner'

                        elif target_jeton.getNb() == 7:
                            bulle = Image(pyxel.width//2,pyxel.height*5/6, 2, 32, 200, 32, 32, 10)
                            self.addTsprite(bulle)
                            # on complète la tâche
                            self.CompleteTask(target_jeton)
                            self.TIME = '13h30 - Cours Programmation'

                        elif target_jeton.getNb() == 8:
                            bulle = Image(pyxel.width//2,pyxel.height*5/6, 2, 32, 200, 32, 32, 10)
                            self.addTsprite(bulle)
                            # on complète la tâche
                            self.CompleteTask(target_jeton)
                            self.TIME = '14h30 - Cours Programmation'

                        elif target_jeton.getNb() == 9:
                            bulle = Image(pyxel.width//2,pyxel.height*5/6, 2, 32, 200, 32, 32, 10)
                            self.addTsprite(bulle)
                            # on complète la tâche
                            self.CompleteTask(target_jeton)
                            self.TIME = '15h15 - Pause dans le couloir'

                        elif target_jeton.getNb() == 10:
                            bulle = Image(pyxel.width//2,pyxel.height*5/6, 2, 32, 200, 32, 32, 10)
                            self.addTsprite(bulle)
                            # on complète la tâche
                            self.CompleteTask(target_jeton)
                            self.TIME = '15h30 - Cours Marketing/Communication'

                        elif target_jeton.getNb() == 11:
                            bulle = Image(pyxel.width//2,pyxel.height*5/6, 2, 32, 200, 32, 32, 10)
                            self.addTsprite(bulle)
                            # on complète la tâche
                            self.CompleteTask(target_jeton)
                            self.TIME = '16h30 - Cours Marketing/Communication'
                        
                        elif target_jeton.getNb() == 12:
                            bulle = Image(pyxel.width//2,pyxel.height*5/6, 2, 32, 200, 32, 32, 10)
                            self.addTsprite(bulle)
                            # on complète la tâche
                            self.CompleteTask(target_jeton)
                            self.TIME = '17h30 - Remise des Diplomes'
                        
                        elif target_jeton.getNb() == 13:
                            bulle = Image(pyxel.width//2,pyxel.height*5/6, 2, 32, 200, 32, 32, 10)
                            self.addTsprite(bulle)
                            # on complète la tâche
                            self.CompleteTask(target_jeton)
                            self.TIME = '18h - Sortir de l\'EPSI'
                        
                        elif target_jeton.getNb() == 14:
                            bulle = Image(pyxel.width//2,pyxel.height*5/6, 2, 32, 200, 32, 32, 10)
                            self.addTsprite(bulle)
                            # on complète la tâche
                            self.CompleteTask(target_jeton)

                        self.INTERFACE = True
                else:
                    for objtext in self.getText:
                        if objtext.getText() == "Press 'E' to interact": # on supprime le texte d'indication
                            self.removeText(objtext)
                        
            else:
                self.KEYS_PRESSED = {'UP':False, 'DOWN':False, 'LEFT':False, 'RIGHT':False}
                # on retire le texte d'indication
                # si on réappuye sur E on ferme le MENU
                if pyxel.btnp(pyxel.KEY_E):
                    for objtext in self.getText:
                        if objtext.getText() in target_jeton.getText():
                            self.removeText(objtext)# on supprime les textes et la bulle
                    self.removeTsprite(self.getTsprites[-1])
                    self.INTERFACE = False

        #gestion des jetons à afficher
            if self.task == 0 and len(self.getSprites) == 1:
                # on crée le premier jeton à l'entrée de l'EPSI
                jeton_entree = Jeton(0, pyxel.height//2, 0, 0, 40, 8, 8, 'text', 0)   
                self.addSprite(jeton_entree)    
            elif self.task == 1 and len(self.getSprites) == 2:
                jeton_mydil = Jeton(self.MAP.getPos()[0]-50, self.MAP.getPos()[1]+36, 0, 0, 40, 8, 8, 'text', 1)   
                self.addSprite(jeton_mydil) 
            elif self.task == 2 and len(self.getSprites) == 3:
                jeton_reseau_cours = Jeton(self.MAP.getPos()[0]-288, self.MAP.getPos()[1]-112, 0, 0, 40, 8, 8, 'text', 2)   
                self.addSprite(jeton_reseau_cours) 
            elif self.task == 3 and len(self.getSprites) == 4:
                jeton_reseau_epreuve = Jeton(self.MAP.getPos()[0]-420, self.MAP.getPos()[1], 0, 0, 40, 8, 8, 'text', 3)   
                self.addSprite(jeton_reseau_epreuve) 
            elif self.task == 4 and len(self.getSprites) == 5:
                jeton_pause = Jeton(self.MAP.getPos()[0]*2-157, self.MAP.getPos()[1]*2-34, 0, 0, 40, 8, 8, 'text', 4)   
                self.addSprite(jeton_pause)
            elif self.task == 5 and len(self.getSprites) == 6:
                jeton_web_cours = Jeton(self.MAP.getPos()[0]+400, self.MAP.getPos()[1]-160, 0, 0, 40, 8, 8, 'text', 5)   
                self.addSprite(jeton_web_cours)
            elif self.task == 6 and len(self.getSprites) == 7:
                jeton_web_epreuve = Jeton(self.MAP.getPos()[0]+428, self.MAP.getPos()[1]-30, 0, 0, 40, 8, 8, 'text', 6)   
                self.addSprite(jeton_web_epreuve)
            elif self.task == 7 and len(self.getSprites) == 8:
                jeton_midi = Jeton(self.MAP.getPos()[0]+332, self.MAP.getPos()[1]*2+50, 0, 0, 40, 8, 8, 'text', 7)   
                self.addSprite(jeton_midi)
            elif self.task == 8 and len(self.getSprites) == 9:
                jeton_dev_cours = Jeton(self.MAP.getPos()[0]-150, self.MAP.getPos()[1]//10+100, 0, 0, 40, 8, 8, 'text', 8)   
                self.addSprite(jeton_dev_cours)
            elif self.task == 9 and len(self.getSprites) == 10:
                jeton_dev_epreuve = Jeton(self.MAP.getPos()[0], self.MAP.getPos()[1]//10+172, 0, 0, 40, 8, 8, 'text', 9)   
                self.addSprite(jeton_dev_epreuve)
            elif self.task == 10 and len(self.getSprites) == 11:
                jeton_pause_aprem = Jeton(self.MAP.getPos()[0], self.MAP.getPos()[1]-36, 0, 0, 40, 8, 8, 'text', 10)   
                self.addSprite(jeton_pause_aprem)
            elif self.task == 11 and len(self.getSprites) == 12:
                jeton_marketing_cours = Jeton(self.MAP.getPos()[0]//2-50, self.MAP.getPos()[1]//3-30, 0, 0, 40, 8, 8, 'text', 11)   
                self.addSprite(jeton_marketing_cours)
            elif self.task == 12 and len(self.getSprites) == 13:
                jeton_marketing_epreuve = Jeton(self.MAP.getPos()[0]*2-50, self.MAP.getPos()[1]//3+10, 0, 0, 40, 8, 8, 'text', 12)   
                self.addSprite(jeton_marketing_epreuve)
            elif self.task == 13 and len(self.getSprites) == 14:
                jeton_remise_diplome = Jeton(self.MAP.getPos()[0]-360, self.MAP.getPos()[1]+200, 0, 0, 40, 8, 8, 'text', 13)   
                self.addSprite(jeton_remise_diplome)
            elif self.task == 14 and len(self.getSprites) == 15:
                jeton_creation_boite = Jeton(self.MAP.getPos()[0]*2+70, self.MAP.getPos()[1]+28, 0, 0, 40, 8, 8, 'text', 14)   
                self.addSprite(jeton_creation_boite)

        # on update les sprites & les textes
            for s in self.getSprites:
                s.update(self.KEYS_PRESSED)
            for t in self.getText:
                t.update(self.KEYS_PRESSED)

        # on update la map
            self.MAP.update(self.KEYS_PRESSED)

        elif self.isState('FINISH'):
            pass

    def draw(self):
        pyxel.cls(0) # background noir
        ''' on affiche la map'''
        m = self.MAP
        pyxel.bltm(m.draw[0], m.draw[1], m.draw[2], m.draw[3], m.draw[4], m.draw[5]*8, m.draw[6]*8, self.cold_key, 0, 4)
        
        '''on parcours les sprites et les textes et on les affiche'''
        for s in self.getSprites:
            pyxel.blt(s.draw[0], s.draw[1], s.draw[2], s.draw[3], s.draw[4], s.draw[5], s.draw[6], self.cold_key, 0, 4)
        for ts in self.getTsprites:
            pyxel.blt(ts.draw[0], ts.draw[1], ts.draw[2], ts.draw[3], ts.draw[4], ts.draw[5], ts.draw[6], self.cold_key, 0, ts.draw[7])
        for t in self.getText:
            pyxel.text(t.draw[0], t.draw[1], t.draw[2], t.draw[3])
        # on affiche l'horloge
        if self.isState('PLAYING'):
            pyxel.text(pyxel.width*1/3,3, self.TIME, 7)

App()