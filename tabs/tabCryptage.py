from tkinter import ttk, Button, Label, Entry, W, N, messagebox, HORIZONTAL
from tkinter.simpledialog import askstring
from tkinter.ttk import Separator

from lib import commun
from lib.commun import MNG_CRYPTOR
from lib.customFileExplorer import CustomFileExplorer

"""
classe de l'onglet 2 "Cryptage" : 
sert à :
==> à crypter un fichier CSV construit selon le modèle indiqué dans "PRECISIONS"
==> à ajouter de nouvelles données cryptées à un fichier déjà crypté par le programme
==> à modifier des données cryptées dans un fichier déjà crypté par le programme
==> à supprimer des données cryptées dans un fichier déjà crypté par le programme
PRECISIONS :
-Nécessite le chargement du couple clef publique/clef privée dans l'onglet 1 (Clefs)
-Modèle du fichier CSV : le fichier CSV à crypter doit être composé de 2 colonnes :
    ==> la 1ere a pour titre 'identifiants', et contient les identifiants (ex: monsieur_toc@gmail.com...)
    ==> la 2ème a pour titre 'passwords', et contient les mots de passe associés aux identifiants
"""
class TabCryptage:

    def __init__(self,tab_control):

        self.tab = ttk.Frame(tab_control)
        tab_control.add(self.tab, text='Cryptage') #on ajoute l'onglet sur le tab control
        #explorateur de fichiers :
        self.fileExplorer=CustomFileExplorer()
        #========================================================
        self.buttonCwCsv=Button(self.tab,text="Crypter données d'un fichier CSV",command=lambda :self.cwCsv())
        self.buttonCwCsv.grid(column=0, row=0, ipadx=5, pady=5, sticky=W+N)
        self.labelCwCsv = Label(self.tab,text="",fg="blue")
        self.labelCwCsv.grid(column=1, row=0, ipadx=5, pady=5, sticky=W)
        #========================================================
        self.sepColSpan=6
        self.sepIpadx=340
        #Séparateur 1
        self.sep1=Separator(self.tab, orient=HORIZONTAL).grid(row=1, column=0, columnspan=self.sepColSpan,ipadx=self.sepIpadx)
        #========================================================
        self.labelNewEntry = Label(self.tab, text="Ajouter une nouvelle entrée : ")
        self.labelNewEntry.grid(column=0, row=2, ipadx=5, pady=5, sticky=W)
        #==
        self.labelEntryNewId = Label(self.tab, text="Identifiant : ")
        self.labelEntryNewId.grid(column=1, row=2, ipadx=5, pady=5, sticky=W)
        self.entryNewId = Entry(self.tab, bd=5)
        self.entryNewId.grid(column=2, row=2, ipadx=5, pady=5, sticky=W)
        #==
        self.labelEntryNewPwd = Label(self.tab, text="Password : ")
        self.labelEntryNewPwd.grid(column=3, row=2, ipadx=5, pady=5, sticky=W)
        self.entryNewPwd = Entry(self.tab, bd=3)
        self.entryNewPwd.grid(column=4, row=2, ipadx=5, pady=5, sticky=W)
        #==
        self.buttonNewEntry=Button(self.tab,text="Enregistrer nouvelle entrée",command=lambda :self.modifyEdataFile("add"))
        self.buttonNewEntry.grid(column=0, row=4, ipadx=5, pady=5, sticky=W)
        #========================================================
        #Séparateur 2
        self.sep2=Separator(self.tab, orient=HORIZONTAL).grid(row=5, column=0, columnspan=self.sepColSpan,ipadx=self.sepIpadx)
        #========================================================
        self.buttonUpdateEntry=Button(self.tab,text="Modifier un password",command=lambda :self.modifyEdataFile("updatePwd"))
        self.buttonUpdateEntry.grid(column=0, row=6, ipadx=5, pady=5, sticky=W) #5
        self.listeDeroulanteUp = ttk.Combobox(self.tab)
        self.buttonModifyUp = Button(self.tab)
        self.buttonStopUp = Button(self.tab)
        #========================================================
        #Séparateur 3
        self.sep3=Separator(self.tab, orient=HORIZONTAL).grid(row=9, column=0, columnspan=self.sepColSpan,ipadx=self.sepIpadx)
        #========================================================
        self.buttonDelEntry=Button(self.tab,text="Supprimer une entrée",command=lambda :self.modifyEdataFile("deleteEntry"))
        self.buttonDelEntry.grid(column=0, row=10, ipadx=5, pady=5, sticky=W)
        self.listeDeroulanteDel = ttk.Combobox(self.tab)
        self.buttonModifyDel = Button(self.tab)
        self.buttonStopDel = Button(self.tab)
        # ========================================================

    def cwCsv(self): #ouverture, cryptage, et exportation du fichier crypté
        if (commun.PUBLIC_KEY):
            filename=self.fileExplorer.openCSV()
            if(filename!=None):
                try:
                    eData = MNG_CRYPTOR.cwDataCsv(filename)
                    # SELECTION DU DOSSIER D'EXPORTATION
                    f=self.fileExplorer.save(self.labelCwCsv, eData)
                    if f is not None:
                        # message d'info
                        msg = "Fichier crypté enregistré"
                        messagebox.showinfo("Info", msg)
                except KeyError:
                    msg = "Le fichier CSV fourni n'est pas construit pour être traité par le programme"
                    messagebox.showinfo("Info", msg)
        else:
            msg="Pas de clef publique chargée dans le logiciel"
            messagebox.showinfo("Info", msg)

    def modifyEdataFile(self,action): #commun à addNewEntry() et displayUpdatePwd() et displayDeleteEntry()
        #on verifie que les 2 clefs sont chargées
        if (commun.PUBLIC_KEY and commun.PRIVATE_KEY):
            if(action=="add"):
                try:
                    self.addNewEntry()
                except:
                    msg = "Le fichier fourni ne correspond aux clefs chargées"
                    messagebox.showinfo("Info", msg)
            else:
                # recuperation du fichier crypté via fileExplorer
                try:
                    commun.EDATA, filename = self.fileExplorer.openBandGetFilemane("Ouvrir fichier crypté")
                    if(action=="updatePwd"):
                        self.displayUpdatePwd(filename)
                    elif(action=="deleteEntry"):
                        self.displayDeleteEntry(filename)
                except TypeError:
                    pass
                except:
                    msg = "Le fichier fourni ne correspond aux clefs chargées"
                    messagebox.showinfo("Info", msg)
        else:
            msg="Charger des clefs dans le logiciel"
            messagebox.showinfo("Info", msg)

    #on ajoute une nouvelle entrée à crypter dans fichier crypté
    def addNewEntry(self):
        newId = self.entryNewId.get()
        newPwd = self.entryNewPwd.get()
        #on verifie que les 2 entrées à ajouter sont complétées
        if (newId and newPwd):
            #on efface de l'interface graphique le contenu dynamique update et delete :
            elts=[self.listeDeroulanteUp, self.buttonModifyUp, self.buttonStopUp,self.listeDeroulanteDel, self.buttonModifyDel, self.buttonStopDel]
            self.eraseElts(elts)
            # recuperation du fichier crypté via fileExplorer si fichier renseigné par l'user :
            try :
                commun.EDATA, filename = self.fileExplorer.openBandGetFilemane("Ouvrir fichier crypté")
                #=====================
                # ouverture du fichier et récupération des données cryptées du fichier dans un tuple de 2 arrays
                eIds, ePwds = MNG_CRYPTOR.getEdata(filename)
                # ================================================================================================
                # cryptage des nouvelles données et ajout dans les 2 arrays :
                eIds.append(MNG_CRYPTOR.eStr(newId))
                ePwds.append(MNG_CRYPTOR.eStr(newPwd))
                # enregistrement de la nouvelle entrée cryptée dans fichier
                MNG_CRYPTOR.writeB(filename, {'identifiants': eIds, 'passwords': ePwds})
                #=====================
                # on informe l'user
                msg = "Fichier " + filename + " mis à jour"
                messagebox.showinfo("Info", msg)
                # on vide les entrees concernees de l'interface graphique
                self.entryNewId.delete(first=0, last=len(self.entryNewId.get()))
                self.entryNewPwd.delete(first=0, last=len(self.entryNewPwd.get()))
            except TypeError:
                pass
        else:
            msg = "Indiquer un identifiant ET un password"
            messagebox.showinfo("Info", msg)

    #affichage des elements graphiques dynamiques pour modifier un password
    def displayUpdatePwd(self,filename):
        # ouverture du fichier et recuperation des données cryptées dans dico de données decryptees
        data = MNG_CRYPTOR.dData(filename)
        ids = data['identifiants']
        #on efface dans l'interface graphique les elements dynamiques de deleteEntry
        elts=[self.listeDeroulanteDel,self.buttonModifyDel,self.buttonStopDel]
        self.eraseElts(elts)
        # on complete les elements graphiques de updatePwd
        self.listeDeroulanteUp = ttk.Combobox(self.tab,values=ids)
        self.buttonModifyUp = Button(self.tab, text="Taper nouveau password", command=lambda: self.openDial(self.listeDeroulanteUp,ids,data))
        self.buttonStopUp = Button(self.tab, text="Fini", command=lambda: self.eraseElts([self.listeDeroulanteUp, self.buttonModifyUp, self.buttonStopUp]))
        # on affiche les elements graphiques de updatePwd
        self.listeDeroulanteUp.current(0)
        self.listeDeroulanteUp.grid(column=1, columnspan=2, row=6)
        self.buttonModifyUp.grid(column=3, columnspan=2, row=6)
        self.buttonStopUp.grid(column=5, row=6)

    """
    Fenêtre de dialogue pour displayUpdatePwd, et modifier un password :
    ==> on ajoute les boutons "Modifier password" (ouvre une fenêtre de dialogue) et "Annuler" (efface les RadioButtons)
    """
    def openDial(self, listeDeroulante, ids, data):
        id = listeDeroulante.get()
        index = ids.index(id)
        pwd = data['passwords'][index]
        newPwd = askstring("Nouveau password pour " + id, "Remplacer " + pwd + " par :")
        if (newPwd):
            # maj des pwds
            data['passwords'][index] = newPwd
            # cryptage des données
            eData = MNG_CRYPTOR.cwData(data)
            # enregistrement des données cryptées et message de confirmation
            self.fileExplorer.saveMsgInfo(eData, "Password modifié et fichier enregistré")

    #affichage des elements graphiques dynamiques pour supprimer une entrée
    def displayDeleteEntry(self,filename):
        # ouverture du fichier et recuperation des données cryptées dans dico de données decryptees
        data = MNG_CRYPTOR.dData(filename)
        ids = data['identifiants']
        #======
        #on efface les elements graphiques dynamiques de updatePwd
        elts=[self.listeDeroulanteUp,self.buttonModifyUp,self.buttonStopUp]
        self.eraseElts(elts)
        # on complete les elements graphiques de deleteEntry
        self.listeDeroulanteDel = ttk.Combobox(self.tab, values=ids)
        self.buttonModifyDel = Button(self.tab, text="Supprimer", command=lambda: self.deleteEntry(self.listeDeroulanteDel,ids,data))
        self.buttonStopDel = Button(self.tab, text="Fini", command=lambda: self.eraseElts([self.listeDeroulanteDel, self.buttonModifyDel, self.buttonStopDel]))
        # on affiche les elements graphiques de deleteEntry
        self.listeDeroulanteDel.current(0)
        self.listeDeroulanteDel.grid(column=1, columnspan=2, row=10)
        self.buttonModifyDel.grid(column=3, columnspan=2, row=10)
        self.buttonStopDel.grid(column=5, row=10)

    #on supprime une entrée; pour la méthode displayDeleteEntry()
    def deleteEntry(self,listeDeroulante,ids,data):
        # recuperation de l'index :
        id = listeDeroulante.get()
        index = ids.index(id)
        # suppression de l'entrée
        data['identifiants'].pop(index)
        data['passwords'].pop(index)
        # cryptage des données
        eData = MNG_CRYPTOR.cwData(data)
        # enregistrement des données cryptées et message de confirmation
        self.fileExplorer.saveMsgInfo(eData, "Entrée supprimé et fichier enregistré")
        # on maj l'affichage de la liste déroulante
        print(data['identifiants'])
        if(len(data['identifiants'])>0):
            listeDeroulante['values'] = data['identifiants']
            listeDeroulante.current(0)

    #on efface les elements graphiques dynamiques
    def eraseElts(self,elts): #elts est un array d'elts : button, radiobutton...
            for elt in elts:
                elt.destroy()