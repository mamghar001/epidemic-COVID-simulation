from random import randrange
import pygame
import sys
import matplotlib.pyplot as plt


# Parameters / Variables :#######################################################################

PROBA_DEATH = 3.5 #3.5% is realistic
                  #. the black plague was 100%. smallpox was ~30%-35%
                       
CONTAGION_RATE = 4  # This is the R0 factor.

SIMULATION_SPEED = 60   # time between days in milliseconds. 0: fastest.
                        # 500 means every day the simulation pauses for 500 ms
                        # 25 is good for watching
                
TYPE_GRAPH = "PERSONALISED" # "CIRCULAR","PERSONALISED"
TYPE_STATE = "dynamic" # "static" or "dynamic"

PARTY_TIME = 180 #180 (6 month)

case_confined = 4  #0 for "no tests"
                  #1 for "no tests but with quarantine"
                  #2 for "for tests on relatives of the deceased"
                  #3 for "random testing"
                  #4 fore "combination of 2 and 3"
                  
Probability_test = 70 # 70% the probability of correctness of covid test
Number_tests = 100 # number of tests daily

VACCINATION_RATE = 0  # 0 to 100

nb_rows = 50 #size graph (> 5)
nb_cols = 50 #size graph (> 5)

Initial_ill_number = 1 # 1 or 2

# CODE :##########################################################################################

# STATES :##########
# 0: healthy       #
# 1: immune        #
# -1: dead         #
# -100 : confined  #
####################

global states, states_temp , Graph_edges
states = [[0] * nb_cols for i1 in range(nb_rows)]
states_temp = [[0] * nb_cols for i1 in range(nb_rows)]
Graph_edges=[[0] * nb_cols for i1 in range(nb_rows)]

PROBA_INFECT = CONTAGION_RATE * 10
INFECTION_TIME = 10 
MAX_CONNECTED_NEIGHBOURS = 50 # k
k2 = 1  #this is k' (or in code : in_touch)


##############################################
#                                            #
#    Circular Graph   (poor simulation)      #
#                                            #
##############################################

def get_neighbour_circular_dynamic(x,y): 
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

def infect_circular_dynamic(neighbours,in_touch):
    if in_touch == 1:
        idx=randrange(2)
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
        if states[x2][y2] == 0:
            states_temp[x2][y2] = 10
        if states[x1][y1] == 0:
            states_temp[x1][y1] = 10

def init_circular_graph_edges():
    for i in range(nb_cols) :
        for j in range(nb_rows):
            if not isinstance(Graph_edges[i][j],list) :
                idx=randrange(2)
                neighbours=get_neighbour_circular_dynamic(j,i)
                connected_x=neighbours[0][idx]
                connected_y=neighbours[1][idx]
                Graph_edges[i][j]=[connected_x,connected_y]
                Graph_edges[connected_y][connected_x]=[i,j]

global ix
ix= randrange(2)

def infect_circular_static(x,y,in_touch):
    if in_touch == 1:
        print(ix)
        if ix  ==1:
            states_temp[4][5] = 10
        else:
            states_temp[6][5] = 10
    else:
        neighbours = get_neighbour_circular_dynamic(x,y)
        x1=neighbours[0][0]
        x2=neighbours[0][1]
        y1=neighbours[1][0]
        y2=neighbours[1][1]
        if states[x2][y2] == 0:
            states_temp[x2][y2] = 10
        if states[x1][y1] == 0:
            states_temp[x1][y1] = 10

##############################################
#                                            #
# Personalised Graph for better simulation : #
#                                            #
##############################################

def get_neighbour(x, y):
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

def get_all_neighbours(x, y):
    neighbours = []
    for i in range(0,3):
        for incy in range(0,3):
            incx = (i * 1) - 1
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
            if (x != x2 or y != y2):
                neighbours.append([x2,y2])
    return neighbours

def infect(neighbour):
    x2 = neighbour[0]
    y2 = neighbour[1]
    neigh_state = states[x2][y2]
    if neigh_state == 0:
        states_temp[x2][y2] = 10

def confine(x,y):
    states_temp[x][y] = -100

def confine_with_test(x,y):
    if states_temp[x][y] >= 10:
        if randrange(99) < Probability_test:
            states_temp[x][y] = -100

def tests(n):
    for i in range(n):
        incx = randrange(nb_rows - 1)
        incy = randrange(nb_cols - 1)
        if states_temp[incx][incy] >= 10:
            if randrange(99) < Probability_test:
                states_temp[incx][incy] = -100
        print("Tests done on (",incx,incy,")")
        

global display
global myfont
global initial_pause

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
RED = (255,0,0)
YELLOW = (255,255,0)

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

def count_healthy():
    global states
    count = 0
    for x in range(nb_cols):
        for y in range(nb_rows):
            if states[x][y] == 0:
                count = count + 1
    return count

def count_immune():
    global states
    count = 0
    for x in range(nb_cols):
        for y in range(nb_rows):
            if states[x][y] == 1:
                count = count + 1
    return count

def count_ill():
    global states
    count = 0
    for x in range(nb_cols):
        for y in range(nb_rows):
            if states[x][y] > 1:
                count = count + 1
    return count

Dead = []
ill_toll = []
healthy_toll = []
immune_toll = []

##############################################
#                                            #
#                   MAIN                     #
#                                            #
##############################################

def main():
    pygame.init()

    pygame.font.init()

    global display
    display=pygame.display.set_mode((800,750),0,32)
    pygame.display.set_caption("COVID-19")

    init_screen()

    global states, states_temp

    if Initial_ill_number == 1:
        states[5][5] = 10
    else:
        states[5][5] = 10
        states[nb_cols - 5][nb_rows - 5] = 10

    vaccinate()

    image = pygame.image.load("death_toll.jpg").convert_alpha()
    image = pygame.transform.rotozoom(image, 0, .35)

    display.blit(image, (540, 23))

    global initial_pause
    initial_pause = True

    it = 0
    death_toll = 0

    while True:
        pygame.time.delay(SIMULATION_SPEED)
        it = it + 1 # day passes        
        if it <= PARTY_TIME and it >= 2:
            states_temp = states.copy()
            for x in range(nb_cols):
                for y in range(nb_rows):
                    state = states[x][y]
                    if state == -1:
                        pass
                    if state >= 10:
                        states_temp[x][y] = state + 1
                    if state >= INFECTION_TIME + 10:
                        if randrange(99) < PROBA_DEATH:
                            states_temp[x][y] = -1
                            if case_confined == 1:
                                neighbours = get_all_neighbours(x,y)                                
                                for l in range(len(neighbours)):
                                    confine(neighbours[l][0],neighbours[l][1])
                                    print("Confined _case1_(",x,y,")")
                            if case_confined == 2 or case_confined == 4:
                                neighbours = get_all_neighbours(x,y)                                
                                for l in range(len(neighbours)):
                                    confine_with_test(neighbours[l][0],neighbours[l][1])
                                    print("Confined _case2_(",x,y,")")
                        else:
                            states_temp[x][y] = 1 
                    if state >= 10 and state <= 20:
                        if randrange(99) < PROBA_INFECT:
                            if TYPE_GRAPH == "CIRCULAR":
                                if TYPE_STATE == "static":
                                    infect_circular_static(x,y,k2)
                                else:
                                    neighbours=get_neighbour_circular_dynamic(x,y)
                                    infect_circular_dynamic(neighbours,k2)
                            if TYPE_GRAPH == "PERSONALISED":
                                neighbour=get_neighbour(x,y)
                                infect(neighbour)
            if case_confined == 3 or case_confined == 4 :
                tests(Number_tests)
            states = states_temp.copy()
            death_toll = count_dead()
            Dead.append(death_toll)
            ill_toll.append(count_ill())
            healthy_toll.append(count_healthy())
            immune_toll.append(count_immune())
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
                    color = RED 
                if states[x][y] == -1:
                    color = WHITE
                if states[x][y] < -1:
                    color = YELLOW
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
                            if Dead != []:
                                #plt.figure()
                                plt.plot(Dead,label = "Dead count",color='r')
                                plt.plot(ill_toll,label = "Ill count",color='b')
                                plt.plot(healthy_toll,label = "Healthy count",color='k')
                                plt.plot(immune_toll,label = "Immune count",color='g')
                                plt.legend()
                                plt.grid(True, which="both", linestyle='--')
                                plt.xlabel("Jours")
                                plt.ylabel("Nombre de presonnes")
                                plt.title("combinaison des stratégies 2 (100 tests/jour) et 3")
                                plt.show()
                                pygame.quit()
                                sys.exit()
                            break
if __name__ == '__main__':
    main()

    
