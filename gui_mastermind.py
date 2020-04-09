###########################################
#
# GUI MasterMind
#
# Author : Antoine-Alexis Bourdon
# Link : https://github.com/antoinealexisb/masterMind
# Version : 0.1.0
# Dependency : mastermind, tkinter
#
###########################################
import tkinter
import mastermind

class VueMM :

    def __init__(self,mmJ,mmO):
        '''VueMM, Mastermind -> VueMM
        '''
        self.__mm = mmJ
        self.__mmO = mmO
        self.__couleur = 0
        self.__prop = [0 for i in range(mmJ.taille())]
        self.__longueur = 10
        self.__elt_courant = self.__longueur - 1
        self.__fen = tkinter.Tk()
        self.__fen.title("Mastermind")
        
    def init_images(self) :
        self.__lesSpheres = []
        for i in range(9):
            self.__lesSpheres.append(tkinter.PhotoImage(file="img/sphere"+str(i)+".gif"))
        

    def lancer(self) :
        self.init_images()
        central = tkinter.Frame(self.__fen)
        plateaux = tkinter.Frame(central)
        plateauJ = tkinter.Frame(plateaux)
        plateauO = tkinter.Frame(plateaux)
        plateauJ.grid(row=0,column=0)
        plateauO.grid(row=0,column=1)
        self.__lesCodes = []
        self.__lesLabels = []
        self.__lesSecrets = []
        # pour le joueur
        self.__lesCodes.append([])
        self.__lesLabels.append([])
        self.__lesSecrets.append([])
        # pour la machine
        self.__lesCodes.append([])
        self.__lesLabels.append([])
        self.__lesSecrets.append([])
        for j in range(2) :
            if j == 0 :
                plat = plateauJ
                mess = tkinter.Label(plat,text="Joueur")
            else : 
                plat = plateauO
                mess = tkinter.Label(plat,text="Machine")
            mess.grid(row=1,columnspan=self.__longueur)
            for k in range(self.__mm.taille()):
                btn = tkinter.Button(plat,image = self.__lesSpheres[0])
                btn.grid(row=0,column=k+1)
                self.__lesSecrets[j].append(btn)
                
            for i in range(self.__longueur) :
                uneLigne = []
                lblJ = tkinter.Label(plat,text="",width=8)
                lblJ.grid(row=i+2,column=0)
                self.__lesLabels[j].append(lblJ)
                for k in range(self.__mm.taille()):
                   btn = tkinter.Button(plat,image = self.__lesSpheres[0])
                   btn.grid(row=i+2,column=k+1)
                   if j==0 :
                       btn.config(command=self.cree_controle_position(i,k))
                   uneLigne.append(btn)
                self.__lesCodes[j].append(uneLigne)

        paletteCouleurs = tkinter.Frame(central)
        self.__lesCouleurs = []
        for i in range(9):
            btn = tkinter.Button(paletteCouleurs,image = self.__lesSpheres[i])
            btn.config(relief="flat")
            btn.grid(row=i,column=0)
            btn.config(command=self.cree_controle_choisit_couleur(i))
            self.__lesCouleurs.append(btn)
        paletteCouleurs.pack(side="left")
        plateaux.pack(side="left")
        central.pack()
        
        bas = tkinter.Frame(self.__fen)
        self.__message = tkinter.Label(bas)
        self.__btnOk = tkinter.Button(bas,text="OK",command=self.controle_proposition)
        self.__btnOk.pack(side="left")
        btnRecommencer = tkinter.Button(bas,text="Recommencer",command=self.recommencer)
        btnRecommencer.pack(side="left")
        self.__message.pack(side="left") 
        bas.pack()
        self.__fen.mainloop()


    def cree_controle_choisit_couleur(self,i):
        def choisit_couleur():
            self.__couleur = i
            self.eteins_les_couleurs()
            self.__lesCouleurs[i]["relief"] = "solid"
        return choisit_couleur

    def eteins_les_couleurs(self) :
        for btn in self.__lesCouleurs :
            btn["relief"] = "flat"

    def cree_controle_position(self,i,j):
        def choisit_position():
            if i == self.__elt_courant :
                self.__prop[j] = self.__couleur
                self.__lesCodes[0][i][j]["image"] = self.__lesSpheres[self.__couleur]
        return choisit_position

    def met_a_jour_lbl(self,jm,bp,mp):
        self.__lesLabels[jm][self.__elt_courant]["text"] = "BP : "+str(bp)+"\nMP : "+str(mp)


    def recommencer(self) :
        self.__elt_courant = self.__longueur - 1
        for j in range(2) :
            for i in range(self.__longueur) :
                self.__lesLabels[j][i]["text"] = ""
                self.__lesLabels[j][i]["width"] = 8
                for k in range(self.__mm.taille()):
                   self.__lesCodes[j][i][k]["image"] = self.__lesSpheres[0]
                   self.__lesCodes[j][i][k]["relief"] = "sunken"
                   if j == 0 :
                       self.__lesCodes[0][i][k]["state"] = "normal"
            for k in range(self.__mm.taille()):
                self.__lesSecrets[j][k]["image"] = self.__lesSpheres[0]
        self.__btnOk["state"] = "normal"
        self.__prop = [0 for i in range(self.__mm.taille())]
        self.__message["text"] = ""
        self.__mm.lancer()
        self.__mmO.lancer()

    def dessine_proposition_machine(self,prop) :
        for i in range(len(prop)) :
            self.__lesCodes[1][self.__elt_courant][i]["image"] = self.__lesSpheres[prop[i]]

    def dessine_secret(self,prop,jm) :
        for i in range(len(prop)) :
            self.__lesSecrets[jm][i]["image"] = self.__lesSpheres[prop[i]]


    def controle_proposition(self):
        bp, mp = self.__mm.bp_mp(self.__prop)
        self.met_a_jour_lbl(0,bp,mp)
        self.__prop = [0 for i in range(self.__mm.taille())]
        if bp == self.__mm.taille() :
            self.__message["text"] = "Bravo ! vous avez gagné !"
            self.ferme_partie(0)
        else :
            p = self.__mmO.proposition()
            bp, mp = self.__mmO.bp_mp(p)
            self.met_a_jour_lbl(1,bp,mp)
            self.dessine_proposition_machine(p)
            self.__mmO.prend_score(bp,mp)
            if self.__mmO.partie_finie() :
                self.__message["text"] = "La machine a gagné !"
                self.ferme_partie(1)
            else :
                if self.__elt_courant > 0 :
                    self.__elt_courant -= 1
                else :
                    self.__message["text"] = "Vous avez perdu tous les deux !"
                    self.ferme_partie(2)

    def ferme_partie(self,jm) :
        for i in range(self.__mm.taille()) :
            if (jm < 2) :
                self.__lesCodes[jm][self.__elt_courant][i]["relief"] = "solid"
            self.__lesCodes[0][self.__elt_courant][i]["state"] = "disable"
        self.__btnOk["state"] = "disable"
        sec = self.__mm.get_secret()
        self.dessine_secret(sec,0)
        sec = self.__mmO.get_secret()
        self.dessine_secret(sec,1)
