from random import randrange
import pygame
import sys



# Parameters :

PROBA_DEATH = 50  #number out of 100 . the black plague was 100%. smallpox was ~30%-35%
CONTAGION_RATE = 4.5  # This is the R0 factor. Number of people an individual will infect on average
INFECTION_TIME = 10 # 10 is a good for watching
MAX_CONNECTED_NEIGHBOURS = 50 # k
VACCINATION_RATE = 0
SIMULATION_SPEED = 25   # time between days in milliseconds. 0: fastest.
                        # 500 means every day the simulation pauses for 500 ms
                        # 25 is good for watching
TYPE_GRAPH = "CIRCULAR" # "CIRCULAR", "ALEATORY","MIX"
nb_rows = 50
nb_cols = 50

k2 = 1
# Functions :

#STATES :
# 0: healthy
# 1: immune
# -1: dead

global states, states_temp
states = [[0] * nb_cols for i1 in range(nb_rows)]
states_temp = [[0] * nb_cols for i1 in range(nb_rows)]

PROBA_INFECT = CONTAGION_RATE * 10

def get_neighbour(x, y): #should be depending on type of graph
    incx = randrange(3)
    incy = randrange(3)
    incx = (incx * 1) - 1
    incy = (incy * 1) - 1
    x2 = x + incx
    y2 = y + incy
    if x2 < 0:
        x2 = 0
    if x2 >= nb_cols:
        x2 = nb_cols - 1
    if y2 < 0:
        y2 = 0
    if y2 >= nb_rows:
        y2 = nb_rows - 1
    return [x2, y2]

# neighbours are (x-1,y) and (x+1,y)
#returns [[x1,x2],[y1,y2]]
def get_neighbour_circular(x,y): #selon x et y (modulo n)
    if x % nb_rows != 0 and x % nb_rows != nb_rows - 1 :
        return [[x-1,x+1],[y,y]]
    if x % nb_rows == 0:
        if y >= 1:
            return [[nb_rows -1,1],[y-1,y]]
        else:
            return [[nb_rows -1,1],[nb_cols -1,y]]
    if x % nb_rows == nb_rows - 1 :
        if y < nb_cols -1:
            return [[nb_rows - 2,0],[y,y+1]]
        else:
            return [[nb_rows - 2,0],[y,0]]

#in_touch is k' defined in subject
def infect_circular(neighbours,in_touch):
    if in_touch == 1:
        idx=randrange(1)
        x2 = neighbours[0][idx]
        y2 = neighbours[1][idx]
        neigh_state = states[x2][y2]
        if neigh_state == 0:
            states_temp[x2][y2] = 10
    else:
        x1=neighbours[0][0]
        x2=neighbours[0][1]
        y1=neighbours[1][0]
        y2=neighbours[1][1]
        states_temp[x1][y1] = 10
        states_temp[x2][y2] = 10
    return



global display
global myfont
global initial_pause

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
RED = (255,0,0)

def init_screen():
    global display

    global myfont
    myfont = pygame.font.SysFont('Calibri', 40)
    display.fill(WHITE)

    image = pygame.image.load("death_toll.jpg").convert_alpha()
    image = pygame.transform.rotozoom(image, 0, .35)

    display.blit(image, (540, 23))


def vaccinate():
    for x in range(nb_cols):
        for y in range(nb_rows):
            if randrange(99) < VACCINATION_RATE:
                states[x][y] = 1


def count_dead():
    global states
    count = 0
    for x in range(nb_cols):
        for y in range(nb_rows):
            if states[x][y] == -1:
                count = count + 1
    return count


def main():
    pygame.init()

    pygame.font.init()

    global display
    display=pygame.display.set_mode((800,750),0,32)
    pygame.display.set_caption("COVID-19")

    init_screen()

    global states, states_temp
    states[5][5] = 10
    vaccinate()

    image = pygame.image.load("death_toll.jpg").convert_alpha()
    image = pygame.transform.rotozoom(image, 0, .35)

    display.blit(image, (540, 23))

    global initial_pause
    initial_pause = True

    it = 0
    death_toll = 0 # count of deaths
    while True:
        pygame.time.delay(SIMULATION_SPEED) # -------> simulation speed
        it = it + 1
        if it <= 10000 and it >= 2:
            states_temp = states.copy()
            for x in range(nb_cols):
                for y in range(nb_rows):
                    state = states[x][y]
                    if state == -1: # --------> if dead
                        pass
                    if state >= 10:
                        states_temp[x][y] = state + 1 # ----------> each day pass
                    if state >= INFECTION_TIME + 10: #20 INFECTION_TIME + 10
                        if randrange(99) < PROBA_DEATH:
                            states_temp[x][y] = -1
                        else:
                            states_temp[x][y] = 1 # ------------> immunised
                    if state >= 10 and state <= 20:
                        if randrange(99) < PROBA_INFECT:
                            #neighbour = get_neighbour(x, y)
                            neighbour=get_neighbour_circular(x,y)
                            infect_circular(neighbour,k2)
                            #x2 = neighbour[0]
                            #y2 = neighbour[1]
                            #neigh_state = states[x2][y2]
                            #if neigh_state == 0:
                            #    states_temp[x2][y2] = 10 # -------> infection done here
            states = states_temp.copy()
            death_toll = count_dead()
        pygame.draw.rect(display, WHITE, (450, 30, 80, 50))
        textsurface = myfont.render(str(death_toll), False, (0, 0, 0))
        display.blit(textsurface, (450, 30))
        for x in range(nb_cols):
            for y in range(nb_rows):
                if states[x][y] == 0:
                    color = BLACK
                if states[x][y] == 1:
                    color = GREEN
                if states[x][y] >= 10:
                    color = RED #(states[x][y] * 12, 50, 50)
                if states[x][y] == -1:
                    color = WHITE
                pygame.draw.circle(display, color, (100 + x * 12 + 5, 100 + y * 12 + 5), 5)
                pygame.draw.rect(display, WHITE, (100 + x * 12 + 3, 100 + y * 12 + 4, 1, 1))
                pygame.draw.rect(display, WHITE, (100 + x * 12 + 5, 100 + y * 12 + 4, 1, 1))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    states = [[0] * nb_cols for i1 in range(nb_rows)]
                    states_temp = [[0] * nb_cols for i1 in range(nb_rows)]
                    vaccinate()
                    states_temp = states.copy()
                    states[5][5] = 10
                    init_screen()
                    it = 0
                    death_toll = 0
                    initial_pause = True
        pygame.display.update()
        if it == 1:
            initial_pause = True
        if initial_pause:
            while initial_pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            initial_pause = False
                            break
#if __name__ == '__main__':
main()
