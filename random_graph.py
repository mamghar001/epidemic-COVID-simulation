import networkx as nx
import random
import math
import numpy as np
import scipy
import matplotlib.pyplot as plt

class GraphClass:
    def __init__(self, N, input_graph, transmision_probability = None, healing_probability = None):
        """Initialize all the variables and graph to be used by all operations"""
        self.N = N
        self.input_graph = input_graph.copy()
        self.virus_strength = 0.0
        self.transmision_probability = transmision_probability
        self.healing_probability = healing_probability
        self.infected = []
        self.susceptible = []
        self.c = 0

    def calculate_val_prop(self):
        """Fonction qui calcule valeur propre de la matrice d'adjacence
        """
        self.N = nx.number_of_nodes(self.input_graph)
        val_prop = scipy.sparse.linalg.eigsh(nx.to_numpy_matrix(self.input_graph),
            k=1, which='LM', return_eigenvectors=False, mode='normal')

        self.max_val_prop = max(val_prop)
        print("Max valeur propre value: " + str(self.max_val_prop))

    def calculate_virus_strength(self, transmision_probability, healing_probability):
        """ Fonction qui calcule l'intensité du virus"""
        self.transmision_probability = transmision_probability
        self.healing_probability = healing_probability
        K = self.transmision_probability / self.healing_probability
        self.virus_strength = self.max_val_prop * K
        return self.virus_strength

    def infect_initial(self):
        """ Infecte les noeuds initiales du graphe"""
        self.c = math.ceil(self.N/10)
        self.infected.clear()

        #Choisit c noeuds aléatoires du graphe pour être infecter. et être ajouter à la liste des noeuds inféctés
        self.infected = random.sample( nx.nodes(self.input_graph) , self.c )

    def get_susceptible(self):
        self.susceptible.clear()
        #Ajoute chaque voisins des neouds inféctés à la liste des suspects
      for node in self.infected:
            neighbours = self.input_graph.neighbors(node)
            self.susceptible.extend(neighbours)
        #Supprime tous les noeuds infectés de la liste des suspects
        self.susceptible = list( set(self.susceptible).difference(set(self.infected)) )

    def infect(self):
        for node in self.susceptible:
            #Choisir une variable dans l'intervalle [1,0]
            x = random.random()

            #Si x est inférieure à transmision_probability , on infecte le noeud
            if x <= self.transmision_probability:
                self.infected.append(node)

    def heal(self):
        for node in self.infected[:]:
            #Choisir une variable dans l'intervalle [1,0]
            x = random.random()
            #Si x est inférieure à healing_probability, on immunise le noeud, en le supprimant des listes des inféctés
            if x <= self.healing_probability:
                self.infected.remove(node)

    def get_fraction_of_infected_nodes(self):
        # Pourcentage de la population infectée
        return len(self.infected) / self.N

    def immune_strategy_A(self, K):
        """Choisir k noeud pour l'immunisation."""
        nodes = random.sample( range(0,self.N) , K )
        #retirer les noeuds immunisés du graphe
        self.input_graph.remove_nodes_from(nodes)
        #réinitialiser le nombre des noeuds
        self.N = nx.number_of_nodes(self.input_graph)

    def immune_strategy_B(self, K):
        """
        Sélectionner les k noeuds avec le plus grand degré pour l'immunisation
        """
        degree = nx.degree(self.input_graph)
        #Trier les noeuds en fonction du degré
        highest_degree_nodes  = [x for x,y in sorted(degree.items(), key=lambda x: x[1], reverse=True)]
        #retirer les noeuds immunisés du graphe
        self.input_graph.remove_nodes_from( highest_degree_nodes[:K] )
        self.N = nx.number_of_nodes(self.input_graph)


    def immune_stratagy_C(self, K):
        self.N = nx.number_of_nodes(self.input_graph)
        #Calcul des plus grandes valeurs et vecteurs propres
        eig_value, eig_vector = scipy.sparse.linalg.eigsh( nx.to_numpy_matrix(self.input_graph),
            k=1, which='LM', return_eigenvectors=True, mode='normal')
        eig_vector_list = sorted(
            [(a, abs(b)) for a, b in enumerate(eig_vector)], key = lambda x: x[1], reverse=True)

        #donne l'indice des k grandes valeurs de eig_vector_list
        nodes = [eig_vector_list[i][0] for i in range(K)]
        #retirer les noeuds immunisés du graphe
        self.input_graph.remove_nodes_from(nodes)
        self.N = nx.number_of_nodes(self.input_graph)

    def infos(self):
       
        strr = "transmision_probability: " + str(self.transmision_probability)
        strr += "\nhealing_probability: " + str(self.healing_probability)
        strr += "\nvirus strength: " + str(self.virus_strength)
        return strr

def input_graph():
    """ Fonction qui crée un networkx graph"""
    rfile = open('../graphedata','r')
    nodes, edges = [int(x) for x in rfile.readline()]
    G = nx.Graph()
    for line in rfile:
        a, b = [int(x) for x in line]
        G.add_edge(a,b)
    return nodes,edges,G

def plot_line_graph(x, y, x1, y1):
    plt.plot( x, y, 'r')
    plt.xlabel(x1)
    plt.ylabel(y1)
    plt.show()


"*******************************************************"

if __name__ == '__main__':
    N, edges, input_graph = input_graph()

    trans_p1 = 0.25; trans_p2=0.01 #transmission probability
    heal_p1 = 0.70; heal_p2 = 0.60 #healing probability
    k1 = 300 #nombres des vaccins

    g_strategy_a = GraphClass(N, input_graph, transmision_probability = trans_p1, healing_probability = heal_p1)
    g_strategy_b = GraphClass(N, input_graph, transmision_probability = trans_p1, healing_probability = heal_p1)
    g_strategy_c = GraphClass(N, input_graph, transmision_probability = trans_p1, healing_probability = heal_p1)


    #Immunize les graphes avec les différentes stratégies
    g_strategy_a.immune_strategy_A(k1)
    g_strategy_b.immune_strategy_B(k1)
    g_strategy_c.immune_strategy_C(k1)


    matrix_a = np.zeros(shape=(100,10))
    matrix_b = np.zeros(shape=(100,10))
    matrix_c = np.zeros(shape=(100,10))

    # Calculer la moyenne des personnes inféctées avec les différentes stratégies
    matrix_b[0,0] = g_strategy_b.c / g_strategy_b.N
    matrix_c[0,0] = g_strategy_c.c / g_strategy_c.N


    for simulation in range(1, 10):
        #Infecter les noeuds (initialement)
        g_strategy_a.infect_initial()
        g_strategy_b.infect_initial()
        g_strategy_c.infect_initial()
        for t in range(1, 100):
            #Trouver les noeuds susceptibles de chaque graphe
            g_strategy_a.get_susceptible()
            g_strategy_b.get_susceptible()
            g_strategy_c.get_susceptible()

            #Immuniser
            g_strategy_a.heal()
            g_strategy_b.heal()
            g_strategy_c.heal()

            #Infecter des neouds susceptibles
            g_strategy_a.infect()
            g_strategy_b.infect()
            g_strategy_c.infect()

            #calcul de la moyenne des personnes inféctées
            matrix_a[t, simulation] =  g_strategy_a.get_fraction_of_infected_nodes()
            matrix_b[t, simulation] =  g_strategy_b.get_fraction_of_infected_nodes()
            matrix_c[t, simulation] =  g_strategy_c.get_fraction_of_infected_nodes()


    x = range(0,100)


    y_s_a = [ a/10 for a in matrix_a.sum(axis=1) ]
    y_s_b = [ a/10 for a in matrix_b.sum(axis=1) ]
    y_s_c = [ a/10 for a in matrix_c.sum(axis=1) ]

    #Affichage des résultats
    plot_line_graphs(x, y_s_a, "nombre de jours", "moyenne des personnes infectées")
    plot_line_graphs(x, y_s_b, "nombre de jours", "moyenne des personnes infectées")
    plot_line_graphs(x, y_s_c, "nombre de jours", "moyenne des personnes infectées")
