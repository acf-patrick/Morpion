# -*-coding:utf-8 -*
__author__ = "acf-patrick"

import pygame
from pygame.locals import*
from constante import*
from classe import*

moteur=Moteur()
pygame.init()
pygame.display.set_icon(pygame.image.load("data/icone.ico"))
pygame.display.set_caption("Morpion 1.0")
screen=pygame.display.set_mode((WIDTH,HEIGHT));
done=False
choix=MENU
while not done:
    if choix==MENU:
        choix=moteur.menu(screen)
    if choix==JEU:
        choix=moteur.jeu(screen)
    if choix==APRES_JEU:
        choix=moteur.apres_jeu(screen)
    if choix==QUITTER:
        done=True
pygame.quit()
