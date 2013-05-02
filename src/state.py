'''
Created on Jan 26, 2013

@author: fabiofilho
'''
from lib import Object,BaseMain,ObjectEvent,Animation,GameState,Text,Form
from objects import Fichas, DrawVector, Vassoura,Balance
import pygame
from pygame.locals import *

#-*- coding: ISO-8859-1 -*-
pygame.init()

class Game(object):

    def __init__(self):

        pygame.init()

        #Chamada do construtor da classe base
        self.main = BaseMain()

        #Rodando Game
        self.runGame = True

        self.State = {"IntroState" : IntroState(),
                             "MainState" : MainState(),
                             "Final" : Final(),
                             "Fase1": Fase1(),"Fase3": Fase3(),
                             "Fase4": Fase4(),"Fase6": Fase6(),
                             "Fase8": Fase8(),"Fase10": Fase10(),
                             "Quit": False}
        pass
    
    def event(self):
        #Inicia a verificacao de enventos da classe
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.runGame = False

                if event.type == pygame.QUIT:
                    self.runGame = False
                else:
                    self.CurrentState.event(event)


            if self.CurrentState.updateState:
                self.nextState()

            
        


    def play(self):

        #Set primeira tela
        self.CurrentState = self.State["Fase4"]

        #Loop Principal
        while self.runGame and not self.CurrentState == False :

            self.dt = self.main.deltaTime()

            self.event()
            
            if not self.CurrentState:
                return

            #Atualiza os objetos da classe
            self.CurrentState.update(self.dt)

            #Pinta na tela
            self.main.draw(self.CurrentState)

            #Atualiza a tela
            self.main.updateScreen()
            pass


        pass

    def nextState(self):

        if not self.State[self.CurrentState.NextCurrentState]:
            self.CurrentState = self.State[self.CurrentState.NextCurrentState]
            return
        else:
            self.State[self.CurrentState.NextCurrentState].draw(self.main.tela)

            self.CurrentState.updateState = Animation(self.CurrentState, self.State[self.CurrentState.NextCurrentState],self.main.telaCurrent,self.main.telaNext,self.CurrentState.effect).drawEffect(self.main.baseSurface,self.dt)


        self.CurrentState = self.State[self.CurrentState.NextCurrentState]

        try:
            self.CurrentState.NextCurrentState = self.CurrentState.StateTemp[1]
            self.CurrentState.updateState = False
        except:
            pass
        try:
            self.CurrentState.quest.NextCurrentState = self.CurrentState.quest.StateTemp[0]
            self.CurrentState.quest.updateState = False
        except:
            pass


        pass



class IntroState(GameState):

    def __init__(self):
        self.backGround = Object("src/Fases/Intro/fundo.png")

        self.NextCurrentState = "MainState"
        self.updateState = False
        self.effect =2
        pass

    def draw(self,tela):
        self.backGround.draw(tela)
        pass

    def event (self,event):
        if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
            self.updateState = True



    def update(self,dt):
        pass


class MainState(GameState):


    def next(self):
        self.updateState = True
        self.NextCurrentState = "Fase1"
        self.effect =2

    def out (self):
        self.updateState = True
        self.NextCurrentState = "Quit"

    def escolaParticular(self):
        self.MainObjects[3].idle = self.MainObjects[3].click
        self.MainObjects[2].idle = self.MainObjects[2].oldIdle
        pass

    def escolaPublica (self):
        self.MainObjects[2].idle = self.MainObjects[2].click
        self.MainObjects[3].idle = self.MainObjects[3].oldIdle
        pass

    def __init__(self):



        self.forms = Form((490,233),195,fontsize=15,bg=(255,255,255),hlcolor=((90,40,40)),maxlines=1)
        self.forms.CURSOR = False

        #Carregando o vetor da fase pelo construtor
        self.backGround = Object("src/Fases/Main/fundo.png")

        self.MainObjects = [ObjectEvent((21,500), "src/Fases/Main/btnSair.png",
                                    "src/Fases/Main/btnSair_move.png",
                                    "src/Fases/Main/btnSair_click.png",self.out),
                            ObjectEvent((875,470),"src/Fases/Main/btnJogar.png",
                                    "src/Fases/Main/btnJogar_move.png",
                                    "src/Fases/Main/btnJogar_click.png",self.next),
                            ObjectEvent((320,376),"src/Fases/Main/btnEscolaPublica.png",
                                    "src/Fases/Main/btnEscolaPublica_click.png",
                                    "src/Fases/Main/btnEscolaPublica_click.png",self.escolaPublica),
                            ObjectEvent((520,376),"src/Fases/Main/btnEscolaParticular.png",
                                    "src/Fases/Main/btnEscolaParticular_click.png",
                                    "src/Fases/Main/btnEscolaParticular_click.png",self.escolaParticular)]


        self.NextCurrentState = "Fase1"
        self.updateState = False
        self.effect = 0

        pass


    def draw(self,tela):

        #Pintando o vetor da fase
        self.backGround.draw(tela)
        DrawVector(self.MainObjects,tela)

        self.forms.show()

        pass


    def event (self,event):

        #self.forms.wakeup(event)

        if event.type == pygame.MOUSEMOTION:
            for q in self.MainObjects:
                q.update(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONDOWN:
            for q in self.MainObjects:
                q.clickStart(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONUP:
            for q in self.MainObjects:
                if q.clickEnd(pygame.mouse.get_pos()):
                    return



    def update(self,dt):
        pass

    pass


class Fase1(GameState):

    def out (self):
        self.updateState = True
        self.NextCurrentState = "Quit"


    def next(self):
        self.updateState = True
        self.effect = 0
        pass

    def help (self):
        print "Help"
        pass

    def __init__(self):



        #Carregando o vetor da fase pelo construtor

        self.backGround = Object("src/Fases/Fase1/fundo.png")

        self.MainObjects = [ObjectEvent((925,100), "src/Fases/Botoes/btnSetaDireita.png",
                                    "src/Fases/Botoes/btnSetaDireita_move.png",
                                    "src/Fases/Botoes/btnSetaDireita_click.png",self.next),
                            ObjectEvent((870,15),"src/Fases/Botoes/btnAjuda.png",
                                    "src/Fases/Botoes/btnAjuda_move.png",
                                    "src/Fases/Botoes/btnAjuda_click.png",self.help),
                            ObjectEvent((955,15),"src/Fases/Botoes/btnSair.png",
                                    "src/Fases/Botoes/btnSair_move.png",
                                    "src/Fases/Botoes/btnSair_click.png",self.out)]


        #========Vassoura
        self.vas = Vassoura("Fase1")
        
        self.balance = Balance(True)
        
        self.ficha = Fichas("Fase1", self.vas)
        
        self.NextCurrentState = "Fase3"
        self.updateState = False

        pass

    def draw(self,tela):

        #Pintando o vetor da fase
        self.backGround.draw(tela)
        DrawVector(self.MainObjects,tela)


        #==========================VASSOURA===============================

        self.vas.draw(tela)
        self.balance.draw(tela,self.ficha.eixosLeft, self.ficha.eixosRight)
        self.ficha.draw(tela)

        pass

    def event (self,event):

        self.ficha.event(event)

        if event.type == pygame.MOUSEMOTION:
            for q in self.MainObjects:
                q.update(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONDOWN:

            for q in self.MainObjects:
                q.clickStart(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONUP:
            for q in self.MainObjects:
                if q.clickEnd(pygame.mouse.get_pos()):
                    return
                pass
            pass


    def update(self,dt):

        self.ficha.update(dt)
        self.vas.update(self.ficha.speed,self.ficha.resultWeigth,dt)

        pass

    pass



class Fase3(GameState):

    def __init__(self):

        self.backGround = Object("src/Fases/Questions/fundo3.png")
        self.quest = Questions("Fase3","Fase4","Fase1",self.backGround)
        self.NextCurrentState = "Fase4"
        self.updateState = False
        self.effect = 0
        pass

    def draw(self,tela):
        self.quest.draw(tela)
        pass

    def event(self,event):

        self.quest.event(event)

        pass

    def update(self,dt):
        self.NextCurrentState = self.quest.NextCurrentState
        self.updateState = self.quest.updateState
        self.effect = self.quest.effect

        pass

    pass


class Fase4(GameState):

    def out (self):
        self.updateState = True
        self.NextCurrentState = "Quit"

    def back (self):
        self.updateState = True
        self.NextCurrentState = self.StateTemp[2]
        self.effect =1

    def next(self):
        self.updateState = True
        self.effect = 0
        pass

    def help (self):
        print "Help"
        pass

    def base (self):
        pass

    def prego (self):
        pass

    def __init__(self):

        #Carregando o vetor da fase pelo construtor

        self.backGround = Object("src/Fases/Fase4/fundo.png")

        self.StateTemp = ["Fase4","Fase6","Fase3"]
        self.NextCurrentState = self.StateTemp[1]
        self.updateState = False
        self.effect = 0


        self.base = [ObjectEvent((740,350),"src/Fases/Vassoura/base.png",None,None,self.base),
                     ObjectEvent((700,300),"src/Fases/Vassoura/prego.png",None,None,self.prego)]

        self.MainObjects = [ObjectEvent((925,100), "src/Fases/Botoes/btnSetaDireita.png",
                                    "src/Fases/Botoes/btnSetaDireita_move.png",
                                    "src/Fases/Botoes/btnSetaDireita_click.png",self.next),
                            ObjectEvent((15,100), "src/Fases/Botoes/btnSetaEsquerda.png",
                                    "src/Fases/Botoes/btnSetaEsquerda_move.png",
                                    "src/Fases/Botoes/btnSetaEsquerda_click.png",self.back),
                            ObjectEvent((870,15),"src/Fases/Botoes/btnAjuda.png",
                                    "src/Fases/Botoes/btnAjuda_move.png",
                                    "src/Fases/Botoes/btnAjuda_click.png",self.help),
                            ObjectEvent((955,15),"src/Fases/Botoes/btnSair.png",
                                    "src/Fases/Botoes/btnSair_move.png",
                                    "src/Fases/Botoes/btnSair_click.png",self.out)]


        #========Vassoura
        self.vas = Vassoura("Fase4")
        
        self.balance = Balance(False)

        self.ficha = Fichas("Fase4",self.vas,self.MainObjects)

        pass

    def draw(self,tela):

        #Pintando o vetor da fase
        self.backGround.draw(tela)

        self.base[0].draw(tela)

        self.vas.draw(tela)

        DrawVector(self.MainObjects,tela)

        self.base[1].draw(tela)

        self.ficha.draw(tela)
       
        self.balance.draw(tela, self.ficha.eixosLeft,self.ficha.eixosRight)           


        pass

    def event (self,event):

        self.ficha.event(event)
        self.vas.event(event)

        if event.type == pygame.MOUSEMOTION:
            for q in self.MainObjects:
                q.update(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONDOWN:
            for base in self.base:
                base.clickStart(pygame.mouse.get_pos())
            for q in self.MainObjects:
                q.clickStart(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONUP:
            for base in self.base:
                base.clickEnd(pygame.mouse.get_pos())
            for q in self.MainObjects:
                if q.clickEnd(pygame.mouse.get_pos()):
                    return
                pass
            pass


    def update(self,dt):

        self.ficha.update(dt,self.vas.vas)
        self.vas.update(self.ficha.speed,self.ficha.resultWeigth,dt)
        
        
        #Base da Vassoura
        
        if self.base[1].state == "Clicking" and not self.vas.vas.state == "Clicking ":
            x,y = pygame.mouse.get_pos()
            self.base[1].rect.x , self.base[1].rect.y = x - self.base[1].rect.width/2, y - self.base[1].rect.height/2
        if self.base[0].state == "Clicking" and not self.vas.vas.state == "Clicking" and not self.base[1].state == "Clicking":
            x,y = pygame.mouse.get_pos()
            self.base[0].rect.x  = x - self.base[0].rect.width/2
        pass
        
        
        #Vassoura
        
        if self.vas.vas.state == "Clicking" and not self.base[1].state == "Clicking":
            x,y = pygame.mouse.get_pos()
            self.vas.vas.rect.x , self.vas.vas.rect.y = x - self.vas.vas.rect.width/2, y -self.vas.vas.rect.height/2
            

        if self.vas.vas.state == "Idle":
            
            loop = True
            while loop:
                if self.vas.vas.rect.y <= 160: 
                    self.vas.vas.rect.y +=1
                else: loop = False    
                
            if self.vas.vas.rect.x < 0 :
                self.vas.vas.rect.x = 0
            elif self.vas.vas.rect.x+self.vas.vas.image.get_width() > 1024:
                self.vas.vas.rect.x = 1024-self.vas.vas.image.get_width()


    
    
        # Balance 
        if self.base[1].state == "Idle" and self.vas.vas.state == "Idle":
            if self.base[1].rect.colliderect(self.vas.vas.rect):
                
                if self.base[1].rect.x < self.vas.vas.rect.x+216:
                    self.base[1].rect.x = self.vas.vas.rect.x + 9*(self.vas.vas.image.get_width()/53)
                    #self.ficha.eixosLeft,self.ficha.eixosRight = self.balance.setLeft()
                    pass
                
                if self.base[1].rect.x >= self.vas.vas.rect.x+216 and self.base[1].rect.x <= self.vas.vas.rect.x+578:
                    self.base[1].rect.x = self.vas.vas.rect.x + self.vas.vas.image.get_width()/2-self.base[1].image.get_width()/2
                    #self.ficha.eixosLeft,self.ficha.eixosRight = self.balance.setCenter()
                    pass
                
                if self.base[1].rect.x >self.vas.vas.rect.x+ 578:
                    self.base[1].rect.x = self.vas.vas.rect.x + 43*(self.vas.vas.image.get_width()/53)
                    #self.ficha.eixosLeft,self.ficha.eixosRight = self.balance.setRight()
                    pass
                
                self.base[1].rect.y = self.vas.vas.image.get_height()/2+self.vas.vas.rect.y-self.base[1].image.get_height()/2                
                pass
    
    
    
    

class Fase6(GameState):

    def __init__(self):



        self.backGround = Object("src/Fases/Questions/fundo6.png")
        self.quest = Questions("Fase6","Fase8","Fase4",self.backGround)
        self.NextCurrentState = "Fase7"
        self.updateState = False
        self.effect =0
        pass

    def draw(self,tela):
        self.quest.draw(tela)
        pass

    def event(self,event):

        self.quest.event(event)

        pass

    def update(self,dt):
        self.NextCurrentState = self.quest.NextCurrentState
        self.updateState = self.quest.updateState
        self.effect = self.quest.effect
        pass

    pass




class Fase8(GameState):


    def out (self):
        self.updateState = True
        self.NextCurrentState = "Quit"

    def back (self):
        self.updateState = True
        self.NextCurrentState = self.StateTemp[2]
        self.effect =1

    def next(self):
        self.updateState = True
        self.effect = 0
        pass

    def help (self):
        print "Help"
        pass

    def __init__(self):

        #Carregando o vetor da fase pelo construtor

        self.backGround = Object("src/Fases/Fase8/fundo.png")


        self.StateTemp = ["Fase8","Fase10","Fase6"]
        self.NextCurrentState = self.StateTemp[0]
        self.updateState = False
        self.effect = 0

        self.MainObjects = [ObjectEvent((925,100), "src/Fases/Botoes/btnSetaDireita.png",
                                    "src/Fases/Botoes/btnSetaDireita_move.png",
                                    "src/Fases/Botoes/btnSetaDireita_click.png",self.next),
                            ObjectEvent((15,100), "src/Fases/Botoes/btnSetaEsquerda.png",
                                    "src/Fases/Botoes/btnSetaEsquerda_move.png",
                                    "src/Fases/Botoes/btnSetaEsquerda_click.png",self.back),
                            ObjectEvent((870,15),"src/Fases/Botoes/btnAjuda.png",
                                    "src/Fases/Botoes/btnAjuda_move.png",
                                    "src/Fases/Botoes/btnAjuda_click.png",self.help),
                            ObjectEvent((955,15),"src/Fases/Botoes/btnSair.png",
                                    "src/Fases/Botoes/btnSair_move.png",
                                    "src/Fases/Botoes/btnSair_click.png",self.out)]


        #========Vassoura
        self.vas = Vassoura("Fase8")

        self.balance = Balance(True)

        self.ficha = Fichas("Fase8", self.vas)
        self.ficha.eixosLeft,self.ficha.eixosRight = self.balance.setRight(self.ficha.eixosLeft,self.ficha.eixosRight)

        self.base = ObjectEvent((self.vas.vas.rect.x + 43*(self.vas.vas.image.get_width()/53)
                                 ,self.vas.vas.image.get_height()/2+self.vas.vas.rect.y-15)
                                ,"src/Fases/Vassoura/prego.png",None,None)

        pass


    def draw(self,tela):

        #Pintando o vetor da fase
        self.backGround.draw(tela)
        DrawVector(self.MainObjects,tela)


        #==========================VASSOURA===============================

        self.vas.draw(tela)

        self.balance.draw(tela, self.ficha.eixosLeft, self.ficha.eixosRight)
        
        self.ficha.draw(tela)
        
        pass

    def event (self,event):

        self.ficha.event(event)

        if event.type == pygame.MOUSEMOTION:
            for q in self.MainObjects:
                q.update(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONDOWN:

            for q in self.MainObjects:
                q.clickStart(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONUP:
            for q in self.MainObjects:
                if q.clickEnd(pygame.mouse.get_pos()):
                    return
                pass
            pass


    def update(self,dt):

        self.ficha.update(dt)
        self.vas.update(self.ficha.speed,self.ficha.resultWeigth,dt)

        pass


class Fase10(GameState):

    def __init__(self):


        self.backGround = Object("src/Fases/Questions/fundo10.png")
        self.quest = Questions("Fase10","Final","Fase8",self.backGround)
        self.updateState = False
        self.NextCurrentState = "Final"
        self.effect =0

        pass

    def draw(self,tela):
        self.quest.draw(tela)
        pass

    def event(self,event):

        self.quest.event(event)

        pass

    def update(self,dt):
        self.NextCurrentState = self.quest.NextCurrentState
        self.updateState = self.quest.updateState
        self.effect = self.quest.effect
        pass

    pass


class Final:

    def __init__(self):

        self.backGround = Object("src/Fases/Final/fundo.png")

        self.NextCurrentState = "Quit"
        self.updateState = False
        self.effect =0

        pass

    def draw(self,tela):
        self.backGround.draw(tela)
        pass

    def event(self,event):
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.updateState = True

        pass

    def update(self,dt):
        pass

    pass


class Questions:

    def next(self):
        self.updateState = True
        self.NextCurrentState = self.StateTemp[1]
        self.effect =0
        pass

    def back (self):
        self.updateState = True
        self.NextCurrentState = self.StateTemp[2]
        self.effect =1
        pass

    def __init__(self,faseCurrent,faseNext,faseBack,backGround):

        #Carregando o vetor da fase pelo construtor
        self.backGround = backGround

        self.MainObjects = [ObjectEvent((925,535), "src/Fases/Botoes/btnSetaDireita.png",
                                    "src/Fases/Botoes/btnSetaDireita_move.png",
                                    "src/Fases/Botoes/btnSetaDireita_click.png",self.next),
                            ObjectEvent((15,535),"src/Fases/Botoes/btnSetaEsquerda.png",
                                    "src/Fases/Botoes/btnSetaEsquerda_move.png",
                                    "src/Fases/Botoes/btnSetaEsquerda_click.png",self.back)]

        self.StateTemp = [faseCurrent,faseNext,faseBack]
        self.NextCurrentState = self.StateTemp[0]
        self.updateState = False
        self.effect =0
        pass



    def draw(self,tela):

        self.backGround.draw(tela)
        DrawVector(self.MainObjects,tela)

        pass

    def event(self,event):

        if event.type == pygame.MOUSEMOTION:
            for q in self.MainObjects:
                q.update(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONDOWN:
            for q in self.MainObjects:
                q.clickStart(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONUP:
            for q in self.MainObjects:
                q.clickEnd(pygame.mouse.get_pos())




