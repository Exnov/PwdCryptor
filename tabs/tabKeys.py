from tkinter import ttk, Button, Label, W, N, HORIZONTAL, messagebox
from tkinter.ttk import Separator

from lib import commun
from lib.commun import MNG_CRYPTOR
from lib.customFileExplorer import CustomFileExplorer
from lib.libCryptor import Locksmith

"""
classe de l'onglet 1 "Clefs" :
sert à :
==> créer le couple clef publique/clef privée
==> charger le couple clef publique/clef privée
PRECISIONS :
-La clef publique est nécessaire pour crypter les données
-La clef privée est nécessaire pour décrypter les données
"""
class TabKeys:

    def __init__(self,tab_control):
        self.lockSmith=Locksmith()
        self.publicKey=""
        self.privateKey=""
        #==
        self.tab = ttk.Frame(tab_control)
        tab_control.add(self.tab, text='Clefs') #on ajoute l'onglet sur le tab control
        #explorateur de fichiers :
        self.fileExplorer=CustomFileExplorer()
        #========================================================
        self.buttonGenKeys=Button(self.tab,text="Créer des clefs",command=lambda : self.genKeys())
        self.buttonGenKeys.grid(column=0, row=0, ipadx=5, pady=5, sticky=W+N)
        #==
        self.labelGenKeys = Label(self.tab,text="",height=2,fg="blue")
        self.labelGenKeys.grid(column=1, row=0)
        #========================================================
        self.sepColSpan=6
        self.sepIpadx=340
        #Séparateur
        self.sep=Separator(self.tab, orient=HORIZONTAL).grid(row=1, column=0, columnspan=self.sepColSpan, ipadx=self.sepIpadx)
        #========================================================
        self.buttonOpenKeys=Button(self.tab,text="Charger des clefs",command=lambda : self.openKeys())
        self.buttonOpenKeys.grid(column=0, row=2, ipadx=5, pady=5, sticky=W)
        #==
        self.labelOpenKeys = Label(self.tab,text="",height=2,fg="blue")
        self.labelOpenKeys.grid(column=1, row=2)

    #on cree des clefs
    def genKeys(self):
        self.lockSmith.createKeys()
        commun.PUBLIC_KEY=self.lockSmith.getPublicKey()
        commun.PRIVATE_KEY = self.lockSmith.getPrivateKey()
        #==========
        filenames=self.fileExplorer.saveFiles([commun.PUBLIC_KEY,commun.PRIVATE_KEY],['clef publique','clef privée'])
        #messagebox :
        if(filenames):
            messagebox.showinfo("Info", "Clefs exportées")

    #on charge des clefs
    def openKeys(self):
        try:
            #explorer file
            filenames=self.fileExplorer.openMultiB()
            #si chargement de fichiers :
            if(filenames):
                #on verifie que ce sont bien des clefs en couple pour les charger dans notre objet MNG_CRYPTOR ; objet que se partagent nos onglets
                for k in filenames:
                    if(self.lockSmith.isPublicKey(k)):
                        commun.PUBLIC_KEY=k
                        MNG_CRYPTOR.setPublicKey(commun.PUBLIC_KEY)
                    if(self.lockSmith.isPrivateKey(k)):
                        commun.PRIVATE_KEY=k
                        MNG_CRYPTOR.setPrivateKey(commun.PRIVATE_KEY)
                if commun.PUBLIC_KEY and commun.PRIVATE_KEY and self.lockSmith.isSamePaire(commun.PUBLIC_KEY,commun.PRIVATE_KEY):
                    msg="Clefs chargées dans le logiciel"
                    self.labelOpenKeys.configure(text=msg)
                else:
                    msg="Impossible de charger les clefs"
                    messagebox.showinfo("Info", msg)
        except:
            msg = "Il faut charger 2 CLEFS : 1 PUBLIQUE ET 1 PRIVEE"
            messagebox.showinfo("Info", msg)
