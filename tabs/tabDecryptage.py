from tkinter import ttk, Button, W, N, messagebox, HORIZONTAL
from tkinter.ttk import Separator

from lib import commun
from lib.commun import MNG_CRYPTOR
from lib.customFileExplorer import CustomFileExplorer

"""
classe de l'onglet 3 "Decryptage" : 
sert à :
==> décrypter un fichier crypté par le programme pour afficher ses données dans le programme
==> décrypter un fichier crypté par le programme pour l'exporter dans un fichier CSV
PRECISIONS :
-Nécessite le chargement du couple clef publique/clef privée dans l'onglet 1 (Clefs)
-Modèle du fichier CSV : le fichier CSV à crypter sera composé de 2 colonnes :
    ==> la 1ere aura pour titre 'identifiants', et contiendra les identifiants (ex: email...)
    ==> la 2ème aura pour titre 'passwords', et contiendra les mots de passe associés aux identifiants
"""
class TabDecryptage:

    def __init__(self,tab_control):

        self.tab = ttk.Frame(tab_control)
        tab_control.add(self.tab, text='Decryptage') #on ajoute l'onglet sur le tab control
        #explorateur de fichiers :
        self.fileExplorer=CustomFileExplorer()
        #========================================================
        self.buttonOpenData=Button(self.tab,text="Decrypter un fichier",command=lambda :self.openData())
        self.buttonOpenData.grid(column=0, row=0, ipadx=5, pady=5, sticky=W+N)
        self.listeDeroulante = ttk.Combobox(self.tab, values=[],width=50)
        self.listeDeroulante.grid(column=1, row=0, ipadx=5, pady=5, sticky=W)
        #========================================================
        self.sepColSpan=6
        self.sepIpadx=340
        #Séparateur
        self.sep=Separator(self.tab, orient=HORIZONTAL).grid(row=1, column=0, columnspan=self.sepColSpan, ipadx=self.sepIpadx)
        #========================================================
        self.buttonCsvSave=Button(self.tab,text="Exporter les données décryptées dans un CSV",command=lambda :self.exportDataCsv())
        self.buttonCsvSave.grid(column=0, row=2, ipadx=5, pady=5, sticky=W)
        # ========================================================

    #on decrypte les données si la clef privée est chargée
    def openData(self):
        if (commun.PRIVATE_KEY):
            commun.EDATA = self.fileExplorer.openB()
            if(commun.EDATA!=None):
                try:
                    commun.DATA = MNG_CRYPTOR.decrypt(commun.EDATA)
                    idsToDisplay=[]
                    ids=commun.DATA["identifiants"]
                    pwds=commun.DATA["passwords"]
                    n=0
                    for id in ids:
                        idsToDisplay.append(str(n+1)+" : " + id + " : "+ pwds[n])
                        n+=1
                    self.listeDeroulante['values']=idsToDisplay
                    self.listeDeroulante.current(0)
                except :
                    msg="La clef privée ne correspond pas ou le fichier fourni n'est pas crypté"
                    messagebox.showinfo("Info", msg)
        else:
            msg="Pas de clef privée chargée dans le logiciel"
            messagebox.showinfo("Info", msg)

    #On exporte les données decryptées dans un CSV : si clef privée chargée
    def exportDataCsv(self):
        if (commun.PRIVATE_KEY):
            try:
                # recuperation du fichier crypté via fileExplorer
                commun.EDATA, filename = self.fileExplorer.openBandGetFilemane("Ouvrir fichier crypté")
                # decrypter données :
                commun.DATA = MNG_CRYPTOR.decrypt(commun.EDATA)
                #enregistrement des données décryptées
                self.fileExplorer.saveCSV(commun.DATA,"Fichier enregistré")
            except TypeError:
                pass
            except AttributeError:
                msg = "La clef privée ne correspond pas ou le fichier fourni n'est pas crypté"
                messagebox.showinfo("Info", msg)
        else:
            msg="Pas de clef privée chargée dans le logiciel"
            messagebox.showinfo("Info", msg)