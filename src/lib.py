import pygame, os
from pygame.locals import *
from random import Random


class BaseMain(object):

    def __init__(self):


        os.environ["SDL_VIDEO_CENTERED"] = "1"

        self.size = [1024,615]
        self.baseSurface = pygame.display.set_mode((self.size),pygame.NOFRAME)
        #self.baseSurface = pygame.display.set_mode((self.size),pygame.FULLSCREEN)
        self.tela = pygame.Surface((self.size), pygame.SRCALPHA, 32)


        self.telaCurrent = pygame.Surface((self.size), pygame.SRCALPHA, 32)
        self.telaNext = pygame.Surface((self.size), pygame.SRCALPHA, 32)

        self.time = pygame.time.Clock()
        pygame.display.set_caption("Jogo da Vassoura")


        #Set Fps=30
        self.fps = pygame.time.Clock()
        self.fpsTick = 30
        pass

    def deltaTime(self):
        
        self.dt = self.fps.tick(self.fpsTick)

        #Pegando o FPS e jogando na tela
        pygame.display.set_caption("Jogo da Vassoura - %d fps" % self.fps.get_fps())

        return self.dt/1000.0

    def draw(self,CurrentState):

        self.baseSurface.blit(self.tela,(0,0))

        CurrentState.draw(self.tela)

        pass


    def updateScreen(self):

        pygame.display.flip()

        pass

    pass


class GameState(object):

    def __init__(self):
        self.fps = 30
        pass

    def draw(self, tela):
        pass

    def update(self,dt):
        pass

    def event(self, event):
        pass


class ObjectEixo(object):

    def __init__(self,file,posx = 0, posy = 0):

        self.image = file
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = posx,posy
        pass

    def draw(self,tela):
        tela.blit(self.image, self.rect)
        pass


class Object(object):

    def __init__(self,file,posx = 0, posy = 0):

        self.initImage = self.image = pygame.image.load(file).convert_alpha()
        self.oldRect = self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = posx,posy
        pass

    def draw(self,tela):
        tela.blit(self.image, self.rect)
        pass

    def rotate(self,angle):
        
        self.imageRotate = self.initImage
        
        oldrectCenter = self.rect.center
        self.imageRotate =  pygame.transform.rotate(self.imageRotate,angle)
        
        self.rect = self.imageRotate.get_rect()
        self.rect.center = oldrectCenter
        
        self.image = self.imageRotate
        
    pass

class ObjectEvent(Object):

    def __init__(self, pos, idleImage, hoverImage=None, clickImage=None, function=None,peso=0,classObject='',centerIMG = False):
        self.centerIMG = centerIMG
        self.classObject=classObject
        self.oldPos = pos
        self.peso = peso
        self.oldIdle = self.idle = pygame.image.load(idleImage)
        if hoverImage is not None:
            self.hover = pygame.image.load(hoverImage)
            if centerIMG:
                self.hovereringIMG = self.hover
                self.hover = self.idle 
        else:
            self.hover = self.idle

        if clickImage is not None:
            self.click = pygame.image.load(clickImage)
        else:
            self.click = self.idle

        self.rect = self.idle.get_rect()
        self.rect.x, self.rect.y = pos

        self.state = "Idle"
        self.hovering = False

        self.initImage = self.image = self.idle
        self.onclick = function
        self.hasParameter = False

        if self.centerIMG:
            self.IMGPOS = Position((self.rect.x,self.rect.y),self.idle)
            self.newhovereringIMGPOS = self.IMGPOS.update()
    
    def rotate(self,angle):
        
        self.imageRotate = self.initImage
        
        oldrectCenter = self.rect.center
        self.imageRotate =  pygame.transform.rotate(self.imageRotate,angle)
        
        self.rect = self.imageRotate.get_rect()
        self.rect.center = oldrectCenter
        
        self.image = self.imageRotate
    
    def update(self, mousepos):

        if self.state == "Idle":
            if self.rect.collidepoint(mousepos):
                self.image = self.hover
                self.hovering = True

            else:
                self.image = self.idle
                self.hovering = False



        if self.state == "Clicking":
            if self.rect.collidepoint(mousepos):
                self.image = self.click
            else:
                self.image = self.idle
                pass
            pass


    def setParameter(self, param):
        self.hasParameter = True
        self.parameter = param

    def clickStart(self, mousepos):
        if self.rect.collidepoint(mousepos):
            self.state = "Clicking"
            self.image = self.click

    def clickEnd(self, mousepos):
        ret = False
        if self.state == "Clicking":
            if self.rect.collidepoint(mousepos):
                
                if self.centerIMG:
                    self.IMGPOS = Position((self.rect.x,self.rect.y),self.idle)
                    self.newhovereringIMGPOS = self.IMGPOS.update()
                    
                self.image = self.idle                
                if self.onclick is not None:
                    if self.hasParameter:
                        self.onclick(self.parameter)
                    else:
                        self.onclick()
                    ret = True
            self.state = "Idle"
            
        return ret

    pass


class Position:

    def __init__(self,posCurrent,idle):
        self.posCurrent = posCurrent
        self.horverPos = posCurrent[0]-idle.get_width()/2,posCurrent[1]-idle.get_height()/2
        pass

    def update(self):

        return self.horverPos




class Animation (BaseMain):

    def __init__(self, currentState, nextState,telaCurrent,telaNext,effect=0):

        self.rand = Random()

        self.currentState, self.nextState = currentState, nextState
        self.telaCurrent,self.telaNext = telaCurrent,telaNext

        #self.effects = [[self.windowsUP,0,1], [self.windowsDOWN,0,-1],
        #                [self.windowsLEFT,1,0],[self.windowsRIGHT,-1,0]]
        #self.effectWindows = self.effects [self.rand.randrange(0,len(self.effects))]

        self.effects = [[self.windowsLEFT,1,0], [self.windowsRIGHT,-1,0],[self.windowsUP,0,1], [self.windowsDOWN,0,-1]]
        self.effectWindows = self.effects [effect]

        self.posCurrent, self.posNext = [0,0],[self.currentState.backGround.rect.width*self.effectWindows[1],self.nextState.backGround.rect.height*self.effectWindows[2]]

        self.speed = 4
        pass


    def drawEffect (self,baseSurface,dt):

        self.currentState.draw(self.telaCurrent)
        self.nextState.draw(self.telaNext)

        while True:

            if self.effectWindows[0](dt):
                self.nextState.draw(self.telaCurrent)
                return False
            else:

                baseSurface.blit(self.telaCurrent,self.posCurrent)
                baseSurface.blit(self.telaNext,self.posNext)

                pygame.display.flip()
                pass


    def windowsUP(self,dt):

        if not (self.posNext[1] < 0):

            self.posCurrent[1] += -self.speed+int(self.speed*dt)
            self.posNext[1] += -self.speed+int(self.speed*dt)

            return False
        else:
            return True

        pass

    def windowsDOWN(self,dt):

        if not (self.posNext[1] > 0):

            self.posCurrent[1] += self.speed+int(self.speed*dt)
            self.posNext[1] += self.speed+int(self.speed*dt)

            return False
        else:
            return True


        pass

    def windowsLEFT(self,dt):

        if not (self.posNext[0] < 0):

            self.posCurrent[0] += -self.speed+int(self.speed*dt)
            self.posNext[0] += -self.speed+int(self.speed*dt)
            
            return False
        else:
            return True

        pass

    def windowsRIGHT(self,dt):

        if not (self.posNext[0] > 0):

            self.posCurrent[0] += self.speed+int(self.speed*dt)
            self.posNext[0] += self.speed+int(self.speed*dt)

            return False
        else:
            return True

        pass

    pass


class Text:

        def __init__(self,text="", posX=0 ,posY=0, size= 20,italic=True,
                     negrito=False,cor=[255,255,255], fundoCor=[154,58,165],
                     nameFont="Comic Sans MS"):

            self.pos = posX,posY
            self.fonte = pygame.font.SysFont(nameFont,size,negrito,italic)
            self.texto = self.fonte.render(text,0,cor,fundoCor)

            pass

        def draw(self, tela):
            tela.blit(self.texto,self.pos)
            pass
 


class Form(pygame.Rect,object):
    
    def __init__(self,pos,width,height=None,font=None,fontsize=None,bg=(200,200,200),fgcolor=(0,0,0),curscolor=(0,0,0),hlcolor=(0xa0,0,0),maxlines=0):
        if not font: self.FONT = pygame.font.Font(pygame.font.get_default_font(),fontsize)
        elif type(font) == str: self.FONT = pygame.font.Font(font,fontsize)
        else: self.FONT = font
        if not height: pygame.Rect.__init__(self,pos,(width,self.FONT.get_height()))
        else: pygame.Rect.__init__(self,pos,(width,height))
        
        self.BG = bg
        self.FGCOLOR = fgcolor
        self.CURSCOLOR = curscolor
        self.CURSOR = True
        self.HLCOLOR = hlcolor
        self.MAXLINES = maxlines
        self.TAB = 4
        
        self.OUTPUT = ''
        self.CURSORINDEX = 0
        self.SELECTSTART = 0
        self._x,self._y = pos
        self.SRC = pygame.display.get_surface()
    
    def clear_selection(self):
        if self.SELECTSTART != self.CURSORINDEX:
            select1,select2 = sorted((self.SELECTSTART,self.CURSORINDEX))
            self.OUTPUT = self.OUTPUT[:select1]+self.OUTPUT[select2:]
            self.CURSORINDEX = select1
            return True
        return False
        
    def show(self):
        h = self.FONT.get_height()
        x,y = self._x,self._y
        r = pygame.Rect(x,y,0,h)
        for e,i in enumerate(self.OUTPUT+'\n'):
            if e == self.CURSORINDEX+1: break
            if i not in '\n\t':
                r = pygame.Rect(x,y,*self.FONT.size(i))
                x = r.right
            elif i == '\n':
                r = pygame.Rect(x,y,1,h)
                x = self._x
                y = r.bottom
            else:
                t = self.FONT.size(self.TAB*' ')[0]
                t = ((((x-self._x) / t) + 1) * t ) - (x-self._x)
                r = pygame.Rect(x,y,t,h)
                x = r.right
        
        rclamp = r.clamp(self)
        self._x += rclamp.x - r.x
        self._y += rclamp.y - r.y
        
        clip = self.SRC.get_clip()
        self.SRC.set_clip(self.clip(clip))
        try: self.SRC.fill(self.BG,self)
        except: self.SRC.blit(self.BG,self)
        x = self._x
        y = self._y
        select1,select2 = sorted((self.SELECTSTART,self.CURSORINDEX))
        self.C = []
        for e,i in enumerate(self.OUTPUT):
            if i not in '\n\t':
                self.C.append(pygame.Rect(x,y,*self.FONT.size(i)))
                if select1 <= e < select2:
                    scr.blit(self.FONT.render(i,1,self.HLCOLOR),(x,y))
                else:
                    scr.blit(self.FONT.render(i,1,self.FGCOLOR),(x,y))
                x = self.C[-1].right
            elif i == '\n':
                self.C.append(pygame.Rect(x,y,0,h))
                x=self._x
                y = self.C[-1].bottom
            else:
                t = self.FONT.size(self.TAB*' ')[0]
                t = ((((x-self._x) / t) + 1) * t ) - (x-self._x)
                self.C.append(pygame.Rect(x,y,t,h))
                x = self.C[-1].right
        self.C.append(pygame.Rect(x,y,0,h))
        if self.CURSOR:
            p = self.C[self.CURSORINDEX]
            draw.line(scr,self.CURSCOLOR,p.topleft,(p.left,p.bottom),1)
        pygame.display.update(self)
        self.SRC.set_clip(clip)
            
    def place_cursor(self,pos):
            c = pygame.Rect(pos,(0,0)).collidelist(self.C)
            if c > -1: self.CURSORINDEX = c if pos[0] <= self.C[c].centerx else c + 1
            else:
                l = (pos[1] - self._y) / self.FONT.get_height()
                self.CURSORINDEX = sum([len(i) for i in self.OUTPUT.split('\n')][:l+1])+l
                if self.CURSORINDEX > len(self.OUTPUT): self.CURSORINDEX = len(self.OUTPUT)
                elif self.CURSORINDEX < 0: self.CURSORINDEX = 0
                
    def wakeup(self,ev):
        if ev.type == pygame.KEYDOWN:
            
            if ev.key == pygame.K_RIGHT:
                if self.SELECTSTART != self.CURSORINDEX: self.CURSORINDEX = max((self.SELECTSTART,self.CURSORINDEX))
                elif self.CURSORINDEX < len(self.OUTPUT): self.CURSORINDEX += 1
                
            elif ev.key == pygame.K_LEFT:
                if self.SELECTSTART != self.CURSORINDEX: self.CURSORINDEX = min((self.SELECTSTART,self.CURSORINDEX))
                elif self.CURSORINDEX > 0: self.CURSORINDEX -= 1
                
            elif ev.key == pygame.K_DELETE:
                if not self.clear_selection():
                    self.OUTPUT = self.OUTPUT[:self.CURSORINDEX]+self.OUTPUT[self.CURSORINDEX+1:]
            
            elif ev.key == pygame.K_END:
                try:
                    self.CURSORINDEX = self.OUTPUT[self.CURSORINDEX:].index('\n') + self.CURSORINDEX
                except:
                    self.CURSORINDEX = len(self.OUTPUT)
            
            elif ev.key == pygame.K_HOME:
                try:
                    self.CURSORINDEX = self.OUTPUT[:self.CURSORINDEX].rindex('\n') + 1
                except:
                    self.CURSORINDEX = 0
            
            elif ev.key == pygame.K_RETURN or ev.key == pygame.K_KP_ENTER:
                self.clear_selection()
                if not self.MAXLINES or self.OUTPUT.count('\n') < self.MAXLINES - 1:
                    self.OUTPUT = self.OUTPUT[:self.CURSORINDEX]+'\n'+self.OUTPUT[self.CURSORINDEX:]
                    self.CURSORINDEX += 1
            
            elif ev.key == pygame.K_BACKSPACE:
                if not self.clear_selection():
                    if self.CURSORINDEX > 0:
                        self.CURSORINDEX -= 1 
                        self.OUTPUT = self.OUTPUT[:self.CURSORINDEX]+self.OUTPUT[self.CURSORINDEX+1:]
            
            elif ev.key == pygame.K_UP:
                c = self.C[self.CURSORINDEX]
                self.place_cursor((c.left,c.top-self.FONT.get_height()))

            elif ev.key == pygame.K_DOWN:
                c = self.C[self.CURSORINDEX]
                self.place_cursor((c.left,c.top+self.FONT.get_height()))
                
            elif ev.unicode:
                self.clear_selection()
                self.OUTPUT = self.OUTPUT[:self.CURSORINDEX]+ev.unicode+self.OUTPUT[self.CURSORINDEX:]
                self.CURSORINDEX += 1
            if ev.key not in (K_NUMLOCK,K_CAPSLOCK,K_SCROLLOCK,K_RSHIFT,K_LSHIFT,K_RCTRL,K_LCTRL,K_RALT,K_LALT,K_RMETA,K_LMETA,K_LSUPER,K_RSUPER,K_MODE,K_HELP,K_PRINT,K_SYSREQ,K_BREAK,K_MENU,K_POWER):
                self.SELECTSTART = self.CURSORINDEX
            self.show()
        
        elif (ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1) or (ev.type == pygame.MOUSEMOTION and ev.buttons[0]):
            self.place_cursor(ev.pos)
            if ev.type == pygame.MOUSEBUTTONDOWN:
                self.SELECTSTART = self.CURSORINDEX
            self.show()
    
    
    