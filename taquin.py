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
        self.puzzle = puzzle

    def update_voisins(self):
        voisins = []
        # for palet in puzzle.palets:
        #     palet.check_satisfait()
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
        self.check_satisfait()
        while self.etat != 1:
            self.etat = -1
            distances = self.ordre_voisins()

            cible = distances[0][0]

            print(self.valeur, "agresse", cible.valeur)
            self.agresser(cible)
            self.check_satisfait()

            print("ETATS :")
            puzzle.afficherEtats()
            print("PALETS :")
            puzzle.afficherPaletsBis()

    def agresser(self,palet):
        if (palet.etat == 1):    # On n'agresse pas un palet satisfait (même si ça devrait déjà ne jamais arriver ...)
            print("nope")
            for blanc in self.puzzle.palets:
                if blanc.valeur == -1:  # Mais quand ça arrive on fait un mouvement aléatoire a la place, qui ne bouge pas de palet satisfait
                    print("dans if")
                    blanc.update_voisins()
                    while True :
                        cible =  random.choice(blanc.voisins)
                        if cible.etat != 1:
                            cible.agresser(blanc)
                            return 1

        palet.etat = -1
        try:
            palet.fuite(self)
        except RecursionError as re:
            for blanc in self.puzzle.palets:
                if blanc.valeur == -1:
                    blanc.update_voisins()
                    blanc.voisins[0].agresser(blanc)
                palet.etat = 0
                return 1

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
            # print("distances :", distances)
            # print("distance[0][0] :", distances[0][0].valeur)
            done = False
            while not done and distances:
                cible = distances[0][0]
                if cible.posx != palet.but.posx or cible.posy != palet.but.posy: # contrainte but
                    done = True
                else:
                    print("je ne peux pas agresser :", cible.valeur)
                    del distances[0]

            if not distances :
                print("a cours de cible ...")
                for blanc in self.puzzle.palets:
                    if blanc.valeur == -1:
                        blanc.update_voisins()
                        blanc.voisins[0].agresser(blanc)
                    palet.etat = 0
                    return 1
                sys.exit()

            print(self.valeur, "agresse", cible.valeur)
            self.agresser(cible)

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
        etatm1 = []

        for item in distances:
            if item[1] == 0:
                etat0.append(item)
            elif item[1] == -1:
                etatm1.append(item)

        etat0.sort(key=lambda tup: tup[2])
        etatm1.sort(key=lambda tup: tup[2])

        distances = []
        distances.extend(etat0)
        distances.extend(etatm1)

        for item in distances:
            if item[1] == 1:
                print("ne devrait pas arriver")
                sys.exit()

        if random.randint(0,35) == 42 :
            random.shuffle(distances)
            print("random move")
            return distances

        return distances


class Puzzle:
    def __init__(self,taille):
        self.taille = taille
        self.cases = []
        self.palets = []
        #list_elem = random.sample(range(taille*taille-1),taille*taille-1)
        list_elem = range(taille*taille-1)

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
            palet.puzzle = self
            # palet.check_satisfait()

    def shuffle(self):
        for i in range(1,40):
            for blanc in self.palets:
                if blanc.valeur == -1:  # Mais quand ça arrive on fait un mouvement aléatoire a la place, qui ne bouge pas de palet satisfait
                    blanc.update_voisins()
                    cible = random.choice(blanc.voisins)
                    cible.agresser(blanc)


    def afficherPalets(self):
        for i in range(self.taille):
            for j in range(self.taille):
                print(self.palets[i*(self.taille)+j].valeur,end=" ")
            print("\n")

    def afficherPaletsBis(self):
        for i in range(self.taille):
            for j in range(self.taille):
                print(self.paletxy(i,j).valeur, end=" ")
            print("\n")

    def afficherEtats(self):
        for i in range(self.taille):
            for j in range(self.taille):
                print(self.paletxy(i, j).etat, end=" ")
            print("\n")

    def paletxy(self,x,y):
        for palet in self.palets:
            if __name__ == '__main__':
                if palet.posx == x and palet.posy == y:
                    return palet

    def afficherCases(self):
        for i in range(self.taille):
            for j in range(self.taille):
                #print(self.cases[i*self.taille+j].valeur,end=" ")
                        print(self.cases[i*(self.taille)+j].valeur,end=" ")
            print("\n")



if __name__ == '__main__':
    TAILLE_PUZZLE = 3
    puzzle = Puzzle(TAILLE_PUZZLE)
    puzzle.shuffle()

    import copy
    depart = copy.deepcopy(puzzle)

    # print("CASES :")
    # puzzle.afficherCases()
    # print("ETATS :")
    # puzzle.afficherEtats()
    print("PALETS :")
    puzzle.afficherPaletsBis()

    liste_palets = []

    # méthode sale pour ordonner les satisfactions
    for palet in puzzle.palets:
        if palet.valeur == 0:
            liste_palets.append(palet)

    for palet in puzzle.palets:
        if palet.valeur == 1:
            liste_palets.append(palet)

    for palet in puzzle.palets:
        if palet.valeur == 2:
            liste_palets.append(palet)

    for palet in puzzle.palets:
        if palet.valeur == 3:
            liste_palets.append(palet)

    for palet in puzzle.palets:
        if palet.valeur == 6:
            liste_palets.append(palet)

    for palet in puzzle.palets:
        if palet.valeur == 4:
            liste_palets.append(palet)

    for palet in puzzle.palets:
        if palet.valeur == 5:
            liste_palets.append(palet)

    for palet in puzzle.palets:
        if palet.valeur == 7:
            liste_palets.append(palet)


    liste_palets[0].try_satisfaction()
    liste_palets[1].try_satisfaction()
    liste_palets[2].try_satisfaction()
    liste_palets[3].try_satisfaction()
    liste_palets[4].try_satisfaction()
    liste_palets[5].try_satisfaction()
    liste_palets[6].try_satisfaction()
    liste_palets[7].try_satisfaction()

    print("ETATS :")
    puzzle.afficherEtats()

    print("DEPART était :")
    depart.afficherPaletsBis()

