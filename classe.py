# -*-coding:utf-8-*
__author__ = "acf-patrick"

""" Module où les classes utiles au programme sont déclarées """

import pygame
from random import randrange
from pygame.locals import*
from constante import*
import os

#Objet>>Plateau>>Moteur
#Variable globale

humain=pygame.image.load("data/humain.jpg")
ordinateur=pygame.image.load("data/ordinateur.jpg")
img_menu=pygame.image.load("data/menu.jpg")
background=pygame.image.load("data/background.jpg")
Pygame=pygame.image.load("data/pygame.png")
pos=(WIDTH-Pygame.get_width(), HEIGHT-Pygame.get_height())
RED=(255,0,0)
BLACK=(0,0,0)

def opp(t):
    if t==X:
        return O
    elif t==O:
        return X
def estime(t):
    if t[0]==1:
        return 30*t[1]
    elif t[0]==2:
        return 50*t[1]
    else:
        return 0
class Objet:
    def __init__(self, x=0, y=0):
        """Objet(tuple, int) -> Objet"""
        self.image=pygame.Surface((70,70))
        self.type=VIDE
        self.vide=True#un booleen ,simple quéstion de lisibilité
        self.x=case[x][y][0]#coordonnées en pixel..Rappelons que 'case' est une liste bidimensionnelle de tuple
        self.y=case[x][y][1]
    def __eq__(self, objet):#Surcharge de l'operateur égalité
        return objet.type==self.type
    def aff(self, screen):
        """affiche l'objet en quéstion
          aff(Surface ) -> None"""
        if self.type is not VIDE:
            screen.blit(self.image ,(self.x, self.y))
    def clic(self, x, y):
        """Gestion du clic
           clic(int, int) -> bool"""
        return ((self.x<x and x<self.x+self.image.get_width())and (self.y<y and y<self.y+self.image.get_height()))
    def setType(self, t):
        """Met à jour le type de l'objet
           setType(int ) -> None""" 
        self.type=t
        self.vide=(t is VIDE)
        if t is O:
            self.image=pygame.image.load("data/rond.jpg")
        elif t is X:
            self.image=pygame.image.load("data/x.jpg")
        else:
            self.image=pygame.Surface((70,70))

vide=Objet()
class Plateau:
    def __init__(self):
        self.tab=[[Objet(0,0), Objet(0,1), Objet(0,2)],
                   [Objet(1,0), Objet(1,1), Objet(1,2)],
                   [Objet(2,0), Objet(2,1), Objet(2,2)]]
        self.remplie=False
        self.nulle=True#la Partie est nulle
    def fini(self):
        """Methode qui verifie si le jeu est terminé ou le plateau est rempli"""
        #Verification si le plateau est rempli
        self.remplie=True
        for ligne in self.tab:
            for objet in ligne:
                if objet.vide:
                    self.remplie=False
                    break
        #Verification des lignes
        for ligne in self.tab:
            if not ligne[0].vide:#On verifie si le premier element de la ligne n'est pas vide
                if (ligne[0]==ligne[1]==ligne[2]):
                    self.nulle=False
                    return True
        #Verification des colonnes
        i=0
        while i<3:
            if not self.tab[0][i].vide and (self.tab[0][i]==self.tab[1][i]==self.tab[2][i]):
                self.nulle=False
                return True
            i+=1
        #Verification des diagonales
            #Droite à Gauche
        if not self.tab[0][0].vide and (self.tab[0][0]==self.tab[1][1]==self.tab[2][2]):
            self.nulle=False
            return True
            #Gauche à Droite
        if not self.tab[0][2].vide and (self.tab[0][2]==self.tab[1][1]==self.tab[2][0]):
            self.nulle=False
            return True
        if self.remplie:
            return True
        #Si on est arrivé ici c'est que tout les tests ont échoué
        return False

    def clean(self):
        i=0
        j=0
        while i<3:
            while j<3:
                self.tab[i][j].setType(VIDE)
                j+=1
            j=0
            i+=1
            
    def aff(self, screen):
        """Methode qui affiche le plateau de jeu"""
        for ligne in self.tab:
            for elt in ligne:
                elt.aff(screen)#Rien de spéciale, on affiche
                               #chaque case du plateau
    def coup(self):
        """Retourne le nombre coup jouer depuis le début
           coup(...) -> int"""
        cmp=0
        for ligne in self.tab:
            for elt in ligne:
                if elt.type is not VIDE:
                    cmp+=1
        return cmp
        
    def gagnant(self):
        """Methode qui retourne le type du joueur gagnant"""
        if self.fini():#Si le jeu est terminé
            for ligne in self.tab:
                if ligne[0].type is not VIDE and ligne[0]==ligne[1]==ligne[2]:
                    return ligne[0].type
            i=0
            while i<3:
                if self.tab[0][i].type is not VIDE:
                    if self.tab[0][i]==self.tab[1][i]==self.tab[2][i]:
                        return self.tab[0][i].type
                i+=1
            if self.tab[0][0].type is not VIDE:
                if self.tab[0][0]==self.tab[1][1]==self.tab[2][2]:
                    return self.tab[1][1].type
            if self.tab[0][2].type is not VIDE:
                if self.tab[0][2]==self.tab[1][1]==self.tab[2][0]:
                    return self.tab[1][1].type
        #Autrement il n'y a pas ou il n'y a pas encore de vainqeur
        return VIDE
    
class IA:
    def __init__(self, t):
        self.type=t
        self.first= (t==O)
    def evalue(self, plateau):
        i=0
        t=[0,0]
        score=0
        if plateau.fini():
            if plateau.gagnant() is self.type:
                return 1000-plateau.coup()
            elif plateau.gagnant() is opp(self.type):
                return -1000+plateau.coup()
            else:
                return 0

        while i<3:
            if plateau.tab[i][i].type is not VIDE:
                t[0]+=1
                if plateau.tab[i][i].type is self.type:
                    t[1]+=1
                else:
                    t[1]-=1
            i+=1
        score+=estime(t)
        
        i=0
        t=[0,0]
        while i<3:
            if plateau.tab[i][2-i].type is not VIDE:
                t[0]+=1
                if plateau.tab[i][2-i].type is self.type:
                    t[1]+=1
                else:
                    t[1]-=1
            i+=1
        score+=estime(t)
        
        for ligne in plateau.tab:
            t=[0,0]
            for elt in ligne:
                if elt.type is not VIDE:
                   t[0]+=1
                   if elt.type is self.type:
                       t[1]+=1
                   else:
                       t[1]-=1
            score+=estime(t)

        i=0
        j=0
        while i<3:
            t=[0, 0]
            while j<3:
                if plateau.tab[j][i].type is not VIDE:
                    t[0]+=1
                    if plateau.tab[j][i].type is self.type:
                        t[1]+=1
                    else:
                        t[1]-=1
                j+=1
            j=0
            i+=1
            score+=estime(t)
        return score
    
    def joue(self, plateau):
        i=0
        j=i
        tmp=0
        maxI=-1
        maxJ=-1
        MAX=-INFINI
        if not  plateau.fini():
            while i<3 and not self.first:
                while j<3:
                    if plateau.tab[i][j].type is VIDE:
                        plateau.tab[i][j].setType(self.type)
                        tmp=self.evalue(plateau)
                        if MAX<tmp:
                            MAX=tmp
                            maxI=i
                            maxJ=j
                        plateau.tab[i][j].setType(VIDE)
                    j+=1
                j=0
                i+=1
        if self.first:
                (maxI, maxJ)=(randrange(3),randrange(3))
                self.first=False
        plateau.tab[maxI][maxJ].setType(self.type)

    """def Min(self, plateau, prof):
        i=0
        j=0
        if prof==0 or plateau.fini():
            return self.evalue(plateau)
        MIN=INFINI
        tmp=0
        while i<3:
            while j<3:
                if plateau.tab[i][j].type is VIDE:
                    plateau.tab[i][j].setType(self.type)
                    tmp=self.Max(plateau, prof-1)
                    MIN=min(tmp, MIN)
                    plateau.tab[i][j].setType(VIDE)
                j+=1
            j=0
            i+=1
        return MIN
    def Max(self, plateau, prof):
        i=0
        j=0
        if prof==0 or plateau.fini():
            return self.evalue(plateau)
        MAX=-INFINI
        tmp=0
        while i<3:
            while j<3:
                if plateau.tab[i][j].type is VIDE:
                    plateau.tab[i][j].setType(self.type)
                    tmp=self.Min(plateau, prof-1)
                    MAX=max(tmp, MAX)
                    plateau.tab[i][j].setType(VIDE)
                j+=1
            j=0
            i+=1
        return MAX"""
class Moteur:
    """Moteur de jeu"""
    def __init__(self):
        self.j1=HUMAIN
        self.j2=HUMAIN
        self.plateau=Plateau()
        self.tour=O
    def isHuman(self):
        """Retourne le type du joueur en fonction de ces pions"""
        if self.tour==O:
            return self.j1==HUMAIN
        else:
            return self.j2==HUMAIN
    def aff(self , j,screen):
        """Methode utile uniquement à la méthode menu
        aff(int, int, Surface) -> None
        """
        if j==1:
            Type=self.j1
            if Type==HUMAIN:
                screen.blit(humain, POSJ1)
            if Type==ORDINATEUR:
                screen.blit(ordinateur, POSJ1)
        if j==2:
            Type=self.j2
            if Type==HUMAIN:
                screen.blit(humain, POSJ2)
            if Type==ORDINATEUR:
                screen.blit(ordinateur, POSJ2)
    def menu(self, screen):
        """Methode qui gère le menu du jeu
          menu(Surface) -> int
          """
        j1=HUMAIN
        j2=j1
        screen.blit(img_menu, (0,0))
        screen.blit(humain, POSJ1)
        screen.blit(humain, POSJ2)
        screen.blit(Pygame, pos)
        while True:
            pygame.display.flip()
            event=pygame.event.wait()
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                return QUITTER
            if event.type==MOUSEBUTTONUP:
                x=event.pos[0]
                y=event.pos[1]
                if (POSJ1[0]<x and x<MAX_POSJ1[0])and(POSJ1[1]<y and y<MAX_POSJ1[1]):
                    j1+=1
                    j1%=2
                    self.j1=j1
                    self.aff(1,screen)
                if (POSJ2[0]<x and x<MAX_POSJ2[0])and(POSJ2[1]<y and y<MAX_POSJ2[1]):
                    j2+=1
                    j2%=2
                    self.j2=j2
                    self.aff(2, screen)
                if (MIN_QUITTER[0]<x and x<MAX_QUITTER[0])and(MIN_QUITTER[1]<y and y<MAX_QUITTER[1]):
                    return QUITTER
                if (MIN_NOUVEAU[0]<x and x<MAX_NOUVEAU[0])and(MIN_NOUVEAU[1]<y and y<MAX_NOUVEAU[1]):
                    return JEU
    def jeu(self, screen):
        """Le Jeu ...jeu(Surface )-> int"""
        first=True
        screen.blit(background, (0,0))
        self.plateau=Plateau()
        self.tour=O #Les ronds commencent
        j1=self.j1
        j2=self.j2
        if j1 is not HUMAIN:
            ia=IA(O)
        if j2 is not HUMAIN:
            ia1=IA(X)
        while not self.plateau.fini():
            i=0
            j=0
            pygame.display.flip()
            if not self.isHuman():#Si ce n'est pas à un humain de jouer
                if j1 is not HUMAIN:#Savoir lequel n'est pas un humain
                    if ia.type is self.tour:#Savoir si c'est vraiment son tour
                        ia.joue(self.plateau)
                        self.tour=opp(self.tour)
                if j2 is not HUMAIN:
                    if ia1.type is self.tour:
                        ia1.joue(self.plateau)
                        self.tour=opp(self.tour)
            
            for event in pygame.event.get():
                pygame.time.Clock().tick(30)
                if event.type==QUIT:
                    return QUITTER
                if event.type==KEYDOWN:
                    if event.key==K_ESCAPE:
                        return QUITTER
                    if event.key==K_SPACE:
                        return MENU
                if event.type==MOUSEBUTTONUP:
                    if event.button==1:
                        x=event.pos[0]
                        y=event.pos[1]
                        if self.isHuman():
                            while i<3:
                                while j<3:
                                    if self.plateau.tab[i][j].clic(x, y) and self.plateau.tab[i][j].type is VIDE:
                                        self.plateau.tab[i][j].setType(self.tour)
                                        self.tour=opp(self.tour)
                                    j+=1
                                j=0
                                i+=1
            self.plateau.aff(screen)
        return APRES_JEU
    def apres_jeu(self, screen):
        """Methode qui affiche qui a gagné et demande si l'on veut rejouer ou non
           apres_jeu(Surface ) -> int"""
        #la variable temporaire 'tmp' servira pour rendre le fond un peu flou
        tmp=pygame.Surface((WIDTH, HEIGHT))
        tmp.fill(BLACK)
        tmp.set_alpha(120)
        screen.blit(tmp, (0,0))
        police=pygame.font.Font("data/pol.ttf", 40)
        if self.plateau.gagnant() is not VIDE:
            if self.plateau.gagnant() is O:
                texte=police.render("Nandresy ny mpilalao1!", True, RED)
            else:
                texte=police.render("Nandresy ny mpilalao2!", True, RED)
        elif self.plateau.gagnant() is VIDE:
            texte=police.render("Sahala!", True, RED)
        screen.blit(texte, (20,20))
        rejouer=pygame.image.load("data/rejouer.jpg")
        quitter=pygame.image.load("data/quitter.jpg")
        _menu=pygame.image.load("data/_menu.jpg")
        rejouer.set_colorkey(BLACK)
        quitter.set_colorkey(BLACK)
        _menu.set_colorkey(BLACK)
        screen.blit(rejouer, MIN_REJOUER)
        screen.blit(quitter, MIN_QUITTER)
        screen.blit(_menu, MIN_MENU)
        pygame.display.flip()
        self.plateau.clean()
        while True:
            event=pygame.event.wait()
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                return QUITTER
            if event.type==MOUSEBUTTONUP:
                x=event.pos[0]
                y=event.pos[1]
                if MIN_REJOUER[0]<x and x<MAX_REJOUER[0] and MIN_REJOUER[1]<y and y<MAX_REJOUER[1]:
                    return JEU
                if MIN_MENU[0]<x and x<MAX_MENU[0] and MIN_MENU[1]<y and y<MAX_MENU[1]:
                    self.j1=HUMAIN
                    self.j2=self.j1
                    return MENU
                if MIN_QUITTER2[0]<x and x<MAX_QUITTER2[0] and MIN_QUITTER2[1]<y and y<MAX_QUITTER2[1]:
                    return QUITTER
