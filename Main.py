import pyxel
import webbrowser
import os
from Sprites.Player import Player
from Sprites.Map import Map
from Sprites.Image import Image
from Sprites.Jeton import Jeton
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
        self.deleteJeton = []
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
                x = Image(pyxel.width/8.5, pyxel.height/1.7, 0, 16, 16, 207, 16, 1)
                self.addTsprite(x)
                # texte menu informations
                text = Text(pyxel.width // 2 - 40, pyxel.height // 2 + 60, "Menu d'information(i)", 5)
                self.addText(text)
        #Screen information
            if pyxel.btnp(pyxel.KEY_I): 
                if self.INTERFACE==True:
                    self.removeTsprite(self.getTsprites[-1])
                    # texte menu informations
                    text = Text(pyxel.width // 2 - 40, pyxel.height // 2 + 60, "Menu d'information(i)", 5)
                    self.addText(text)
                    self.INTERFACE=False
                else:
                    menu = Image(95,110,0,0,168,64,64,3)
                    self.addTsprite(menu)
                    self.removeText(self.getText[-1]) # on supprime le texte du menu d'informations
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
                player = Player(pyxel.width//2-4, pyxel.height//2-4, 0, 8, 0, 8, 8) 
                self.addSprite(player)
                # crée les objets manquant du MyDil
                objet1 = Jeton(self.MAP.getPos()[0], self.MAP.getPos()[1], 0, 0, 48, 8, 8, '     Casque virtuel !\n\n\nRapporte le vite au MyDil', 15)
                objet2 = Jeton(self.MAP.getPos()[0]+20, self.MAP.getPos()[1], 0, 0, 48, 8, 8, "    Carte Raspberry !\n\n\nRapporte le vite au MyDil", 16)
                objet3 = Jeton(self.MAP.getPos()[0]+40, self.MAP.getPos()[1], 0, 0, 48, 8, 8, "         Robot !\n\n\nRapporte le vite au MyDil", 17)
                objet4 = Jeton(self.MAP.getPos()[0]+60, self.MAP.getPos()[1], 0, 0, 48, 8, 8, "        Manette !\n\n\nRapporte le vite au MyDil", 18)
                objet5 = Jeton(self.MAP.getPos()[0]+80, self.MAP.getPos()[1], 0, 0, 48, 8, 8, "      Imprimante 3D !\n\n\nRapporte le vite au MyDil", 19)
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
                        self.addText(Text(pyxel.width//3, pyxel.height//2+20, "Press 'E' to interact", 7))

                    if pyxel.btnp(pyxel.KEY_E):
                    # gestion des MENUS jetons interactions
                        if target_jeton.getNb() == 0:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))

                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)
                            self.TIME = '8h15 - Se rendre au MyDil'

                        elif target_jeton.getNb() == 1:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, False)
                            self.TIME = '8h30 - Cours de Reseau'

                        elif target_jeton.getNb() == 2:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))              
                            self.CompleteTask(target_jeton, False)
                            self.TIME = '9h30 - Cours de Reseau'

                        elif target_jeton.getNb() == 3:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 8)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)
                            self.TIME = '10h15 - Pause flechette'

                        elif target_jeton.getNb() == 4:
                            bulle = Image(pyxel.width//2-8,pyxel.height*4/5, 2, 32, 200, 32, 32, 8)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//7, pyxel.height//1.47, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, False)
                            self.TIME = '10h30 - Cours Securité Web'
                        
                        elif target_jeton.getNb() == 5:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            
                            # on ouvre une page web
                            path = os.path.join("web", "cours_web.html")
                            url = "file://" + os.path.abspath(path)
                            webbrowser.open(url)
                            
                            # on complète la tâche
                            self.CompleteTask(target_jeton, False)
                            self.TIME = '11h30 - Cours Securité Web'
                        
                        elif target_jeton.getNb() == 6:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            
                            # on ouvre une page web
                            path = os.path.join("web", "test_web.html")
                            url = "file://" + os.path.abspath(path)
                            webbrowser.open(url)
                            
                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)
                            self.TIME = '12h30 - Pause Dejeuner'

                        elif target_jeton.getNb() == 7:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, False)
                            self.TIME = '13h30 - Cours Programmation'

                        elif target_jeton.getNb() == 8:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, False)
                            self.TIME = '14h30 - Cours Programmation'

                        elif target_jeton.getNb() == 9:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)
                            self.TIME = '15h15 - Pause dans le couloir'

                        elif target_jeton.getNb() == 10:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)
                            self.TIME = '15h30 - Cours Marketing/Communication'

                        elif target_jeton.getNb() == 11:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, False)
                            self.TIME = '16h30 - Cours Marketing/Communication'
                        
                        elif target_jeton.getNb() == 12:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)
                            self.TIME = '17h30 - Remise des Diplomes'
                        
                        elif target_jeton.getNb() == 13:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)
                            self.TIME = '18h - Sortir de l\'EPSI'
                        
                        elif target_jeton.getNb() == 14:
                            bulle = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 200, 32, 32, 7)
                            self.addTsprite(bulle)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//8, pyxel.height//1.47, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)
                            self.TIME = '18h - Game Over'

                    # gestion objets Mydil cachés
                        elif target_jeton.getNb() == 15:
                            pancarte = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 192, 24, 8, 6)
                            self.addTsprite(pancarte)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//3.2, pyxel.height-60, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)

                        elif target_jeton.getNb() == 16:
                            pancarte = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 192, 24, 8, 6)
                            self.addTsprite(pancarte)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//3.2, pyxel.height-60, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)

                        elif target_jeton.getNb() == 17:
                            pancarte = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 192, 24, 8, 6)
                            self.addTsprite(pancarte)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//3.2, pyxel.height-60, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)
                        
                        elif target_jeton.getNb() == 18:
                            pancarte = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 192, 24, 8, 6)
                            self.addTsprite(pancarte)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//3.2, pyxel.height-60, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)
                        
                        elif target_jeton.getNb() == 19:
                            pancarte = Image(pyxel.width//2-10,pyxel.height*4/5, 2, 32, 192, 24, 8, 6)
                            self.addTsprite(pancarte)
                            # texte de la bulle
                            self.addText(Text(pyxel.width//3.2, pyxel.height-60, target_jeton.getText(), 7))
                            # on complète la tâche
                            self.CompleteTask(target_jeton, True)
                        

                        for objtext in self.getText:
                            if objtext.getText() == "Press 'E' to interact": # on supprime le texte d'indication
                                self.removeText(objtext)# suppr le texte d'indication

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
                    # on supprime les textes et la bulle
                    for objtext in self.getText:
                        if objtext.getText() in target_jeton.getText():
                            self.removeText(objtext)
                    self.removeTsprite(self.getTsprites[-1])
                    # on supprimer le jeton après consultation si nécessaire
                    for jeton in self.deleteJeton:
                        if jeton in self.getSprites:
                            self.removeSprite(jeton)
                    self.INTERFACE = False

        #gestion des jetons à afficher
            if self.task == 0 and len(self.getSprites) == 6:
                # on crée le premier jeton à l'entrée de l'EPSI
                jeton_entree = Jeton(0, pyxel.height//2, 0, 0, 40, 8, 8, 'Bienvenue à l\'EPSI ! Venez decouvrir la vie\n etudiante sur notre campus le temps d\'une\n journee.\n\n\nCommmence par rendre visite au coach Mydil\npresent au centre du campus !', 0)   
                self.addSprite(jeton_entree)    
            elif self.task == 1 and len(self.getSprites) == 7:
                jeton_mydil = Jeton(self.MAP.getPos()[0]-50, self.MAP.getPos()[1]+36, 0, 0, 40, 8, 8, 'Bienvenue au MyDil. C\'est ici que tu trouves\n\n\n tous les objets qui sont a la pointe de la\n\n\n technologie. Malheureusement on m\'a cacher tous\n\n\n c\'est objet, s\'il vous plaît aidez-moi.', 1)   
                self.addSprite(jeton_mydil) 
            elif self.task == 2 and len(self.getSprites) == 8:
                jeton_reseau_cours = Jeton(self.MAP.getPos()[0]-288, self.MAP.getPos()[1]-112, 0, 0, 40, 8, 8, 'Bienvenue dans le cours de reseau. J\'ai\n\n\n effectivement l\'un des objets que tu cherches.\n\n\n Or j\'ai d\'abord besoin de toi pour retablir le\n\n\n reseau. Relie les differents materiels pour remettre \n\n\nle reseau en place.', 2)   
                self.addSprite(jeton_reseau_cours) 
            elif self.task == 3 and len(self.getSprites) == 9:
                jeton_reseau_epreuve = Jeton(self.MAP.getPos()[0]-420, self.MAP.getPos()[1], 0, 0, 40, 8, 8, 'Bienvenue au cours de WEB. Dans ce cours, tu\n\n\n devras te reconnaitre à mon compte, or à chaque fois\n\n\n j\'oublie mon mdp. Je me souviens juste que je l\'ai\n\n\n mis dans mon code. Si tu le retouve, je te\n\n\n donne l\'objet', 3)   
                self.addSprite(jeton_reseau_epreuve) 
            elif self.task == 4 and len(self.getSprites) == 10:
                jeton_pause = Jeton(self.MAP.getPos()[0]*2-157, self.MAP.getPos()[1]*2-34, 0, 0, 40, 8, 8, 'Salut et Bienvenue au cours de DEV.\n\n\n Si tu es la, c\'est que tu dois sûrement vouloir\n\n\n l\'objet. Je te le donne que si tu m\'aides pour ce\n\n\n petit programme sur lequel j\'ai du mal.', 4)   
                self.addSprite(jeton_pause)
            elif self.task == 5 and len(self.getSprites) == 11:
                jeton_web_cours = Jeton(self.MAP.getPos()[0]+400, self.MAP.getPos()[1]-160, 0, 0, 40, 8, 8, 'Bien le bonjour. Assieds-toi et prends place\n\n\n pour le cours de securite web. Si tu restes assez\n\n\n assidue,tu pourras recuperer l\'objet perdu.', 5)   
                self.addSprite(jeton_web_cours)
            elif self.task == 6 and len(self.getSprites) == 12:
                jeton_web_epreuve = Jeton(self.MAP.getPos()[0]+428, self.MAP.getPos()[1]-30, 0, 0, 40, 8, 8, 'Le mots de passe est perdu...\n\n\n Trouve un moyen de te connecter ;) ', 6)   
                self.addSprite(jeton_web_epreuve)
            elif self.task == 7 and len(self.getSprites) == 13:
                jeton_midi = Jeton(self.MAP.getPos()[0]+332, self.MAP.getPos()[1]*2+50, 0, 0, 40, 8, 8, '**Bruit de Micro-ondes***', 7)   
                self.addSprite(jeton_midi)
            elif self.task == 8 and len(self.getSprites) == 14:
                jeton_dev_cours = Jeton(self.MAP.getPos()[0]-150, self.MAP.getPos()[1]//10+100, 0, 0, 40, 8, 8, 'Assieds-toi!\n\n\n Vous etes ici dans le cours de Programmation.\n\n\n Je vous invite à prendre des notes des\n\n\n  commandes à retenir ',8)   
                self.addSprite(jeton_dev_cours)
            elif self.task == 9 and len(self.getSprites) == 15:
                jeton_dev_epreuve = Jeton(self.MAP.getPos()[0], self.MAP.getPos()[1]//10+172, 0, 0, 40, 8, 8, 'L\'epreuve etant simple,\n\n\n il faut faire avancer le robot\n\n\n  en trouvant le code correct :) ', 9)   
                self.addSprite(jeton_dev_epreuve)
            elif self.task == 10 and len(self.getSprites) == 16:
                jeton_pause_aprem = Jeton(self.MAP.getPos()[0], self.MAP.getPos()[1]-36, 0, 0, 40, 8, 8, 'Blablablablabla', 10)   
                self.addSprite(jeton_pause_aprem)
            elif self.task == 11 and len(self.getSprites) == 17:
                jeton_marketing_cours = Jeton(self.MAP.getPos()[0]//2-50, self.MAP.getPos()[1]//3-30, 0, 0, 40, 8, 8, 'Bonjour,Vous etes ici en cours de Marketing.\n\n\n Nous allons voir les différents\n\n\n  types d\'entreprises.', 11)   
                self.addSprite(jeton_marketing_cours)
            elif self.task == 12 and len(self.getSprites) == 18:
                jeton_marketing_epreuve = Jeton(self.MAP.getPos()[0]*2-50, self.MAP.getPos()[1]//3+10, 0, 0, 40, 8, 8, 'Voici un petit questionnaire,\n\n\n  afin de bien choisir son cursus\n\n\n  au sein de l\'etablissement.', 12)   
                self.addSprite(jeton_marketing_epreuve)
            elif self.task == 13 and len(self.getSprites) == 19:
                jeton_remise_diplome = Jeton(self.MAP.getPos()[0]-360, self.MAP.getPos()[1]+200, 0, 0, 40, 8, 8, 'Prenez place, les ingénieurs informatiques.\n\n\n Vous avez tous obtenu votre diplome\n\n\n  avec franc succes!\n\n\n  Felicitation!!!', 13)   
                self.addSprite(jeton_remise_diplome)
            elif self.task == 14 and len(self.getSprites) == 20:
                jeton_creation_boite = Jeton(self.MAP.getPos()[0]*2+70, self.MAP.getPos()[1]+28, 0, 0, 40, 8, 8, 'Vous etes tout a fait libre desormais\n\n\n  pour creer votre propre  entreprise.\n\n\n  avec toutes les competences acquises\n\n\n  pendant votre parcours', 14)   
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