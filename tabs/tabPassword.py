from tkinter import ttk, Label, W, N, Button, Radiobutton, HORIZONTAL, Entry, messagebox, TclError
from tkinter.ttk import Separator

from lib.customDialog import CustomDialog
from lib.password import Password

"""
classe de l'onglet 4 "Password" : 
sert à :
==> générer des mots de passe : si l'user manque d'inspiration
PRECISIONS :
- Conditions de création d'un mot de passe :
    ==> préciser la longueur du mot de passe, exprimee en nombre de caracteres
    ==> choisir les types de caracteres (nombres, lettres, caracteres spéciaux) qui composeront le mot de passe  : 4 combinaisons possibles
    ==> choisir entre "Sans % de signes" et "Avec des % de signes" : ne change rien au cas où l'utilisateur choisit de creer un mot de passe avec uniquement des nombres
        ==> "Sans % de signes" : signifie que les types de caracteres seront presents dans le mot de passe en quantite aleatoire ; sauf si l'user choisit de creer un mot de passe uniquement avec des nombres
        ==> "Avec % de signes" : signifie que les types de caracteres seront presents dans le mot de passe dans une quantite definie par l'user en pourcentage ; sauf si l'user choisit de creer un mot de passe uniquement avec des nombres
"""
class TabPassword:

    def __init__(self,tab_control,withPercent,pwdType):

        self.tab = ttk.Frame(tab_control)
        tab_control.add(self.tab, text='Password') #on ajoute l'onglet sur le tab control
        #==
        self.password=Password()
        #==
        self.label= Label(self.tab,text="Créer un password",fg="blue")
        self.label.grid(column=0, row=0, ipadx=5, pady=5, sticky=W+N)
        #========================================================
        self.sepColSpan=6
        self.sepIpadx=340
        #Séparateur 1
        self.sep1=Separator(self.tab, orient=HORIZONTAL).grid(row=1, column=0, columnspan=self.sepColSpan,ipadx=self.sepIpadx)
        #========================================================
        self.labelLgthPwd= Label(self.tab,text="Longueur du password : ")
        self.labelLgthPwd.grid(column=0, row=2, ipadx=5, pady=5, sticky=W)
        #==
        self.entryLgthPwd = Entry(self.tab, bd=3)
        self.entryLgthPwd.insert(0,12) #12 pour 12 caracteres de longueur par défaut
        self.entryLgthPwd.bind('<Button>', self.cleanFromEntry)
        self.entryLgthPwd.grid(column=1, row=2, ipadx=5, pady=5, sticky=W)
        #Séparateur 1
        self.sep2=Separator(self.tab, orient=HORIZONTAL).grid(row=3, column=0, columnspan=self.sepColSpan,ipadx=self.sepIpadx)
        #========================================================
        #==radioButtons
        self.withPercent=withPercent
        self.rbOff = Radiobutton(self.tab, text='Sans % de signes',variable=self.withPercent, value=0,command=self.clean) #sans % : valeur par défaut
        self.rbOn = Radiobutton(self.tab, text='Avec % de signes',variable=self.withPercent, value=1,command=self.clean) #avec %
        # =
        self.rbOff.grid(column=0, row=4, ipadx=5, pady=5, sticky=W)
        self.rbOn.grid(column=0, row=5, ipadx=5, pady=5, sticky=W)
        #=============================================
        self.dialog=CustomDialog() #fenêtre de dialogue pour renseigner les %
        #=============================================
        self.pwdType = pwdType
        self.rbOnlyNumbers = Radiobutton(self.tab, text='Avec seulement des nombres',variable=self.pwdType, value=0,command=self.clean) #valeur par défaut
        self.rbNumbersLetterMin = Radiobutton(self.tab, text='Avec des nombres et des lettres min',variable=self.pwdType, value=1,command=self.clean)
        self.rbNumbersLetterMinMaj = Radiobutton(self.tab, text='Avec des nombres et des lettres min/maj',variable=self.pwdType, value=2,command=self.clean)
        self.rbAllSigns = Radiobutton(self.tab, text='Avec nombres, lettres et caractères spéciaux',variable=self.pwdType, value=3,command=self.clean)
        #=
        self.rbOnlyNumbers.grid(column=1,row=4, ipadx=5, pady=5, sticky=W)
        self.rbNumbersLetterMin.grid(column=1,row=5, ipadx=5, pady=5, sticky=W)
        self.rbNumbersLetterMinMaj.grid(column=1, row=6, ipadx=5, pady=5, sticky=W)
        self.rbAllSigns.grid(column=1,row=7, ipadx=5, pady=5, sticky=W)
        #=======================
        self.buttonGenPwd=Button(self.tab,text="Générer password",command=lambda : self.genPwd())
        self.buttonGenPwd.grid(column=0, row=8, ipadx=5, pady=5, sticky=W)
        #==
        self.entryResultPwd = Entry(self.tab, bd=3)
        self.entryResultPwd.grid(column=1, row=8, ipadx=5, pady=5, sticky=W)
        # =====================================================================================

    #generer un mot de passe
    def genPwd(self):
        self.entryResultPwd.delete(first=0,last=len(self.entryResultPwd.get()))
        length=self.entryLgthPwd.get()
        if(len(length)>0 and length.isnumeric()):
            length=int(length)
            withPercent=self.withPercent.get()
            pwdType=self.pwdType.get()
            #==================================
            pwd=""
            # combinaison non possible : 100% avec des chiffres ==> couple (1,0)
            if(withPercent==1 and pwdType==0):
                messagebox.showwarning("Attention", "Pas de % autre que 100% un password uniquement composé de nombres")
            else:
                #avec % :
                if(withPercent==1): #recuperation des % renseignes par l'user
                    self.dialog.create("% par type")
                    if (pwdType == 1): #recuperation de 2 pourcentages
                        self.dialog.addEntries(["% de nombres :", "% de lettres :"],self.entryResultPwd,length,1)
                    elif (pwdType == 2): #recuperation de 3 pourcentages
                        self.dialog.addEntries(["% de nombres :", "% de minuscules :","% de majuscules :"], self.entryResultPwd, length, 2)
                    else: #recuperation de 4 pourcentages
                        self.dialog.addEntries(["% de nombres :", "% de minuscules :","% de majuscules :","% de caractères spéciaux"], self.entryResultPwd, length, 3)
                    self.dialog.launch()
                #sans % :
                else:
                    if(pwdType==0):
                        pwd=self.password.onlyNumbers(length)
                    elif(pwdType==1):
                        pwd=self.password.numbersAndLetters(length)
                    elif(pwdType==2):
                        pwd=self.password.numbersAndAllLetters(length)
                    else:
                        pwd=self.password.allSigns(length)
                #affichage du mot de passe dans une entree pour que l'user puisse le copier :
                try:
                    self.entryResultPwd.insert(0,pwd)
                except TclError:  # quand on ferme le programme après avoir ouvert la fenêtre de dialogue
                    pass
        else:
            messagebox.showwarning("Attention", "Il faut renseigner une longueur en nombre entier (sans virgule)")

    # retire la fenêtre de dialogue des % si déjà affichée, quand on touche aux radiobuttons et à l'entrée length du password
    def clean(self):
        if self.dialog is not None:
            try:
                if(self.dialog.getIsLaunched()):
                    self.dialog.stop()
            except TclError: #quand on clique sur un radiobutton après avoir ferme la fenêtre de dialogue ; "erreur" transparente/invisible pour l'user
                pass

    # appelée par l'entrée length du password ; cmd spécifique bis en bind qui doit prendre event en paramètre ; appelle clean()
    def cleanFromEntry(self,event):
        self.clean()