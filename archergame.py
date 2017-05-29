import pygame, os
pygame.init()
gameDisplay=pygame.display.set_mode((1980,1080))
pygame.display.set_caption("archer")
pygame.display.update()
gameExit=False
import time
from scipy.integrate import odeint
import numpy as np
import math
import matplotlib.pyplot as plt



def loadSprite(fileName):
    return pygame.image.load(fileName).convert_alpha()


def convert(g):
    return g/57.2958

def ganho(x):
    listaganho=[]
    for i in range (len(x)-1):
        listaganho.append((float("{0:.2f}".format(round(x[i+1]-x[i],2)))))
    return listaganho

def gerarlistas(x,x1):
    lista=[]
    for i in range(x,x1+1):
        lista.append(i)
    return(lista)
def gerarlistaL(x,y):
    lista=[]
    for i in range(x):
        lista.append(y)
    return lista

t=np.arange(0,500,0.1)
pho=1.225
Cd=0.05
A=0.002
m=0.5
k=1300
x=0.8
def EqDifArrasto(S, t):
    X=S[0]
    Y=S[1]
    Vx=S[2]
    Vy=S[3]

    V=math.sqrt(Vx**2+Vy**2)
    seno=Vy/V
    cosseno=Vx/V
    Arrasto=(1/2)*pho*V**2*Cd*A
    Arrastox=Arrasto*cosseno
    Arrastoy=Arrasto*seno
    dXdt=Vx
    dYdt=Vy
    dVxdt=-Arrastox/m
    dVydt=-10-Arrastoy/m
    return [dXdt, dYdt, dVxdt, dVydt]

def angulacao(angulo):
    lista=[]
    lista2=[]
    listacy=[]
    listacx=[]
    S0=[20,1,math.sqrt((k*(x**2))/m)*math.cos(convert(angulo)),math.sqrt((k*(x**2))/m)*math.sin(convert(angulo))]
    SArrasto=odeint(EqDifArrasto, S0, t)
    for j in range(len(SArrasto[:,1])):
        if SArrasto[:,1][j]>-8:
            lista.append(SArrasto[:,1][j])
            lista2.append(SArrasto[:,0][j])
        else:
            pass
    for i in lista:
        listacy.append(1*(float("{0:.2f}".format(round(i,2)))))
    for i in lista2:
        listacx.append(1*(float("{0:.2f}".format(round(i,2)))))

    return (listacx,listacy)

class arrow:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.current_img=pygame.transform.scale(loadSprite("arrow.png"),(200,100))
        self.current_frame=0
        self.last_update=0
        self.moveright=False
        self.moveleft=False

    def load_images(self):
        self.arrow=pygame.transform.scale(loadSprite("arrow.png"),(200,100))
        self.hurtarrow=pygame.transform.scale(loadSprite("hurtarrow.png"),(200,100))

    def move(self,x):
        if x=="right":
            self.moveright=True
        if x=="left":
            self.moveleft=True
        if x=="again":
            self.x=200
            self.y=733
            self.current_frame=0
            self.moveright=False
            self.apple=False
            self.current_img=pygame.transform.scale(loadSprite("arrow.png"),(200,100))
            alvo.current_img=alvosc

    def update(self):
        if self.moveright==True:
            listax=(angulacao(62)[0])
            listay=(angulacao(62)[1])
            ganhox=ganho(listax)
            ganhoy=ganho(listay)
            self.current_frame=(self.current_frame+1)%len(listax)
            self.x=self.x+(ganhox[self.current_frame-1]*8)
            self.y=self.y+(ganhoy[self.current_frame-1]*-1*8)
            if self.current_frame==(len(listax)-1):
                self.moveright=False
            elif 650<self.y<690 and 1240<self.x<1280:
                self.apple=True
                self.current_img=applearrow
                alvo.current_img=pygame.transform.scale(loadSprite("alvonoapple.png"),(200,200))
            elif 700<=self.y<=802 and 1260<=self.x<=1300 and self.apple==False:
                self.current_img=hurtarrow
                self.moveright=False



class objeto:
    def __init__(self,x,y,s):
        self.x=x
        self.y=y
        self.current_img=s

fundo=pygame.image.load("background.png")
BackiGround1 =pygame.image.load("background.png")
BackGround=pygame.transform.scale(BackiGround1,(1980,1080))
archer=loadSprite("archer.png")
archerC=pygame.transform.scale(archer,(200,200))
alvos=loadSprite("alvo.png")
alvosc=pygame.transform.scale(alvos,(200,200))
hurtarrow=pygame.transform.scale(loadSprite("hurtarrow.png"),(200,100))
applearrow=pygame.transform.scale(loadSprite("applearrow.png"),(200,100))
alvonoapple=pygame.transform.scale(loadSprite("alvonoapple.png"),(200,200))

arrow1=arrow(200,733)
alvo=objeto(1300,680,alvosc)




clock=pygame.time.Clock()

while not gameExit:
    gameDisplay.blit(BackGround, (0, 0))
    gameDisplay.blit(archerC,(200,680))
    gameDisplay.blit(alvo.current_img,(alvo.x,alvo.y))
    gameDisplay.blit(arrow1.current_img,(arrow1.x,arrow1.y))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            gameExit=True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                arrow1.move("right")
            if event.key == pygame.K_a:
                arrow1.move("left")
            if event.key == pygame.K_s:
                arrow1.move("again")
    arrow1.update()
    clock.tick(120)
    pygame.display.update()

pygame.quit()
quit()
