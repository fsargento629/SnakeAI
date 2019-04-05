import pygame
import  sys, random, copy

# variables do control the game
lost = False
eat = False

timer = 0
width = 800
height = 600
BG = 60,60,60
FOOD_C = 200,0,0
BODY_C =255,255,255
sqr_size = 20
SPEED = sqr_size

# Classes
class Snake(object):
    def __init__(self):
        self.pos = [random.randint(1,(width-sqr_size)/sqr_size * sqr_size),
                    random.randint(1,(height-sqr_size)/sqr_size) * sqr_size]
        self.mov = [(0,1)] #up
        self.body = [self.pos[:]]

    def score(self):
        return len(self.body)
    

    def move(self,change): #Should update snake position and body based on position and change
        # change = (LEFT,STRAIGHT,RIGHT)
        directions = [(1,0),(0,1),(-1,0),(0,-1)]

        

        if change[0]==1: #LEFT
            self.mov =  [directions[-4+i+1] for i in range(0,len(directions)) if directions[i]== self.mov[0] ]
            

        elif change[2]==1: # RIGHT
            self.mov = [directions[i-1] for i in range(0,len(directions)) if directions[i]== self.mov[0] ]
            
        elif change[1]==1:
            self.mov = self.mov

        
        #print(self.mov[1])
        self.pos[0] = self.pos[0] + SPEED * self.mov[0][0]
        self.pos[1] = self.pos[1] + SPEED * self.mov[0][1]
        self.body.insert(0, self.pos[:])

        

class Food(object):
    def __init__(self):
        self.pos = [random.randint(1,(width-sqr_size)/sqr_size * sqr_size),
                random.randint(1,(height-sqr_size)/sqr_size) * sqr_size]

# Functions

def dist(a,b):
    return ( (b.pos[0] - a.pos[0])**2 + (b.pos[1] - a.pos[1])**2 )

def loser(snake,food): # check if game has been lost
    if snake.pos[0]<sqr_size or snake.pos[0]>width-sqr_size or snake.pos[1]<sqr_size or snake.pos[1]>height-sqr_size:
        return True
    for i in snake.body[1:]:
        if i == snake.pos:
            return True
    return False

def delay(snake): # I dont know man
    if 125-snake.score()>35:
        return 125-snake.score()
    else:
        return 35

def next_move (snake,food): 
    # just randomize the next move 
    #next move should either be to 
    # turn right, left or keep straight

    random_num = random.randint(0,2)
    
    if random_num == 0:
        change = (1,0,0)
    elif random_num == 1:
        change= (0,1,0)
    else:
        change = (0,0,1)
    
    return change




# Game setup
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width,height))
snake_1 = Snake()
food = Food()
screen.fill(BG) #black screen

# Game Loop
while True:
    #Event loop not needed 
    if lost==True:
        pygame.quit() 

        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((width,height))
        snake_1 = Snake()
        food = Food()
        screen.fill(BG) #black screen


    if pygame.time.get_ticks()-timer > delay(snake_1):
        timer = pygame.time.get_ticks()
        change = next_move(snake_1,food)
        snake_1.move(change)
        
        eat = dist(snake_1,food) < sqr_size**2

        if eat:
            food = Food()
        else:#removes last piece of snake
            snake_1.body.pop()

        lost = loser(snake_1,food)

        #Screen drawings
        screen.fill(BG)
        for i in snake_1.body:
            pygame.draw.rect(screen, BODY_C, (i[0], i[1], sqr_size, sqr_size), 0)
        pygame.draw.rect(screen, FOOD_C, (food.pos[0], food.pos[1], sqr_size, sqr_size), 0)
        pygame.display.set_caption("Snake. Your score is: {}".format(snake_1.score()))
        pygame.display.update()
        clock.tick(60)






    