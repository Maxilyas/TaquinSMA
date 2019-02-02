import random

# états : 1 = satisfait, 0 = non satisfait, -1 = fuite
# x c'est vers le bas, et y c'est vers la droite
import sys


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
            palet.check_satisfait()
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

    def try_satisfaction(self):
        while self.etat != 1:
            self.update_voisins()
            list_distance = []
            list_voisins = []
            for voisin in self.voisins:
                list_distance.append(distance_but(voisin,self.but))
                list_voisins.append(voisin)

            cible = list_voisins[list_distance.index(min(list_distance))]

            print(self.valeur, "agresse", cible.valeur)
            self.agresser(cible)
            self.check_satisfait()
            # print("CASES :")
            # puzzle.afficherCases()
            print("PALETS :")
            puzzle.afficherPaletsBis()
            #input("Press Enter to continue...")

    def agresser(self,palet):
        palet.etat = -1
        palet.fuite(self)
        self.update_voisins()

        if palet.valeur != -1:
            for voisin in self.voisins:
                if(voisin.valeur == -1):
                    voisin.fuite(self)

        palet.etat = 0

    def fuite(self,palet):
        print(self.valeur,": je fuis l'agent :",palet.valeur)
        self.update_voisins()
        if(self.valeur == -1): # Agent blanc
            self.echanger_place(palet)
            return 1
        else:
            distances = self.ordre_voisins()
            done = False
            while not done and distances:
                cible = distances[0][0]
                if cible.posx != palet.but.posx or cible.posy != palet.but.posy: # contrainte but
                    done = True
                else:
                    del distances[0]

            if not distances : sys.exit()
            print(self.valeur, "agresse", cible.valeur)
            self.agresser(cible)



            # list_distance = []
            # list_voisins = []
            # for voisin in self.voisins:
            #     #print("voisin :", voisin.valeur)
            #     if voisin.posx != palet.but.posx or voisin.posy != palet.but.posy: # première contrainte, on ne va pas sur le but de l'agresseur
            #         list_distance.append(distance_but(voisin, self.but))
            #         list_voisins.append(voisin)
            #
            # done = False
            #
            # while not done:
            #     if len(list_distance) == 0:
            #         print("fuck")
            #         sys.exit()
            #
            #     cible = list_voisins[list_distance.index(min(list_distance))]
            #     del list_voisins[list_distance.index(min(list_distance))]
            #     del list_distance[list_distance.index(min(list_distance))]
            #
            #
            #     if cible.etat != 1:
            #         print(self.valeur,"agresse",cible.valeur)
            #         self.agresser(cible)
            #         done = True
            #     else:
            #         print("je ne peux pas agresser",cible.valeur)
            #
            # return 0


    def echanger_place(self,palet):
        x_palet = palet.posx
        y_palet = palet.posy
        x_self = self.posx
        y_self = self.posy
        palet.posx = x_self
        palet.posy = y_self
        self.posx = x_palet
        self.posy = y_palet

    def ordre_voisins(self):
        self.update_voisins()
        distances = []
        for voisin in self.voisins:
            distances.append((voisin, voisin.etat, distance_but(voisin, self.but)))

        etat0 = []
        etat1 = []
        etatm1 = []

        for item in distances:
            if item[1] == 0:
                etat0.append(item)
            elif item[1] == 1:
                etat1.append(item)
            elif item[1] == -1:
                etatm1.append(item)

        etat0.sort(key=lambda tup: tup[2])
        etat1.sort(key=lambda tup: tup[2])
        etatm1.sort(key=lambda tup: tup[2])

        distances = []
        distances.extend(etat0)
        distances.extend(etatm1)
        distances.extend(etat1)

        # print(distances)
        return distances


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
                    self.palets.append(Agent_palet(i,j,-1,self))# Agent palet blanc
                    break
                self.palets.append(Agent_palet(i, j, list_elem[i * taille + j], self))

        for palet in self.palets:
            palet.get_but(self.cases)
            palet.check_satisfait()


    def afficherPalets(self):
        for i in range(self.taille):
            for j in range(self.taille):
                print(self.palets[i*(self.taille)+j].valeur,end=" ")
            print("\n")

    def afficherPaletsBis(self):
        for i in range(self.taille):
            for j in range(self.taille):
                self.paletxy(i,j)
            print("\n")

    def paletxy(self,x,y):
        for palet in self.palets:
            if __name__ == '__main__':
                if palet.posx == x and palet.posy == y:
                    print(palet.valeur, end=" ")

    def afficherCases(self):
        for i in range(self.taille):
            for j in range(self.taille):
                #print(self.cases[i*self.taille+j].valeur,end=" ")
                        print(self.cases[i*(self.taille)+j].valeur,end=" ")
            print("\n")



if __name__ == '__main__':
    TAILLE_PUZZLE = 3
    puzzle = Puzzle(TAILLE_PUZZLE)
    # print("CASES :")
    # puzzle.afficherCases()
    print("PALETS :")
    puzzle.afficherPaletsBis()

    puzzle.palets[7].try_satisfaction()

    # puzzle.palets[7].ordre_voisins()

    # print("CASES :")
    # puzzle.afficherCases()
    print("PALETS :")
    puzzle.afficherPaletsBis()
