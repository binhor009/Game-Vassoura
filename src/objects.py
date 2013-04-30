

from lib import Object,ObjectEixo,BaseMain,ObjectEvent,Animation,GameState,Text,Position
import pygame
from random import Random
from math import sin,tan,radians





class DrawVector:
    def __init__(self,lista,tela):
        for i in range(len(lista)):
            lista[i].draw(tela)
            pass
        pass
    pass


class Balance:
    
    def setCenter(self,eixoL,eixoR):
        
        eixoTotal = eixoLFinal=eixoRFinal= []
        
        for i in eixoL:
            eixoTotal.append(i)            
        for i in eixoR:
            eixoTotal.append(i)
        
        for i in range(1,len(eixoTotal)):
            if i < 27:
                eixoLFinal.append(eixoTotal[i])
            if i > 27:
                eixoRFinal.append(eixoTotal[i])    
                       
        
        self.change = False 
        return eixoL,eixoR
    
    def setRight(self,eixoL,eixoR):
        
        eixoTotal = eixoLFinal=eixoRFinal= []
        
        for i in eixoL:
            eixoTotal.append(i)            
        for i in eixoR:
            eixoTotal.append(i)
        
        for i in range(1,len(eixoTotal)):
            if i < 44:
                eixoLFinal.append(eixoTotal[i])
            if i > 44:
                eixoRFinal.append(eixoTotal[i])    
        
        self.change = False 
        return eixoLFinal,eixoRFinal
    
    def setLeft(self,eixoL,eixoR):
        
        eixoTotal = eixoLFinal=eixoRFinal= []
        
        for i in eixoL:
            eixoTotal.append(i)            
        for i in eixoR:
            eixoTotal.append(i)
        
        for i in range(1,len(eixoTotal)):
            if i < 9:
                eixoLFinal.append(eixoTotal[i])
            if i > 9:
                eixoRFinal.append(eixoTotal[i]) 
        
        
        self.change = False 
        return eixoL,eixoR
    
    def __init__(self,Draweixos = False):
        
        self.Draweixos = Draweixos
        pass
    
    def draw(self,tela,eixoL,eixoR):
        
        if self.Draweixos:
            DrawVector(eixoL, tela)
            DrawVector(eixoR, tela)
        
        pass


class Vassoura:

    def __init__(self,faseCur):

        self.faseCur = faseCur

        self.angle = 0
        self.rotationMode = False

        self.posVassoura = [22,328]

        self.rand = Random()

        if faseCur == "Fase4":
            self.posVassoura = [50,520]

        self.rotationMode = True

        self.vas = ObjectEvent((self.posVassoura[0],self.posVassoura[1]),"src/Fases/Vassoura/0.png")

    def draw(self,tela):

        self.vas.draw(tela)

        pass

    def event (self,event):

        if event.type == pygame.MOUSEMOTION:
            self.vas.update(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.vas.clickStart(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONUP:
            if self.vas.clickEnd(pygame.mouse.get_pos()):
                return
            pass
        pass


        pass

    def update(self,speed,weight,dt):

        self.rotationMode = False

        if self.faseCur == "Fase1":
            x= speed
            if weight == 0:
                if self.angle > 0:
                    self.angle +=-1*x
                    if self.angle == 1 or self.angle == 0 or self.angle == 2 or self.angle == 3:
                        self.angle = 0
                    if self.angle > 22:
                         self.angle=0
                if self.angle < 0:
                    self.angle +=-1*x
                    if self.angle == -1 or self.angle == 0 or self.angle == -2 or self.angle == -3:
                        self.angle = 0
                    if self.angle < -22:
                         self.angle=0



            self.angle += -1*speed
            if self.angle > 21:
                if weight != 0:
                   self.angle = 21
            if self.angle < -21:
                if weight != 0:
                    self.angle = -21
            self.rotationMode = True

        #print self.angle,speed,weight

        if self.rotationMode:
            self.vas.rotate(self.angle)
            pass


class Fichas:

    def reset(self):

        for i in self.objectFichas:
            i.rect.x, i.rect.y = i.oldPos
        pass


    def reverse(self,vector,pos):

        self.posFinal = len(vector)+1
        for i in range(self.posFinal):

            if i == pos:
                return self.posFinal

            self.posFinal-=1


    def setWeigth (self,vector,positionVector,peso,reverse = False):

        self.pos = positionVector
        self.pos+=1

        if vector[positionVector] == 0:
            if reverse :
                self.pos = self.reverse(vector, self.pos)
            vector[positionVector] += peso*self.pos

        return vector

    def numberWeigth(self,weigth,number):

        if number > 0:
            if weigth >= 0 :
               x = 1*number

            if weigth >= 62:
               x = 2*number

            if weigth >= 122:
               x = 3*number
        if number < 0:
            if weigth < 0:
               x =  1*number

            if weigth <= -62 :
                x =  2*number

            if weigth <= -122:
                x = 3*number
        return x

        pass

    def takePosEixos(self,weigth,speed = 0):


        for i in range(len(self.eixosLeft)):
            #print self.eixosRight[len(self.eixosLeft)-1].rect.y

            if weigth == 0 :

                if self.eixosRight[len(self.eixosLeft)-1].rect.y > self.initPositionEixoY:
                    speed = -1
                if self.eixosRight[len(self.eixosLeft)-1].rect.y < self.initPositionEixoY:
                    speed = 1

            pass

            if weigth > 0 :

                if self.eixosRight[len(self.eixosLeft)-1].rect.y >= 233:
                    speed = self.numberWeigth(weigth, 1)
                if self.eixosRight[len(self.eixosLeft)-1].rect.y >= 240:
                    speed = self.numberWeigth(weigth, 1)
                if self.eixosRight[len(self.eixosLeft)-1].rect.y >= 540 :
                    speed = 0
                if self.eixosRight[len(self.eixosLeft)-1].rect.y >= 533 :
                    speed = 0
            pass


            if weigth < 0 :

                if self.eixosRight[len(self.eixosLeft)-1].rect.y <= 533:
                    speed = self.numberWeigth(weigth, -1)
                if self.eixosRight[len(self.eixosLeft)-1].rect.y <= 540:
                    speed = self.numberWeigth(weigth, -1)

                if self.eixosRight[len(self.eixosLeft)-1].rect.y <= 240:
                    speed = 0
                if self.eixosRight[len(self.eixosLeft)-1].rect.y <= 233:
                    speed = 0
            pass


            if speed == -1:
                speedL = 1
                speedR = -1

            if speed == -2:
                speedL = 2
                speedR = -2
            if speed == -3:
                speedL = 3
                speedR = -3


            if speed == 1 :
                speedL = -1
                speedR = 1
            if speed == 2 :
                speedL = -2
                speedR = 2
            if speed == 3 :
                speedL = -3
                speedR = 3


            if speed == 0:
                speedR = speedL = 0


            self.eixosRight[i].rect.y += speedR
            self.eixosLeft[i].rect.y += speedL
            #self.eixosRight[i].rect.y = int((self.eixosRight[i].rect.x-self.vas.vas.rect.width/2 )*tan(self.vas.angle))*speed
            #self.eixosLeft[i].rect.y = int((self.vas.vas.rect.width/2-self.eixosLeft[i].rect.x )*tan(self.vas.angle))*speed


            if  speed == 5146123412123123123123150:
                try:
                    self.eixosRight[i].rect.y =  -1*int((self.vas.vas.rect.x+self.vas.vas.rect.width/2+self.eixosRight[i].rect.x)*tan(radians(self.vas.angle)))+ self.initPositionEixoY
                    self.eixosLeft[i].rect.y = -1*int((self.eixosLeft[i].rect.x -self.vas.vas.rect.x+self.vas.vas.rect.width/2)*tan(radians(self.vas.angle)))+ self.initPositionEixoY
                except:
                    print "erro"
                    pass

            #print weigth,i,int((self.vas.vas.rect.x+self.vas.vas.rect.width/2+self.eixosRight[i].rect.x)*tan(radians(self.vas.angle)))
            self.speed = speed

            speed = 0
            #pygame.time.wait(60)
            pass

        pass


    def allignEixo(self):

        for i in range(1,len(self.eixosLeft)-1):

            if not self.resultWeigth ==0:
                self.eixosRight[i].rect.y /= i
                self.eixosLeft[i].rect.y /= i

        pass


    def collideFichas (self,i,eixoVector):

        for b in self.objectFichas:

            if not i == b:
                if i.rect.colliderect(b):
                    i.rect.y += self.speed
                    pass

                    #if not b.rect.x == eixoVector.rect.x or b.rect.y == eixoVector.rect.y:
                    #i.rect.x,i.rect.y = eixoVector.rect.x,eixoVector.rect.y
                    #i.rect.y,i.rect.x = b.rect.y + b.rect.height -3,b.rect.x
                    #else :
                    #return b.peso
                return 0



    def __init__(self,faseCur = '',vas = None,objects = None):

        self.objectMain = objects

        self.vas = vas

        self.faseCur = faseCur

        self.rand = Random()

        self.speed = 0

        self.peso3 = 0

        for i in range (1,27):
            self.peso3 += ((26)*3)

        self.difWeigth = self.peso3-1

        self.objectFichas = []

        self.eixosLeft = []
        self.eixosRight = []

        self.initPositionObjectsX = 204
        self.initPositionObjectsY = 19

        self.eixo = pygame.image.load("src/Fases/Fichas/eixo.png").convert_alpha()

        self.initPositionEixoLeftX = 92
        self.initPositionEixoY = 380
        self.initPositionEixoRigthX = self.initPositionEixoLeftX + (27 * 16)


        self.weigthLeft = []
        self.weigthRigth = []

        self.i = 1

        for i in range(1,27):
            self.objectFichas.append(ObjectEvent([self.initPositionObjectsX,self.initPositionObjectsY],
                                                 "src/Fases/Fichas/idle "+str(i)+".png" ,
                                                  "src/Fases/Fichas/hover "+str(i)+".png",
                                                  "src/Fases/Fichas/idle "+str(i)+".png",None,self.i,"Animais"))
            if i > 13:
                self.i = 3

            self.initPositionObjectsX += 5 + self.objectFichas[0].rect.width

            #====EIXOS
            
            self.eixosLeft.append(ObjectEixo(self.eixo, self.initPositionEixoLeftX,self.initPositionEixoY))
                
            self.eixosRight.append(ObjectEixo(self.eixo, self.initPositionEixoRigthX,self.initPositionEixoY))    

            #self.initPositionEixoLeftX += i*(1 + self.eixosLeft[0].rect.width)
            #self.initPositionEixoRigthX += i*(1 + self.eixosLeft[0].rect.width)
            self.initPositionEixoLeftX += 16
            self.initPositionEixoRigthX +=16
            
            self.weigthLeft.append(i)
            self.weigthRigth.append(i)
            pass
        

        if faseCur == "Fase4":
            if objects is not None:
                for i in self.objectFichas:
                    i.rect.x,i.rect.y = self.rand.randrange(175,800),self.rand.randrange(0,580)
                    for o in objects:
                        loop = True
                        while loop:
                            if i.rect.colliderect(o):
                                i.rect.x,i.rect.y = self.rand.randrange(175,800),self.rand.randrange(0,580)
                            else:
                                loop = False
                                pass
                            pass
                    for o in self.objectFichas:
                        if not i == o:
                            loop = True
                            while loop:
                                if i.rect.colliderect(o):
                                    i.rect.x,i.rect.y = self.rand.randrange(175,800),self.rand.randrange(0,580)
                                else:
                                    loop = False
                                    pass
                                pass



        self.fichaCur = None
        self.rigth = self.left = self.resultWeigth = 0
        pass


    def draw(self,tela):
            
        DrawVector(self.objectFichas, tela)
        if not self.fichaCur is None:
            self.fichaCur.draw(tela)



    def event (self,event):

        if event.type == pygame.MOUSEMOTION:
            for q in self.objectFichas:
                q.update(pygame.mouse.get_pos())
                if q.hovering:
                    self.fichaCur = q

        if event.type == pygame.MOUSEBUTTONDOWN:
            for q in self.objectFichas:
                q.clickStart(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONUP:
            for q in self.objectFichas:
                if q.clickEnd(pygame.mouse.get_pos()):
                    return


    def update(self,dt,vas = None):

        for i in self.objectFichas:

            if i.state == "Clicking":
                x,y = pygame.mouse.get_pos()
                i.rect.x , i.rect.y = x - i.rect.width/2, y - i.rect.height/2


            if i.state == "Idle":
                btn = False

                if self.faseCur == "Fase1":

                    for a in range(len(self.eixosRight)):
                        if i.rect.colliderect(self.eixosRight[a]):
                            btn = True
                            i.rect.x ,i.rect.y = self.eixosRight[a].rect.x , self.eixosRight[a].rect.y
                            self.collideFichas(i,self.eixosRight[a])
                            self.weigthRigth = self.setWeigth(self.weigthRigth,a, i.peso)
                            #self.collideFichas(i)
                            break


                        if i.rect.colliderect(self.eixosLeft[a]):
                            btn = True
                            i.rect.x , i.rect.y = self.eixosLeft[a].rect.x , self.eixosLeft[a].rect.y
                            self.collideFichas(i,self.eixosLeft[a])
                            self.weigthLeft = self.setWeigth(self.weigthLeft,a, i.peso,True)
                            #self.collideFichas(i)
                            break

                        pass

                if self.faseCur == "Fase4" and vas is not None:

                    for ob in self.objectMain:
                        if i.rect.colliderect(vas) or i.rect.colliderect(ob):
                            speed = 0
                            if i.rect.y <= vas.rect.y+i.click.get_height()/2 :
                                speed = -1
    
                            if i.rect.y >= vas.rect.y:
                                speed = 1
    
                            if i.rect.y >= 580 or i.rect.y <= 0:
                                speed = -1
    
                                if i.rect.y <= 0:
                                    speed = 1
    
                                loop = True
                                while loop:
                                    if i.rect.colliderect(vas) or i.rect.colliderect(ob):
                                        if i.rect.x <= 500:
                                            i.rect.x+= 1
                                        if i.rect.x > 500:
                                            i.rect.x+= -1                                               
                                        
                                        i.rect.y+= speed
                                    else:
                                        loop = False
                                pass
    
                            i.rect.y+= speed
                        pass


                if not btn:

                    if self.faseCur == "Fase1":
                        if i.rect.x > 850 or i.rect.x < 175 or i.rect.y > 160:
                            i.rect.x , i.rect.y = i.oldPos
                            pass

                for o in self.objectFichas:
                    if not i == o:

                        if i.rect.colliderect(o):
                            speed = 0
                            if i.rect.x <= o.rect.x+o.click.get_width()/2 :
                                speed = -1
                                pass
                            if i.rect.x >= o.rect.x:
                                speed = 1
                                pass

                            if i.rect.x >= 850 or i.rect.x <= 175:
                                break

                            i.rect.x+= speed

            pass


        self.rigth = self.left = self.resultWeigth = 0

        for i in range(len(self.weigthLeft)):

            self.left += self.weigthLeft[i]
            self.rigth += self.weigthRigth[i]
            self.resultWeigth = self.rigth-self.left

        #print "LEFT "+str(self.left)+ "  RIGHT "+str(self.rigth)+ "  RESULT  " +str(self.resultWeigth)

        for i in range(len(self.weigthLeft)):

            self.weigthLeft[i] = 0
            self.weigthRigth[i] = 0
            pass


        #=================================================
        #=================================================
        #self.allignEixo()

        return self.takePosEixos(self.resultWeigth)

    pass

