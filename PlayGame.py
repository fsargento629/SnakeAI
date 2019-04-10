import pygame
import  sys, random, copy
import pandas as pd
import math
from Snake import Snake,Food
from Snake import dist,loser,delay,next_move_random,obstacles,get_output,snake_food_angle
from AI import Neural_Network

width = 800
height = 600
BG = 60,60,60
FOOD_C = 200,0,0
BODY_C =255,255,255
sqr_size = 20
SPEED = sqr_size
 

def Play_Game(show_game,max_score,max_time,columns=["left","front","right","food_angle","sug_direction","move_rating"],user="random"):

    # Game Constants
    lost = False
    eat = False

    timer = 0
    



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

        if user == "random":   
            change = next_move_random(snake,food)
            # Convert change to sug_change
            sug_change = change[0]*-1 + change[2]*1
        
        elif user == "NN":
            sug_change = Neural_Network(obstacles(snake,width,height),snake_food_angle) #should return a sug change (-1,0 or 1)
            #change = function of sug_change

        
        
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

Play_Game(True,5,5)
