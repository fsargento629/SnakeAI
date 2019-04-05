import pygame
import  sys, random, copy
import pandas as pd

# Game constants
width = 800
height = 600
BG = 60,60,60
FOOD_C = 200,0,0
BODY_C =255,255,255
sqr_size = 20
SPEED = sqr_size


# constant variables
save_file = "Snake_data.csv"
inputs = ["left","front","right","food_angle","sug_direction"]
output =["move_rating"] #-1-> snake didnt survive;0->survived but the direction is wrong;1-> survived and the direction is right
columns = inputs + output


# Cycle to play n games
## Cycle parameters
n = 5
show_game = True
max_score = 30
max_time = 2 #min
# cycle for each gamer snake
for gamer in range(0,n):
    # Initialize game
    game_data = game_data.append(Play_Game())




##### Functions #####

def Play_Game(show_game,max_score,max_time):

    # Game Constants
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



    data = pd.DataFrame(columns=columns)

    if show_game == True:
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((width,height))
        screen.fill(BG) #black screen
    
    snake = Snake()
    food = Food()

    # begin game cycle

    while not lost:

        if pygame.time.get_ticks()-timer > delay(snake) and show_game == True:
            timer = pygame.time.get_ticks()
        change,sug_change = next_move(snake,food)
        
        # Create input list
        new_data_list = obstacles(snake,width,height)
        new_data_list.append(snake_food_angle(snake,food))
        new_data_list.append(sug_change)

        snake.move(change)
        eat = dist(snake,food) < sqr_size**2

        if eat:
            food = Food()
        else:#removes last piece of snake
            snake.body.pop()

        lost = loser(snake,food)

        # create output value for the dataframe
        new_data_list.append(output(snake,food,eat,lost))

        if show_game == True:
            #Screen drawings
            screen.fill(BG)
            for i in snake.body:
                pygame.draw.rect(screen, BODY_C, (i[0], i[1], sqr_size, sqr_size), 0)
                pygame.draw.rect(screen, FOOD_C, (food.pos[0], food.pos[1], sqr_size, sqr_size), 0)
                pygame.display.set_caption("Snake. Your score is: {}".format(snake.score()))
                pygame.display.update()
                clock.tick(60)

    return data





####################### Classes and functions imported from the other file #######################


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

####### Functions to play snake #######

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


def obstacles(snake,width,height):
    return [left,front,right]

def snake_food_angle(snake,food):
    return angle

def output(snake,food,eat,lost):
    return output_value