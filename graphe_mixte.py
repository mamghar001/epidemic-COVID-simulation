from random import randrange
from random import randint

import matplotlib.pyplot as plt

global states, states_temp, time_ill, Graph_edges
global nb_people 
nb_people=100
states = [0] * nb_people
states_temp=[0] * nb_people
time_ill= [0] * nb_people
i=0



Graph_edges=[[0] * nb_people for i in range(nb_people)]

global CONTAGION_RATE, INFECTION_TIME, DEATH_RATE, k, PARTY_TIME

CONTAGION_RATE=2
INFECTION_TIME=14
DEATH_RATE=4
PARTY_TIME=180
k=10

Dead=[]
Healthy=[]
Ill=[]
Immune=[]

############
#States     #
#healthy: 0 #
#Ill : 1    #
#dead: -1   #
#Immune: 2  # 
############


def init_circular_graph(p):
    states[p]=1
    time_ill[p]=1
    for i in range(nb_people):
        if ((i-1)>=0):
            Graph_edges[i][i-1]=1
            Graph_edges[i-1][i]=1
        if ((i+1)<nb_people):
            Graph_edges[i][i+1]=1
            Graph_edges[i+1][i]=1
    Graph_edges[0][nb_people-1]=1
    Graph_edges[nb_people-1][0]=1
def infect_circular_dynamic(p):
   
    r =randrange(nb_people)
    if (p-1)>=0:
        if (r<=CONTAGION_RATE) and (states[p-1]==0):
            states[p-1]=1
            time_ill[p-1]=1
    if (p+1)<nb_people:
        if (r<=CONTAGION_RATE) and (states[p+1]==0):
            states[p+1]=1
            time_ill[p+1]=1
       

    

def count_dead():
    count=0
    for i in range(nb_people):
        if states[i]==-1:
            count=count+1
    return count

def count_sick():
    count=0
    for i in range(nb_people):
        if states[i]==1:
            count=count+1
    return count

def count_healthy():
    count=0
    for i in range(nb_people):
        if states[i]==0:
            count=count+1
    return count

def count_immune():
    count=0
    for i in range(nb_people):
        if time_ill[i]<0:
            count=count+1
    return count
def init_random_graph(p):
    states[p]=1
    time_ill[p]=1
    l=[]
    for i in range(nb_people):
        l=[randint(0,nb_people-1) for i in range(k)]
        for e in l:
            
            Graph_edges[i][e]=1
            Graph_edges[e][i]=1
def infect_random_graph(p):
    for j in range(nb_people):
        if ((randrange(99)<=CONTAGION_RATE) and (Graph_edges[p][j]==1)):
            
            states[j]=1

def circular():
    p=randrange(nb_people-1)
    init_circular_graph(p)
    i=0
    while i<=PARTY_TIME:
        states_temp=states
        for j in range(nb_people):
            if (states_temp[j]==1):
                infect_circular_dynamic(j)
                if (randrange(99)<=DEATH_RATE):
                    states[j]=-1
        for k in range(nb_people):
            if states[k]==1:
                time_ill[k]=time_ill[k]+1
            if (time_ill[k]==INFECTION_TIME):
                states[k]==2
                time_ill[k]=0-2*nb_people
        
        Dead.append(count_dead())
        Healthy.append(count_healthy())
        Ill.append(count_sick())
        Immune.append(count_immune())
        i=i+1
    plt.plot(Dead,"--",label = "Dead ",color='r')   
    plt.plot(Healthy,"--",label = "Safe",color='g')
    plt.plot(Ill,"--",label = "Ill ",color='b')
    plt.plot(Immune,"--",label="Immune ",color='k')
    plt.xlabel("Days")
    plt.ylabel("People")
    plt.legend()
    plt.title("Circular dynamic")
    plt.show()

def random():
    p=randrange(nb_people-1)
    init_random_graph(p)
    i=0
    while i<=PARTY_TIME:
        states_temp=states
        for j in range(nb_people):
            if (states_temp[j]==1):
                infect_random_graph(j)
                if (randrange(99)<=DEATH_RATE):
                    states[j]=-1
        for k in range(nb_people):
            if states[k]==1:
                time_ill[k]=time_ill[k]+1
            if (time_ill[k]==INFECTION_TIME):
                states[k]==2
                time_ill[k]=0-2*nb_people
        
        Dead.append(count_dead())
        Healthy.append(count_healthy())
        Ill.append(count_sick())
        Immune.append(count_immune())
        i=i+1
    plt.plot(Dead,"--",label = "Dead ",color='r')   
    plt.plot(Healthy,"--",label = "Safe",color='g')
    plt.plot(Ill,"--",label = "Ill ",color='b')
    plt.plot(Immune,"--",label="Immune ",color='k')
    plt.xlabel("Days")
    plt.ylabel("People")
    plt.legend()
    plt.title("random dynamic")
    plt.show()

def mixte():
    p=randrange(nb_people-1)

    init_circular_graph(p)

    init_random_graph(p)
   
    i=0
    while i<=PARTY_TIME:
        states_temp=states
        for j in range(nb_people):
            if (states_temp[j]==1):
                infect_random_graph(j)
                infect_circular_dynamic(j)
            
                if (randrange(99)<=DEATH_RATE):
                    states[j]=-1
        for k in range(nb_people):
            if states[k]==1:
                time_ill[k]=time_ill[k]+1
            if (time_ill[k]==INFECTION_TIME):
                states[k]==2
                time_ill[k]=0-2*nb_people
        
        Dead.append(count_dead())
        Healthy.append(count_healthy())
        Ill.append(count_sick())
        Immune.append(count_immune())
        i=i+1
    plt.plot(Dead,"--",label = "Dead ",color='r')   
    plt.plot(Healthy,"--",label = "Safe",color='g')
    plt.plot(Ill,"--",label = "Ill ",color='b')
    plt.plot(Immune,"--",label="Immune ",color='k')
    plt.xlabel("Days")
    plt.ylabel("People")
    plt.legend()
    plt.title("mixte")
    plt.show()
    
#circular()
#random()
#mixte()
