import random
import numpy as np
import matplotlib.pyplot as plt

class case: #case du labyrinthe
    def __init__(self,x,y):
        self.pos = (x,y)
        self.val = 0


class labyrinthe:

    def __init__(self,n):
        self.taille = n
        self.tab = []
        self.pos = []
        self.wall = []
        self.ufwall = []

        for x in range(n): #Création de la liste des cases 
            for y in range(n):
                self.tab.append(case(x,y))

        for p in self.tab: #Liste des positions des cases
            self.pos.append(p.pos)
        
        for k in range(len(self.tab)): #Valeur de chaque case de 0 à n^2
            self.tab[k].val = k

        
        for i in range(n): #Liste des murs, tuple des liaisons entre les index des cases
            for j in range(n):
                if i < n-1:
                    self.wall.append((self.pos.index((i,j)), self.pos.index((i+1,j))))
                if j < n-1:
                    self.wall.append((self.pos.index((i,j)), self.pos.index((i,j+1))))

        for w in self.wall:
            self.ufwall.append(w)


    def index_val(self,val): #renvoie liste des index des cases de même valeur
        eq_val = []
        for i in range(len(self.tab)):
            if self.tab[i].val == val:
                eq_val.append(i)
        return eq_val

    def parfait(self): #test pour savoir si le labyrinthe est parfait (ie les valeurs sont nulles)
        for c in self.tab:
            if c.val != 0:
                return False
        return True

    def link(self): #suppresion d'un mur et liaison des deux espaces
        i = random.choice(range(len(self.ufwall)))
        w = self.ufwall.pop(i)
        self.wall.remove(w)

        minimum = min(self.tab[w[0]].val, self.tab[w[1]].val)

        for p in self.index_val(self.tab[w[0]].val):
            self.tab[p].val = minimum

        for q in self.index_val(self.tab[w[1]].val):
            self.tab[q].val = minimum

        self.ufwall = []
        for u in range(len(self.wall)):
            a = self.wall[u]
            if self.tab[a[0]].val != self.tab[a[1]].val:
                self.ufwall.append(a)


    def grid(self): #array représentant le labyrinthe et les murs 
        n = self.taille
        g = np.zeros((2*n + 1, 2*n + 1), dtype=np.uint8)
        for i in range(2*n+1):
            for j in range(2*n+1):
                if i == 0 or j == 0 or i == 2*n or j == 2*n:
                    g[i,j] = 1
                elif i%2 == 0 and j%2 == 0:
                    g[i,j] = 1
        g[0,1] = 0
        g[2*n,2*n-1] = 0

        for c in self.wall:
            g[int((2*self.tab[c[0]].pos[0]+2*self.tab[c[1]].pos[0]+2)/2),int((2*self.tab[c[0]].pos[1]+2*self.tab[c[1]].pos[1]+2)/2)] = 1
        return g

    def plot_lab(self): #affichage du labyrinthe
        plt.imshow(self.grid())
        plt.show()


L = labyrinthe(10)

while L.parfait() != True:
    L.link()

L.plot_lab()

