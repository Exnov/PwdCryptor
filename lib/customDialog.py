from tkinter import *
from tkinter import messagebox
from lib.password import Password

"""
Classe pour creer une fenetre de dialogue appelée dans tabPassword.py (onglet 4 : Password), 
pour que l'user y renseigne les pourcentages de signes differents qui composent son mot de passe
"""
class CustomDialog:

    def __init__(self):
        self.root=None
        self.frame=None
        self.password=Password()
        self.isLaunched=False

    def create(self,t=""):
        print("creation")
        self.root=Tk()
        print(self.root)
        self.root.title(t)
        self.frame = Frame(self.root)
        self.frame.pack()

    def addEntries(self,data,entryResult,length,indice): #data est un array qui contient les labels de chaque entrée
        entries=[]
        for i in range(0,len(data)):
            label = Label(self.frame, text=data[i])
            label.grid(column=0, row=i, ipadx=5, pady=5, sticky=W)
            #==
            entry = Entry(self.frame, bd=3)
            entry.grid(column=1, row=i, ipadx=5, pady=5, sticky=W)
            entries.append((entry))
        btnValid = Button(self.frame, text="Valider", command=lambda : valid(entryResult,length,indice))
        btnValid.grid(column=0, row=len(data), ipadx=5, pady=5, sticky=E)
        btnCancel = Button(self.frame, text="Fini", command=lambda : cancel())
        btnCancel.grid(column=1, row=len(data), ipadx=5, pady=5, sticky=W)

        #on verifie les indications de l'user, et cree le mot de passe si les indications sont OK
        def valid(entry,length,indice):
            entry.delete(first=0, last=len(entry.get()))
            percents=[]
            pwd=""
            #==check des % renseignés par l'user, et conversion si OK des % en float : l'user doit renseigner les % en donnant un nombre à virgule entre 0 et 1 : ex: 0.5 pour 50%
            for e in entries:
                if(isFloat(e.get())):
                    percents.append(float(e.get()))
                else:
                    messagebox.showwarning("Attention", "Il faut renseigner tous les % avec un nombre entre 0 et 1 avec 1 seul chiffre après la virgule")
                    return
            #===================
            if(indice==1):
                pwd=self.password.numbersAndAllLetters(length,percents)
            elif(indice==2):
                pwd=self.password.numbersAndAllLetters(length,percents)
            else:
                pwd=self.password.allSigns(length,percents)
            entry.insert(0, pwd)

        #fait disparaitre la fenêtre de dialogue
        def cancel():
            self.root.destroy()

        #verifie si l'entree est un nombre à virgule
        def isFloat(value):  # value est un str avec la forme attendue "0.n" où est un chiffre
            check = False
            if (len(value) == 3):
                if (value[0] == '0' and value[1] == '.' and value[2].isnumeric):
                    check=True
            return check

    #affiche la fenêtre de dialogue
    def launch(self):
        self.isLaunched=True
        self.root.mainloop()

    #verifie si la fenêtre de dialogue est affichée
    def getIsLaunched(self):
        return self.isLaunched

    #fait disparaitre la fenêtre de dialogue
    def stop(self):
        self.isLaunched=False
        self.root.destroy()
