###########################################
#
# Code MasterMind
#
# Author : Antoine-Alexis Bourdon
# Link : https://github.com/antoinealexisb/masterMind
# Version : 0.1.0
# Dependency : random
#
###########################################
from random import randint

class Proposition:
    

    def __init__(self,prop=None,dim=4,nb_couleurs=6):
        '''Proposition, list(int), int, int -> Proposition
        '''
        self.__mp = None
        self.__bp = None
        self.__nb_couleurs = nb_couleurs
        self.__dim = dim
        self.__prop = None
        if prop is not None :
            self.__dim = len(prop)
            self.__prop = prop[:]


    def set_mal_places(self,mp):
        '''Proposition, int -> None
        '''
        self.__mp = mp

    def set_bien_places(self,bp):
        '''Proposition, int -> None
        '''
        self.__bp = bp

    def mp(self):
        '''Proposition -> int
        '''
        return self.__mp

    def bp(self):
        '''Proposition -> int
        '''
        return self.__bp

    def proposition_suivante(self):
        '''Proposition -> Proposition
        '''
        assert self.__prop is not None
        prop = self.__prop[:]
        ind = 0
        while ind < len(prop) and prop[ind] == (self.__nb_couleurs - 1) :
            prop[ind] = 0
            ind += 1
        if ind < len(prop) :
            prop[ind] += 1
        return Proposition(prop,nb_couleurs=self.__nb_couleurs)
            
    def calcule_bp_mp(self,prop):
        '''Proposition, list(int) -> int,int
        '''
        temp1 = prop[:]
        temp2 = self.proposition()
        bp = self.__calcule_bp(temp1,temp2)
        mp = self.__calcule_mp(temp1,temp2)
        return bp,mp

    def valide(self,prop):
        '''Proposition, list(int) -> boolean
        '''
        return (self.__bp, self.__mp) == (self.calcule_bp_mp(prop))

    def __calcule_bp(self,prop1,prop2):
        '''Proposition, list(int), list(int) -> int
        '''
        ind = 0
        bp = 0
        while ind < len(prop1):
            if prop1[ind] == prop2[ind] :
                bp += 1
                del(prop1[ind])
                del(prop2[ind])
            else :
                ind += 1
        return bp


    def __calcule_mp(self,prop1,prop2):
        '''Proposition, list(int), list(int) -> int
        '''
        ind = 0
        mp = 0
        while ind < len(prop1) :
            ind2 = 0
            while ind2 < len(prop2) :
                if prop2[ind2] == prop1[ind]:
                    mp += 1
                    del(prop2[ind2])
                    ind2 = len(prop2)
                else :
                    ind2 += 1
            ind += 1
        return mp

    def proposition(self) :
        '''Proposition -> list(int)
        '''
        return self.__prop[:]

    def __str__(self) :
        '''Proposition -> str
        '''
        mess = str(self.__prop)
        if not (self.__bp is None) :
            mess += " - BP : " + str(self.__bp)
            mess += " - MP : " + str(self.__mp)
        return mess

    ## fin de la classe Proposition


class Mastermind:

    def __init__(self,nb_couleurs=6,taille=4):
        '''Mastermind, int, int -> Mastermind
        '''
        self.__nb_couleurs = nb_couleurs
        self.__taille = taille
        self.__historique = []
        self.__mystere = None

    def lancer(self) :
        '''Mastermind -> None
        '''
        self.__mystere = self.generer_alea()
        self.__historique = []
        

    def generer_alea(self) :
        '''Mastermind -> Proposition
        '''
        prop = []
        for i in range(self.__taille):
            prop.append(randint(0,self.__nb_couleurs-1))
        return Proposition(prop,nb_couleurs=self.__nb_couleurs)

    def get_secret(self) :
        return self.__mystere.proposition()

    def proposition(self):
        '''Mastermind -> list(int)
        '''
        if len(self.__historique) == 0:
            self.__historique.append(self.generer_alea())
        else:
            prop_depart = self.__historique[-1].proposition_suivante()
            while not self.est_valide(prop_depart.proposition()) :
                prop_depart = prop_depart.proposition_suivante()
            self.__historique.append(prop_depart)
        return self.__historique[-1].proposition()


    def est_valide(self,code) :
        '''Mastermind -> list(int)
        '''
        for prop in self.__historique :
            if not prop.valide(code) :
                return False
        return True


    def bp_mp(self,prop) :
        '''Mastermind, list(int) -> int,int 
        '''
        assert self.__mystere is not None
        return self.__mystere.calcule_bp_mp(prop)

    def prend_score(self,bp,mp):
        '''Mastermind, int, int -> None 
        '''
        self.__historique[-1].set_bien_places(bp)
        self.__historique[-1].set_mal_places(mp)

    def __str__(self) :
        '''Mastermind -> str
        '''
        mess = ''
        if self.__mystere is None :
            mess = "La partie n'a as démarré."
        else :
            mess = "Mystere : " + self.__mystere.__str__()
            for prop in self.__historique :
                mess += "\n" + prop.__str__()
        return mess
            

    def partie_finie(self) :
        '''Mastermind -> boolean
        '''
        return len(self.__historique) > 0 and \
               (self.__historique[-1].bp() == self.__taille)


    def taille(self) :
        return self.__taille
