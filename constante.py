# -*-coding:utf-8-*
__author__ = "acf-patrick"
"""Module où les constantes sont définies"""

VIDE=0
O=1#rond
X=2

HUMAIN=0
ORDINATEUR=1

MENU=0
JEU=1
APRES_JEU=2
QUITTER=3

WIDTH=408
HEIGHT=408

POSJ1=(18,195)
POSJ2=(238,193)
MAX_POSJ1=(POSJ1[0]+110, POSJ1[1]+40)
MAX_POSJ2=(POSJ2[0]+110, POSJ2[1]+40)
MIN_QUITTER=(128,295)
MAX_QUITTER=(237,330)
MIN_NOUVEAU=(124,252)
MAX_NOUVEAU=( 260 , 285 )

MIN_REJOUER=(41,198)
MAX_REJOUER=(187,258)
MIN_MENU=( 237 , 197 )
MAX_MENU=( 365 , 248 )
MIN_QUITTER2=( 148 , 310 )
MAX_QUITTER2=( 288 , 362 )

INFINI=10000

case=[]
i=0
j=0
while i<3:
    case.append([])
    while j<3:
        case[i].append(())
        j+=1
    j=0
    i+=1
case[0][0]=(69,81)
case[0][1]=(162,80)
case[0][2]=(265,80)
case[1][0]=(67,169)
case[1][1]=(164,169)
case[1][2]=(264,174)
case[2][0]=(67,260)
case[2][1]=(164,262)
case[2][2]=(265, 265)
