import pygame
import  sys, random, copy
import pandas as pd
import math

####################### Classes and functions imported from the other file #######################

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

def next_move_random (snake,food): 
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

