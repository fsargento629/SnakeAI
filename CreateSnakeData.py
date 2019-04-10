import pygame
import  sys, random, copy
import pandas as pd
import math

##### Functions #####

def Play_Game(show_game,max_score,max_time,columns):

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
        # save the previous distance
        previous_distance = dist(snake,food)

        if pygame.time.get_ticks()-timer > delay(snake) and show_game == True:
            timer = pygame.time.get_ticks()
        change = next_move(snake,food)

        # Convert change to sug_change
        sug_change = change[0]*-1 + change[2]*1
        
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
        new_data_list.append(get_output(snake,food,eat,lost,previous_distance))
        data.loc[len(data)] = new_data_list
        #print(new_data_list)
        
        if show_game == True:
            #Screen drawings
            screen.fill(BG)
            for i in snake.body:
                pygame.draw.rect(screen, BODY_C, (i[0], i[1], sqr_size, sqr_size), 0)
                pygame.draw.rect(screen, FOOD_C, (food.pos[0], food.pos[1], sqr_size, sqr_size), 0)
                pygame.display.set_caption("Snake. Your score is: {}".format(snake.score()))
                pygame.display.update()
                clock.tick(60)
    #print(data.head(10))
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
    # left walls
    if (snake.pos[0]==sqr_size):
        if snake.mov[0][1]>0:
            return [1,0,0]
        if snake.mov[0][1]<0:
            return [0,0,1]
        if snake.mov[0][1]<0:
            return [0,1,0]
        return [0,0,0]
    
    # right walls
    if (snake.pos[0]==width-sqr_size):
        if snake.mov[0][1]>0:
            return [0,0,1]
        if snake.mov[0][1]<0:
            return [1,0,0]
        if snake.mov[0][0]>0:
            return [0,1,0]
        return [0,0,0]
    
    # down walls
    if (snake.pos[1]==sqr_size):
        if snake.mov[0][1]<0:
            return [0,1,0]
        if snake.mov[0][0]<0:
            return [1,0,0]
        if snake.mov[0][0]>0:
            return [0,0,1]
        return [0,0,0]

    # upper wals
    if (snake.pos[1]==height-sqr_size):
        if snake.mov[0][1]>0:
            return [0,1,0]
        if snake.mov[0][0]>0:
            return [1,0,0]
        if snake.mov[0][0]<0:
            return [0,0,1]
        return [0,0,0]
    return [0,0,0]


def snake_food_angle(snake,food):
    # Vector from snake to food
    SF = [food.pos[0]-snake.pos[0],food.pos[1]-snake.pos[1]]
    #print(snake.mov)
    angle = math.acos( (SF[0] * snake.mov[0][0] + SF[1] * snake.mov[0][1] )/dist(snake,food) )
    if SF[1]<0:
        angle = -angle 
    angle = angle/math.pi
    return angle

def get_output(snake,food,eat,lost,previous_distance):
    if eat == 1:
        return 1
    if lost == 1:
        return -1
    if previous_distance>dist(snake,food):
        return 0
    else:
        return 1
    
    return 0



####################### MAIN #######################

# Game constants
width = 800
height = 600
BG = 60,60,60
FOOD_C = 200,0,0
BODY_C =255,255,255
sqr_size = 20
SPEED = sqr_size


# constant variables

inputs = ["left","front","right","food_angle","sug_direction"]
output =["move_rating"] #-1-> snake didnt survive;0->survived but the direction is wrong;1-> survived and the direction is right
columns = inputs + output
game_data = pd.read_csv("game_data.csv")
#game_data = pd.DataFrame(columns=columns)




# Cycle to play n games
## Cycle parameters
n = 200
show_game = True
max_score = 30
max_time = 2 #min
# cycle for each gamer snake
for gamer in range(0,n):
    # Initialize game
    print("Gamer "+str(gamer))
    new_data = Play_Game(True,5,2,columns)
    
    game_data = game_data.append(new_data)
    print("Gamer "+str(gamer)+" has lost =(")
    print(game_data.head(10))
    game_data.to_csv (r'game_data.csv', index = None, header=True) 

    print("Saved it!")




