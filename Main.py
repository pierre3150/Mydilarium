import pyxel
import webbrowser
import os
from Sprites.Player import Player
from Sprites.Map import Map
from Sprites.Image import Image
from Sprites.Jeton import Jeton
from Sprites.Button import Button
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
        self.MAP = Map(480, 192, 0, 0, 0, 40, 16)
        self.INTERFACE = False # si une interface est ouverte dans le jeu
        self.TIME = '8H - Debut de la journee '
        self.task = 0 # Tâche actuelle
        self.deleteJeton = [] #
        self.INVENTORY = [] # liste pour stocker les objets du MyDil récupérés
        self.Buttons = []
        self.caseCoche = []
        self.nbObjet = 0 # compteur d'objet trouvés
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

# Gestion des Button
    def addButton(self, button):
        ''' ajouter un nouveau sprite à la liste des buttons à aficher '''
        self.Buttons.append(button)

    def removeButton(self, button):
        '''supprimer un button pour ne plus l'afficher'''
        self.Buttons.remove(button)
    @property
    def getButton(self):
        ''' retourne la liste de tous les buttons à afficher'''
        return self.Buttons
    
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
    def CompleteTask(self, jeton, deleteAfterOpen):
        if not jeton.isComplete():
            jeton.Complete()
            self.task += 1
        if deleteAfterOpen:
            self.deleteJeton.append(jeton)

# Gestion global du jeu
    def update(self):
        '''update des éléments du jeu'''
        if self.isState('WAITING'):
        # texte indicatif space to interact 
            if len(self.getTsprites) == 0:
                pyxel.playm(0, 1, True)# on lance la musique
                x = Image(pyxel.width/8.5, pyxel.height/1.7, 0, 16, 16, 207, 16, 1)
                self.addTsprite(x)
                # texte menu informations
                text = Text(pyxel.width // 2 - 40, pyxel.height // 2 + 60, "Menu d'information(i)", 5)
                self.addText(text)
        #Screen information
            if pyxel.btnp(pyxel.KEY_I): 
                if self.INTERFACE==True:
                    self.TEXT.clear()
                    self.removeTsprite(self.getTsprites[-1])
                    # texte menu informations
                    text = Text(pyxel.width // 2 - 40, pyxel.height // 2 + 60, "Menu d'information(i)", 5)
                    self.addText(text)
                    self.INTERFACE=False
                else:
                    menu = Image(95,110,0,0,168,64,64,3)
                    self.addTsprite(menu)
                    self.removeText(self.getText[-1]) # on supprime le texte du menu d'informations
                    self.addText(Text(pyxel.width//3 - 42, pyxel.height//2+30, "Bienvenue sur notre jeu de Workshop de\n\nseconde annee d\'etude, ce jeu a etait\n\n\ncreer par le groupe compose de Alix\n\n Paul et Pierre SN2 etudiant\n\n a l\'EPSI d\'Arras. ", 0))
                    self.INTERFACE = True

        # détection de lancement de partie
            if pyxel.btn(pyxel.KEY_SPACE)and self.INTERFACE==False:
                self.removeTsprite(self.getTsprites[0])
                # on tp le joueur
                self.MAP.x, self.MAP.y= -470, 100
                self.TEXT.clear()
                self.setState('PLAYING') # on change l'état de la partie en PLAYING



        elif self.isState('PLAYING'):
        # on affiche des éléments de la partie quand elle débute
            if len(self.getSprites) == 0:
                # on crée un joueur
                player = Player(pyxel.width//2-4, pyxel.height//2-4, 0, 8, 0, 8, 8, 4) 
                self.addSprite(player)
                
                # crée les objets manquant du MyDil
                objet1 = Jeton(self.MAP.getPos()[0]*2+36, self.MAP.getPos()[1]+34, 0, 0, 48, 8, 8, 2,'     Casque virtuel !\n\n\nRapporte le vite au MyDil', 15)
                objet2 = Jeton(self.MAP.getPos()[0]//2-40, self.MAP.getPos()[1]*3+28, 0, 0, 48, 8, 8, 2,"    Carte Raspberry !\n\n\nRapporte le vite au MyDil", 16)
                objet3 = Jeton(self.MAP.getPos()[0]//2+24, self.MAP.getPos()[1]//3-90, 0, 0, 48, 8, 8, 2,"         Robot !\n\n\nRapporte le vite au MyDil", 17)
                objet4 = Jeton(self.MAP.getPos()[0]//8+22, self.MAP.getPos()[1]+210, 0, 0, 48, 8, 8, 2,"        Manette !\n\n\nRapporte le vite au MyDil", 18)
                objet5 = Jeton(self.MAP.getPos()[0]-388, self.MAP.getPos()[1]+228, 0, 0, 48, 8, 8, 2,"      Imprimante 3D !\n\n\nRapporte le vite au MyDil", 19)
                self.addSprite(objet1)
                self.addSprite(objet2)
                self.addSprite(objet3)
                self.addSprite(objet4)
                self.addSprite(objet5)

        # déplacement 
            # UP
            target_jeton = self.canInteract(self.getSprites[0], self.getSprites[1:]) # jeton le plus proche
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
                        self.addText(Text(pyxel.width//3.5, pyxel.height//2+20, "Appuyez sur 'E' pour interagir", 7))

                    if pyxel.btnp(pyxel.KEY_E):
                    # gestion des MENUS jetons interactions
                        if target_jeton.getNb() == 0:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))

                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)

                        elif target_jeton.getNb() == 1:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)

                        elif target_jeton.getNb() == 2:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))            
                            self.CompleteTask(target_jeton, False)

                        elif target_jeton.getNb() == 3:
                            # epreuve réseau
                            pyxel.mouse(True) # on active la souris
                            bg = Image(pyxel.width//2-63, 60, 2, 0, 0, 127, 143, 1.5)
                            self.addTsprite(bg)
                            # on ajoute les boutons
                            self.addButton(Button(pyxel.width//2+65, 52, 2, 104, 16, 16, 16, 1.5, '3')) 
                            self.addButton(Button(pyxel.width//2+65, 100, 2, 104, 16, 16, 16, 1.5, '2'))
                            self.addButton(Button(pyxel.width//2+65, 148, 2, 104, 16, 16, 16, 1.5, '1'))
                            self.addButton(Button(pyxel.width//2+65, 196, 2, 104, 16, 16, 16, 1.5, '4'))

                            self.addText(Text(pyxel.width//3.5, 58, 'installer Linux', 0))
                            self.addText(Text(pyxel.width//3.7, 106, 'Connecter un Serveur', 0))
                            self.addText(Text(pyxel.width//3.7, 154, 'Retablir le Reseau', 0))
                            self.addText(Text(pyxel.width//3.7, 202, 'configurer Apache2', 0))

                            self.CompleteTask(target_jeton, True)

                        elif target_jeton.getNb() == 4:
                            bulle = Image(pyxel.width//2-8,pyxel.height*4/5, 2, 32, 200, 32, 32, 8)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//7, pyxel.height//1.47, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, False)
                        
                        elif target_jeton.getNb() == 5:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, False)
                        
                        elif target_jeton.getNb() == 6:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            
                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)

                        elif target_jeton.getNb() == 7:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, False)

                        elif target_jeton.getNb() == 8:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            
                            # on complète la tâche
                            self.CompleteTask(target_jeton, False)

                        elif target_jeton.getNb() == 9:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                        
                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)

                        elif target_jeton.getNb() == 10:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)

                        elif target_jeton.getNb() == 11:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            
                            # on complète la tâche
                            self.CompleteTask(target_jeton, False)
                        
                        elif target_jeton.getNb() == 12:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                    
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)
                        
                        elif target_jeton.getNb() == 13:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)
                        
                        elif target_jeton.getNb() == 14:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)

                        elif target_jeton.getNb() == 20:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            if self.nbObjet >=4:
                                self.addText(Text(pyxel.width//8, pyxel.height//1.47, 'Bravo tu as trouve et ramene tous\nles objets du MyDil ! \n\nMerci pour ton aide :)', 7))
                            else:
                                self.addText(Text(pyxel.width//8, pyxel.height//1.47, 'Merci beaucoup !\n\nIl reste ' + str(5-(self.nbObjet+1)) + ' objets a trouver, je\n compte sur toi !', 7))
                            # on vide l'inventaire
                            self.INVENTORY.clear()
                            self.nbObjet += 1
                            # on complète la tâche
                            target_jeton.Complete()
                            self.deleteJeton.append(target_jeton)
                            
                        elif target_jeton.getNb() == 21:
                            map = Image(pyxel.width//2-20 ,pyxel.height//3, 0, 16, 32, 40, 24, 6)
                            self.addTsprite(map)
                            self.addText(Text(pyxel.width//6, pyxel.height//6+4, 'Reseau', 0))
                            self.addText(Text(pyxel.width//2-10, pyxel.height//6+4, 'Marketing', 0))
                            self.addText(Text(pyxel.width*4/5-5, pyxel.height//6+4, 'Web', 0))
                            self.addText(Text(pyxel.width//6-6, pyxel.height//2+1, 'Conference', 0))
                            self.addText(Text(pyxel.width//2-20, pyxel.height//2+9, 'Developpement', 0))
                            self.addText(Text(pyxel.width*4/5-8, pyxel.height//2+9, 'Pause', 0))
                            self.addText(Text(pyxel.width//2-4, pyxel.height//3+18, 'MyDiL', 0))
                            # on complète la tâche
                            if not target_jeton.isComplete():
                                target_jeton.Complete()
                        elif target_jeton.getNb() == 22:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, False)
                            
                        self.INTERFACE = True

                    # gestion objets Mydil cachés
                        if target_jeton.getNb() == 15:
                            if not target_jeton.isComplete():
                                casque = Image(pyxel.width//2, pyxel.height*1/3, 0, 32, 128, 16, 16, 6)
                                self.addTsprite(casque)
                                pancarte = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 192, 24, 8, 6)
                                self.addTsprite(pancarte)
                                if len(self.INVENTORY) == 0:
                                    # texte de la bulle
                                    self.addText(Text(pyxel.width//3.2, pyxel.height-60, target_jeton.getText(), 7))
                                    self.INVENTORY.append(target_jeton)# on ajoute à l'inventaire
                                    
                                    # on complète la tâche
                                    target_jeton.Complete()
                                else:
                                    # texte de la bulle
                                    self.addText(Text(pyxel.width//3.2, pyxel.height-60, 'Deposez votre objet au MyDil\navant de pouvoir recuperer\ncelui-ci.', 7))
                            else:
                                self.INTERFACE = False  # si on essaie de réinteragir avec un objet deja trouvé on n'ouvre pas de menu 
                        elif target_jeton.getNb() == 16:
                            if not target_jeton.isComplete():
                                raspberry = Image(pyxel.width//2, pyxel.height*1/3, 0, 16, 112, 16, 16, 6)
                                self.addTsprite(raspberry)
                                pancarte = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 192, 24, 8, 6)
                                self.addTsprite(pancarte)
                                if len(self.INVENTORY) == 0:
                                    # texte de la bulle
                                    self.addText(Text(pyxel.width//3.2, pyxel.height-60, target_jeton.getText(), 7))
                                    self.INVENTORY.append(target_jeton)# on ajoute à l'inventaire
                                    # on complète la tâche
                                    target_jeton.Complete()
                                else:
                                    # texte de la bulle
                                    self.addText(Text(pyxel.width//3.2, pyxel.height-60, 'Deposez votre objet au MyDil\navant de pouvoir recuperer\ncelui-ci.', 7))
                            else:
                                self.INTERFACE = False  # si on essaie de réinteragir avec un objet deja trouvé on n'ouvre pas de menu 
                        elif target_jeton.getNb() == 17:
                            if not target_jeton.isComplete():
                                robot = Image(pyxel.width//2, pyxel.height*1/3, 0, 0, 128, 16, 16, 6)
                                self.addTsprite(robot)
                                pancarte = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 192, 24, 8, 6)
                                self.addTsprite(pancarte)
                                if len(self.INVENTORY) == 0:
                                    # texte de la bulle
                                    self.addText(Text(pyxel.width//3.2, pyxel.height-60, target_jeton.getText(), 7))
                                    self.INVENTORY.append(target_jeton)# on ajoute à l'inventaire
                                    # on complète la tâche
                                    target_jeton.Complete()
                                else:
                                    # texte de la bulle
                                    self.addText(Text(pyxel.width//3.2, pyxel.height-60, 'Deposez votre objet au MyDil\navant de pouvoir recuperer\ncelui-ci.', 7))
                            else:
                                self.INTERFACE = False  # si on essaie de réinteragir avec un objet deja trouvé on n'ouvre pas de menu 
                        elif target_jeton.getNb() == 18:
                            if not target_jeton.isComplete():
                                manette = Image(pyxel.width//2, pyxel.height*1/3, 0, 0, 112, 16, 16, 6)
                                self.addTsprite(manette)
                                pancarte = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 192, 24, 8, 6)
                                self.addTsprite(pancarte)
                                if len(self.INVENTORY) == 0:
                                    # texte de la bulle
                                    self.addText(Text(pyxel.width//3.2, pyxel.height-60, target_jeton.getText(), 7))
                                    self.INVENTORY.append(target_jeton)# on ajoute à l'inventaire
                                    # on complète la tâche
                                    target_jeton.Complete()
                                else:
                                    # texte de la bulle
                                    self.addText(Text(pyxel.width//3.2, pyxel.height-60, 'Deposez votre objet au MyDil\navant de pouvoir recuperer\ncelui-ci.', 7))
                            else:
                                self.INTERFACE = False  # si on essaie de réinteragir avec un objet deja trouvé on n'ouvre pas de menu 
                        elif target_jeton.getNb() == 19:
                            if not target_jeton.isComplete():
                                imprimante = Image(pyxel.width//2, pyxel.height*1/3, 0, 48, 128, 16, 16, 6)
                                self.addTsprite(imprimante)
                                pancarte = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 192, 24, 8, 6)
                                self.addTsprite(pancarte)
                                if len(self.INVENTORY) == 0:
                                    # texte de la bulle
                                    self.addText(Text(pyxel.width//3.2, pyxel.height-60, target_jeton.getText(), 7))
                                    self.INVENTORY.append(target_jeton)# on ajoute à l'inventaire
                                    # on complète la tâche
                                    target_jeton.Complete()
                                else:
                                    # texte de la bulle
                                    self.addText(Text(pyxel.width//3.2, pyxel.height-60, 'Deposez votre objet au MyDil\navant de pouvoir recuperer\ncelui-ci.', 7))        
                            else:
                                self.INTERFACE = False  # si on essaie de réinteragir avec un objet deja trouvé on n'ouvre pas de menu 
                        for objtext in self.getText:
                            if objtext.getText() == "Appuyez sur 'E' pour interagir": # on supprime le texte d'indication
                                self.removeText(objtext)# suppr le texte d'indication

                else:
                    for objtext in self.getText:
                        if objtext.getText() == "Appuyez sur 'E' pour interagir": # on supprime le texte d'indication
                            self.removeText(objtext)
                        
            else:
                self.KEYS_PRESSED = {'UP':False, 'DOWN':False, 'LEFT':False, 'RIGHT':False}
                # on retire le texte d'indication
                # si on réappuye sur E on ferme le MENU
                if pyxel.btnp(pyxel.KEY_E):
                    # on supprime les textes et la bulle
                    '''for objtext in self.getText:
                        if objtext.getText() in target_jeton.getText() or objtext.getText() in 'Deposez votre objet au MyDil\navant de pouvoir recuperer\ncelui-ci.':
                    '''
                    self.getText.clear()
                    self.Buttons.clear()
                    self.getTsprites.clear() # on supprime les images du menu
                    # on supprimer le jeton après consultation si nécessaire
                    for jeton in self.deleteJeton:
                        if jeton in self.getSprites:
                            self.removeSprite(jeton)
                    pyxel.mouse(False) # on retire la souris

                    # gestion des sites
                    if self.task == 6:
                        path = os.path.join("web", "cours_web.html")
                        url = "file://" + os.path.abspath(path)
                        webbrowser.open(url)
                    elif self.task == 7:
                        path = os.path.join("web", "test_web.html")
                        url = "file://" + os.path.abspath(path)
                        webbrowser.open(url)
                    elif self.task == 9:
                        path = os.path.join("web", "cours_dev.html")
                        url = "file://" + os.path.abspath(path)
                        webbrowser.open(url)
                    elif self.task == 10:
                        path = os.path.join("web", "test_dev.html")
                        url = "file://" + os.path.abspath(path)
                        webbrowser.open(url)
                    elif self.task == 12:
                        path = os.path.join("web", "cours_Market.html")
                        url = "file://" + os.path.abspath(path)
                        webbrowser.open(url)
                    elif self.task == 13:
                        path = os.path.join("web", "test_mark.html")
                        url = "file://" + os.path.abspath(path)
                        webbrowser.open(url)

                    self.INTERFACE = False

        #gestion des jetons à afficher
            jeton = None
            if self.task == 0:
                # on crée le premier jeton à l'entrée de l'EPSI
                jeton = Jeton(0, pyxel.height//2, 0, 0, 40, 8, 8, 3,'Bienvenue à l\'EPSI ! Venez decouvrir la vie\n etudiante sur notre campus le temps d\'une\n journee.\n\n\nCommmence par rendre visite au coach Mydil\npresent au centre du campus !', 0)       
            elif self.task == 1:
                self.TIME = '8h15 - Se rendre au MyDil'
                jeton = Jeton(self.MAP.getPos()[0]-50, self.MAP.getPos()[1]+36, 0, 0, 40, 8, 8, 3,'Bienvenue au MyDil. C\'est ici que tu trouves\n\n tous les objets qui sont a la pointe de la\n\n technologie. Malheureusement tous\n\n ces objets, ce sont fait derober et cacher,\n\n s\'il te plait aide-moi a les trouver.', 1)   
            elif self.task == 2:
                self.TIME = '8h30 - Cours de Reseau'
                jeton = Jeton(self.MAP.getPos()[0]-288, self.MAP.getPos()[1]-112, 0, 0, 40, 8, 8, 3,'Bienvenue dans le cours de reseau. \n\n\nDans ce cours tu vas apprendre a installer un\nserveur web afin de permettre aux autres\n intervenant d\'heberger leur cours au format web\nsur le reseau interne de l\'ecole.\nAssure toi que le réseau est bien\nactif avant de configurer un serveur.', 2)   
            elif self.task == 3:
                self.TIME = '9h30 - Cours de Reseau'
                jeton = Jeton(self.MAP.getPos()[0]-420, self.MAP.getPos()[1], 0, 0, 40, 8, 8, 3,'Configure et met en place un serveur web !\n\nAttention fait les choses dans le bon ordre si tu\nque tout fonctionne correctement.', 3)   
            elif self.task == 4:
                self.TIME = '10h15 - Pause flechette'
                jeton = Jeton(self.MAP.getPos()[0]*2-157, self.MAP.getPos()[1]*2-34, 0, 0, 40, 8, 8, 3,'bruit de flechettes', 4)   
            elif self.task == 5:
                self.TIME = '10h30 - Cours Securite Web'
                jeton = Jeton(self.MAP.getPos()[0]+400, self.MAP.getPos()[1]-160, 0, 0, 40, 8, 8, 3,'Bien le bonjour. Assieds-toi et prends place\n\n\n pour le cours de securite web. Tu vas etre\n\n\n sensibiliser sur la securite a travers une\n epreuve de hacking.', 5)   
            elif self.task == 6:
                self.TIME = '11h30 - Cours Securite Web'
                jeton = Jeton(self.MAP.getPos()[0]+428, self.MAP.getPos()[1]-30, 0, 0, 40, 8, 8, 3,'Le mots de passe est perdu...\n\n\n Trouve un moyen de te connecter ;) ', 6)   
            elif self.task == 7:
                self.TIME = '12h30 - Pause Dejeuner'
                jeton = Jeton(self.MAP.getPos()[0]+332, self.MAP.getPos()[1]*2+50, 0, 0, 40, 8, 8, 3,'**Bruit de Micro-ondes***', 7)   
            elif self.task == 8:
                self.TIME = '13h30 - Cours Programmation'
                jeton = Jeton(self.MAP.getPos()[0]-150, self.MAP.getPos()[1]//10+100, 0, 0, 40, 8, 8, 3,'Assieds-toi!\n\n\n Vous etes ici dans le cours de Programmation.\n\n\n Je vous invite à prendre des notes des\n\n\n  commandes à retenir ',8)   
            elif self.task == 9:
                self.TIME = '14h30 - Cours Programmation'
                jeton = Jeton(self.MAP.getPos()[0], self.MAP.getPos()[1]//10+172, 0, 0, 40, 8, 8, 3,'L\'epreuve est tres simple,\n\n\n fait avancer le robot en trouvant le code correct :) ', 9)   
            elif self.task == 10:
                self.TIME = '15h15 - Pause dans le couloir'
                jeton = Jeton(self.MAP.getPos()[0], self.MAP.getPos()[1]-36, 0, 0, 40, 8, 8, 3,'Blablablablabla', 10)   
            elif self.task == 11:
                self.TIME = '15h30 - Cours Marketing/Communication'
                jeton = Jeton(self.MAP.getPos()[0]//2-50, self.MAP.getPos()[1]//3-30, 0, 0, 40, 8, 8, 3,'Bonjour,Vous etes ici en cours de Marketing.\n\n\n Nous allons voir les différents\n\n\n  types d\'entreprises.', 11)   
            elif self.task == 12:
                self.TIME = '16h30 - Cours Marketing/Communication'
                jeton = Jeton(self.MAP.getPos()[0]*2-50, self.MAP.getPos()[1]//3+10, 0, 0, 40, 8, 8, 3,'Voici un petit questionnaire,\n\n\n  afin de bien choisir son cursus\n\n\n  au sein de l\'etablissement.', 12)   
            elif self.task == 13:
                self.TIME = '17h30 - Remise des Diplomes'
                jeton = Jeton(self.MAP.getPos()[0]-360, self.MAP.getPos()[1]+200, 0, 0, 40, 8, 8, 3,'Prenez place, Expert IT.\n\n\n Vous avez tous obtenu votre diplome\n\n\n  avec franc succes!\n\n\n  Felicitation!!!', 13)   
            else:
                self.TIME = '18h - Game Over'
                jeton = Jeton(self.MAP.getPos()[0]*2+70, self.MAP.getPos()[1]+28, 0, 0, 40, 8, 8, 3,'Vous etes tout a fait libre desormais\n\n\n  pour creer votre propre  entreprise.\n\n\n  avec toutes les competences acquises\n\n\n  pendant votre parcours', 14)   
            # jeton Mydil
            if len(self.INVENTORY) != 0 and self.task > 1:
                jeton = Jeton(self.MAP.getPos()[0], self.MAP.getPos()[1]+28, 0, 0, 40, 8, 8, 3,'Merci beaucoup !\n\nIl reste des objets a trouver, je\n compte sur toi !', 20)
            
            if len(self.getSprites) == 6:# on crée une map au début
                jeton = Jeton(self.MAP.getPos()[0]//3+28, self.MAP.getPos()[1], 0, 0, 40, 8, 8, 3,'map', 21)

            if len(self.getSprites) == 7:# on crée un jeton referent au début
                jeton = Jeton(self.MAP.getPos()[0]*1.95, self.MAP.getPos()[1]*3, 0, 0, 40, 8, 8, 3,'Bonjour, je suis la referent handicap\n\n\n et a l\'EPSI on met tout en oeuvre pour\n\n\n que tout le monde se sante au mieux', 22)
        
            
            # on affiche le jeton sur l'écran
            inList = False
            for j in self.getSprites:
                if isinstance(j, Jeton):
                    if j.getText() == jeton.getText():
                        inList = True
            if not inList:
                self.addSprite(jeton) # si on a pas encore affiché le jeton d'interaction

        # gestion epreuve reseau
            for btn in self.getButton:
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and btn.getPos()[0] < pyxel.mouse_x < btn.getPos()[0]+24 and btn.getPos()[1] < pyxel.mouse_y < btn.getPos()[1]+24:  
                    if len(self.caseCoche) < 4:
                        if btn.getText() == '':
                            self.caseCoche.append(btn)
                            btn.setText(str(len(self.caseCoche)))
                            self.addText(Text(btn.getPos()[0]+6, btn.getPos()[1]+6, btn.getText(), 0))
            # détecte la bonne réponse
            if len(self.caseCoche) == 4 :
                if self.getButton[0].getText() == self.getButton[0].getReponse() and self.getButton[1].getText() == self.getButton[1].getReponse() and self.getButton[2].getText() == self.getButton[2].getReponse() and self.getButton[3].getText() == self.getButton[3].getReponse():
                    self.addText(Text(pyxel.width//3-15, pyxel.height*2/3+8, 'Bravo, tu as reussi le test !', 3))
                    self.caseCoche.clear()
                else:
                    self.addText(Text(pyxel.width//3-15, pyxel.height*2/3+8, 'Tu n\'as pas reussi le test...', 8))
                    self.caseCoche.clear()

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
        pyxel.blt(0, 0, 0, 0, 242, 256, 12)
        pyxel.blt(0, pyxel.height-12, 0, 0, 242, 256, 12)
        
        '''on parcours les sprites et les textes et on les affiche'''
        for s in self.getSprites:
            pyxel.blt(s.draw[0], s.draw[1], s.draw[2], s.draw[3], s.draw[4], s.draw[5], s.draw[6], self.cold_key, 0, s.draw[7])
        for ts in self.getTsprites:
            pyxel.blt(ts.draw[0], ts.draw[1], ts.draw[2], ts.draw[3], ts.draw[4], ts.draw[5], ts.draw[6], self.cold_key, 0, ts.draw[7])
        for b in self.getButton:
            pyxel.blt(b.draw[0], b.draw[1], b.draw[2], b.draw[3], b.draw[4], b.draw[5], b.draw[6], self.cold_key, 0, b.draw[7])
        for t in self.getText:
            pyxel.text(t.draw[0], t.draw[1], t.draw[2], t.draw[3])

         # on affiche l'horloge
        if self.isState('PLAYING'):
            pyxel.text(pyxel.width*1/3,3, self.TIME, 7)
        # on affiche le compteur d'objets
        if self.task >=2:
            pyxel.blt(pyxel.width-10,pyxel.height-10, 0, 8, 48, 8, 8)
            pyxel.text(pyxel.width-23,pyxel.height-8, str(self.nbObjet) + '/5', 7)

App()