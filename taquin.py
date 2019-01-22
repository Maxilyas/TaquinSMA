import random

class Agent_Case:


    def __init__(self,x,y,valeur):
        self.posx = x
        self.posy = y
        self.valeur = valeur
        self.palet = Agent_palet(x,y,valeur)



class Agent_palet:


    def __init__(self,x,y,valeur):
        self.posx = x
        self.posy = y
        self.valeur = valeur

    def check_voisin(self):
        pass



class Puzzle:

    def __init__(self,taille):
        self.taille = taille
        self.cases = []
        self.palets = []
        list_elem =random.sample(range(taille*taille-1),taille*taille-1)

        for i in range(taille):
            for j in range(taille):
                self.cases.append(Agent_Case(i, j, i * taille + j))

        for i in range(taille):
            for j in range(taille):
                if j == taille-1 and i ==taille-1:
                    break
                self.palets.append(Agent_palet(i, j, list_elem[i * taille + j]))

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

    puzzle = Puzzle(3)
    print("CASES :")
    puzzle.afficherCases()
    print("PALETS :")
    puzzle.afficherPalets()

    print(puzzle.cases[0].palet.valeur)



