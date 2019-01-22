import random

# états : 1 = satisfait, 0 = non satisfait, -1 = fuite
# x c'est vers le bas, et y c'est vers la droite

def distance_but(palet, case):
    return abs(palet.posx - case.posx) + abs(palet.posy - case.posy)

class Agent_Case:
    def __init__(self,x,y,valeur):
        self.posx = x
        self.posy = y
        self.valeur = valeur
        self.etat = 1


class Agent_palet:
    def __init__(self,x,y,valeur,puzzle):
        self.posx = x
        self.posy = y
        self.valeur = valeur
        self.but = None
        self.etat = 0
        self.voisins = []

    def update_voisins(self):
        voisins = []
        for palet in puzzle.palets:
            if palet.posx == self.posx + 1 and palet.posy == self.posy:
                voisins.append(palet)
            if palet.posx == self.posx -1 and palet.posy == self.posy:
                voisins.append(palet)
            if palet.posx == self.posx and palet.posy == self.posy + 1:
                voisins.append(palet)
            if palet.posx == self.posx and palet.posy == self.posy - 1:
                voisins.append(palet)
        self.voisins = voisins

    # TODO : faire un try/except
    def get_but(self, cases):
        for case in cases:
            if case.valeur == self.valeur:
                self.but = case

    def check_satisfait(self):
        if self.but != None and self.posx == self.but.posx and self.posy == self.but.posy:
            self.etat = 1
        else:
            self.etat = 0

    def try_satisfaction(self):
        while self.etat != 1:
            list_distance = []
            list_voisins = []
            for voisin in self.voisins:
                list_distance.append(distance_but(voisin,self.but))
                list_voisins.append(voisin)

            cible = list_voisins[list_distance.index(min(list_distance))]
            self.agresser(cible)
            self.check_satisfait()

    def agresser(self,palet):
        palet.etat = -1
        palet.fuite()

    def fuite(self):
        voisins = self.update_voisins()
        # TODO : supprimer des voisins les contraintes
        #









class Puzzle:
    def __init__(self,taille):
        self.taille = taille
        self.cases = []
        self.palets = []
        list_elem = random.sample(range(taille*taille-1),taille*taille-1)

        for i in range(taille):
            for j in range(taille):
                self.cases.append(Agent_Case(i, j, i * taille + j))

        for i in range(taille):
            for j in range(taille):
                if j == taille-1 and i == taille-1:
                    break
                self.palets.append(Agent_palet(i, j, list_elem[i * taille + j], self))

        for palet in self.palets:
            palet.get_but(self.cases)
            palet.check_satisfait()


    def afficherPalets(self):
        for i in range(self.taille):
            for j in range(self.taille):
                #print(self.cases[i*self.taille+j].valeur,end=" ")
                    if not(i == self.taille-1 and j == self.taille-1):
                        print(self.palets[i*(self.taille)+j].valeur,end=" ")
            print("\n")
    def afficherCases(self):
        for i in range(self.taille):
            for j in range(self.taille):
                #print(self.cases[i*self.taille+j].valeur,end=" ")
                        print(self.cases[i*(self.taille)+j].valeur,end=" ")
            print("\n")



if __name__ == '__main__':
    TAILLE_PUZZLE = 3
    puzzle = Puzzle(TAILLE_PUZZLE)
    print("CASES :")
    puzzle.afficherCases()
    print("PALETS :")
    puzzle.afficherPalets()

    print(puzzle.cases[3].posx)
    print(puzzle.cases[3].posy)
