import pygame
import  sys, random, copy

#Initialising variables
lost = False
eat = False
key1 = [0, -1]
timer = 0
width = 800
height = 600
BG = 60, 60, 60
FOOD_C = 200, 0, 0
BODY_C = 255, 255, 255
sqr_size = 20
SPEED = sqr_size

#Define functions
def dist(a, b):
    return ((b.pos[0] - a.pos[0])**2 + (b.pos[1] - a.pos[1])**2)

def loser(snake, food): #Check if lost the game
    if snake.pos[0]<sqr_size or snake.pos[0]>width-sqr_size or snake.pos[1]<sqr_size or snake.pos[1]>height-sqr_size:
        return True
    for i in snake.body[1:]:
        if i == snake.pos:
            return True          

def delay(snake):
    if 125 - snake.score() > 35:
        return 125-snake.score()
    else:
        return 35

def whatkey(event, key):
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                return [-1, 0]
            if event.key == pygame.K_RIGHT:
                return [1, 0]
            if event.key == pygame.K_UP:
                return [0, -1]
            if event.key == pygame.K_DOWN:
                return [0, 1]
    return key
            
#Define classes
class Snake(object):
    def __init__(self):
        self.pos = [random.randint(1, (width-sqr_size)/sqr_size)*sqr_size,
                    random.randint(10, (height-sqr_size)/sqr_size)*sqr_size]
        self.mov = [0, -1]
        self.body = [self.pos[:]]

    def score(self):
        return len(self.body)

    def move(self, key): #Snake movement
        if key[0] + self.mov[0] != 0 and key[1] + self.mov[1] != 0:
            self.mov = key
        self.pos[0] += self.mov[0]*SPEED
        self.pos[1] += self.mov[1]*SPEED
        self.body.insert(0, self.pos[:])
       
class Food(object):
    def __init__(self):
        self.pos = [random.randint(1, (width-sqr_size)/sqr_size)*sqr_size,
                    random.randint(1, (height-sqr_size)/sqr_size)*sqr_size]

#Game setup
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width,height))
snake = Snake()
food = Food()
screen.fill(BG)

#Game Loop
while not lost:
    #Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            lost = True
        key1 = whatkey(event, key1)
 
    #Logic loop
    if pygame.time.get_ticks()-timer > delay(snake):
        timer = pygame.time.get_ticks()
        snake.move(key1)
        eat = dist(snake, food) < sqr_size**2
        if eat:
            food = Food()
        else:    
            snake.body.pop()
    lost = loser(snake, food)

    #Screen drawings
    screen.fill(BG)
    for i in snake.body:
        pygame.draw.rect(screen, BODY_C, (i[0], i[1], sqr_size, sqr_size), 0)
    pygame.draw.rect(screen, FOOD_C, (food.pos[0], food.pos[1], sqr_size, sqr_size), 0)
    pygame.display.set_caption("Snake. Your score is: {}".format(snake.score()))
    pygame.display.update()
    clock.tick(60)            

print("Your score is: {}".format(snake.score()))
sys.exit()