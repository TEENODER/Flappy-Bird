from turtle import width
import pygame
import time
import sys
import random
pygame.init()


class Game():
    def __init__(self,width,height,caption,icon) -> None:

        self.score = 0
        self.gamewindow = pygame.display.set_mode((width,height))
        self.width = width
        self.height = height
        self.birdarray = [Game.loadimage(f"gallery/flappy bird/f{i}.png") for i in range(1,8)]
        self.birdindex = 0
        self.digits = {i:Game.loadimage(f"gallery/sprites/{i}.png") for i in range(10)}
        self.background  = Game.loadimage('gallery/sprites/background.png')
        self.base  = Game.loadimage('gallery/sprites/base.png')
        self.base2  = Game.loadimage('gallery/sprites/base.png')
        self.bird  = self.birdarray[self.birdindex]
        self.msg  = Game.loadimage('gallery/sprites/message.png')
        self.pipe  = Game.loadimage('gallery/sprites/pipe.png')
        self.rpipe = pygame.transform.rotate(self.pipe,180)
        self.lowerPipes   =  []
        self.upperPipes   =  []
        self.exitgame  = False
        self.gameover = False
        self.gravity = 3
        self.birdy = int(self.width//2 - 0.04*self.width)
        self.birdx = 20
        pygame.display.set_caption(caption)
        pygame.display.set_icon(Game.loadimage(icon))
        self.FPS = 30
        self.Clock = pygame.time.Clock()
        self.presspower = 10*self.gravity
        self.gamecounter = 0

        #Base Data
        self.basex = 0
        self.basey = 0.8*self.height
        self.base2y = self.basey
        self.base2x = self.basex + self.width
        self.baseheight = 0.2*self.height
        self.baseindex = 1

        #PIPE - DATA
        self.minPipeDiff = 1
        self.maxPipeDiff = 50
        self.pipewidth = 0.2*self.width


        self.pipeXDifference = random.randint(self.minPipeDiff,self.maxPipeDiff)
        self.pipeheight = random.randint(int(0.2*self.height//1),int(0.36*self.height//1))
        self.lpipey = 0
        self.lowerPipes.append([self.width,self.lpipey,self.pipewidth,self.pipeheight])


        self.pipeXDifference = random.randint(self.minPipeDiff,self.maxPipeDiff)
        self.pipeheight = random.randint(int(0.2*self.height//1),int(0.39*self.height//1))
        self.upipey = self.basey -   self.pipeheight

        self.upperPipes.append([self.width+self.pipeXDifference+self.pipewidth,self.upipey,self.pipewidth,self.pipeheight])

        self.birdwidth = 0.06*self.width
        self.birdheight = 0.06*self.height


        



    @staticmethod
    def blitimage(parent,img,x,y,width,height):
        image = pygame.transform.scale(img,(width,height))
        return parent.blit(image,(x,y))

    def playsound(self,path):
        pygame.mixer.init()
        pygame.mixer.Sound(path).play()
        

    @staticmethod
    def loadimage(image):
        return pygame.image.load(image).convert_alpha()


    def quitgame(self):
        self.exitgame = True


    def gameloop(self,task=None,key=None,task2 = None):

        while not self.exitgame:

            for event in pygame.event.get():
                if (event.type==pygame.QUIT):
                    self.quitgame()
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        self.quitgame()
                    if key!=None:
                        if event.key==key:
                            task2()

                        
                    
            

            #Setting Background
            Game.blitimage(self.gamewindow,self.background,0,0,self.width,self.height)


            if(task!=None):
                task()
                
            pygame.display.update()
            self.Clock.tick(self.FPS)
        pygame.quit()
        sys.exit()


    def maingame(self):
        """Main Game Code"""
        def jump():
                """This Helps In Jumping Of Flappy Bird"""
                self.birdy -= self.presspower
                self.playsound('gallery/audio/wing.wav')

        def displayScore():
            width = 0.05*self.width
            height = 0.05*self.height
            xdiff = 0
            x  = self.width//2-width//2
            y = 0.01*self.height
            for chr in str(self.score):
                Game.blitimage(self.gamewindow,self.digits[int(chr)],x,y,width,height)
                x+=width+xdiff


        def gameover():
            self.playsound('gallery/audio/hit.wav')
            pygame.time.wait(2000)
            def main():
                self.score  = 0
                self.lowerPipes.clear()
                self.upperPipes.clear()
                self.birdy = int(self.width//2 - 0.04*self.width)
                self.birdx = 20
                self.lowerPipes.append([self.width,self.lpipey,self.pipewidth,self.pipeheight])
                self.upperPipes.append([self.width+self.pipeXDifference+self.pipewidth,self.upipey,self.pipewidth,self.pipeheight])
                self.maingame()
                
                

            self.gameloop(main)

        

        def main():
            self.pipeXDifference = random.randint(self.minPipeDiff,self.maxPipeDiff)
            self.pipeheight = random.randint(int(0.2*self.height//1),int(0.37*self.height//1))
            self.upipey = self.basey -   self.pipeheight


            #Adding Gravity
            self.gamecounter += 1
            self.birdy += self.gravity


            #Animation Related
            if(self.gamecounter%2==0):
                self.birdindex+=1
                self.basex -= 2
                self.base2x -= 2
                for i in range(len(self.lowerPipes)):
                    self.upperPipes[i][0]-=2
                    self.lowerPipes[i][0]-=2



            #Base

            Game.blitimage(self.gamewindow,self.base,self.basex,self.basey,self.width,self.baseheight)

            Game.blitimage(self.gamewindow,self.base2,self.base2x,self.base2y,self.width,self.baseheight)

            #Moving Base
            if(self.baseindex==1):
                if((self.basex+self.width)<self.width):
                    self.base2x = self.basex + self.width
                    self.baseindex = 2
            elif(self.baseindex==2):
                if((self.base2x+self.width)<self.width):
                    self.basex = self.base2x + self.width
                    self.baseindex = 1

            #Bird
            try:
                self.bird  = self.birdarray[self.birdindex]
            except IndexError:
                self.birdindex = 0


            Game.blitimage(self.gamewindow,self.bird,self.birdx,self.birdy,self.birdwidth,self.birdheight)


            #Pipe
            if(self.lowerPipes[-1][0]<self.width):
                self.lowerPipes.append([self.upperPipes[-1][0]+self.pipeXDifference+self.pipewidth,self.lpipey,self.pipewidth,self.pipeheight])

                self.pipeXDifference = random.randint(self.minPipeDiff,self.maxPipeDiff)
                self.pipeheight = random.randint(int(0.2*self.height//1),int(0.38*self.height//1))
                self.upipey = self.basey -   self.pipeheight

            

                
                
                self.upperPipes.append([self.lowerPipes[-1][0]+self.pipeXDifference+self.pipewidth,self.upipey,self.pipewidth,self.pipeheight])

            #Blitting Pipe
            for i in range(len(self.lowerPipes)):
                
                
                Game.blitimage(self.gamewindow,self.rpipe,self.lowerPipes[i][0],self.lowerPipes[i][1],self.lowerPipes[i][2],self.lowerPipes[i][3]) 

                

                Game.blitimage(self.gamewindow,self.pipe,self.upperPipes[i][0],self.upperPipes[i][1],self.upperPipes[i][2],self.upperPipes[i][3]) 

                #GameOver Logic
                gameOverConditions = [self.birdy+22<=(self.lowerPipes[i][1]+self.lowerPipes[i][3]) and self.birdx+self.birdwidth - 5>=self.lowerPipes[i][0],


                self.birdy+36>=self.upperPipes[i][1] and self.birdx+16>=self.upperPipes[i][0],


                self.birdy + 14<=0,


                self.birdy+self.birdheight >=self.basey,
                ]

                

                if(any(gameOverConditions)):
                    gameover()
                
                try:

                    if(self.birdx+self.birdwidth - 20>self.lowerPipes[i][0]+self.lowerPipes[i][2]+self.birdwidth):
                        self.playsound('gallery/audio/point.wav')
                        self.score += 1
                        self.lowerPipes.pop(0)
                        break

                    
                    elif(self.birdx+self.birdwidth - 20>self.upperPipes[i][0]+self.upperPipes[i][2]+self.birdwidth):
                        self.playsound('gallery/audio/point.wav')
                        self.score += 1
                        self.upperPipes.pop(0)
                        break

                except Exception:
                    pass

                
                    
                    

          #Base

            Game.blitimage(self.gamewindow,self.base,self.basex,self.basey,self.width,self.baseheight)

            Game.blitimage(self.gamewindow,self.base2,self.base2x,self.base2y,self.width,self.baseheight)
            displayScore()

 
        return self.gameloop(main,pygame.K_SPACE,jump)


    def intro(self):
        """This Shows The Intro Of Our Game"""
        def main():
            #Adding Base
            Game.blitimage(self.gamewindow,self.base,self.basex,self.basey,self.width,self.baseheight)
            Game.blitimage(self.gamewindow,self.msg,20,20,self.width-40,self.height-40)
            Game.blitimage(self.gamewindow,self.bird,self.birdx,self.birdy,self.birdwidth,self.birdheight)
        return self.gameloop(main,pygame.K_RETURN,self.maingame)
            
            

if __name__ == "__main__":
    flappybird =  Game(350,600,'Flappy Bird  -  By Parth','gallery\icon.ico')
    flappybird.intro()

    