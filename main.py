
from tkinter import *
from tkinter import ttk
#== importation des classes des 4 onglets
from tabs.tabCryptage import TabCryptage
from tabs.tabDecryptage import TabDecryptage
from tabs.tabKeys import TabKeys
from tabs.tabPassword import TabPassword

#INTERFACE GRAPHIQUE :
window = Tk()
window.title("Crypteur et décrypteur d'identifiants et de passwords'")

tab_control = ttk.Notebook(window)
#==Les 4 onglets :
#onglet de clefs
TabKeys(tab_control)
#onglet de cryptage
TabCryptage(tab_control)
#onglet de decryptage
TabDecryptage(tab_control)
#onglet de creations de passwords
withPercent = IntVar()
withPercent.set(0)
pwdType = IntVar()
pwdType.set(0)
TabPassword(tab_control,withPercent,pwdType)
#===
tab_control.pack(expand=1, fill='both')

window.mainloop()