from tkinter import filedialog, messagebox
from lib.commun import Commun

"""
Classe pour ouvrir des explorateurs personnalisés de fichiers, pour la recuperation de données de fichiers,
et l'écriture de données dans fichiers
"""
class CustomFileExplorer:

    def __init__(self):
        self.commun=Commun() #on utilise des méthodes de la classe Commun

    #ouverture de fichier CSV
    def openCSV(self):
        filetype = [('fichier CSV', '.csv')]
        filename = filedialog.askopenfilename(title="Ouvrir CSV",filetypes=filetype)
        if(len(filename)>0):
            return filename
        else:
            return None

    #pour ouvrir un fichier qui contient 1 ou des objets
    def openB(self,label_file_explorer="",t=""): #B dans openB pour byte
        filename = filedialog.askopenfilename(title=t)
        if (len(filename) > 0):
            data = self.commun.readB(filename)
            # message dans label pour l'user
            if(label_file_explorer):
                label_file_explorer.configure(text="Fichier ouvert : " + filename)
            return data
        else:
            return None

    #openB() avec un retour aussi du filename, et sans demande de label
    def openBandGetFilemane(self,t=""):
        filename = filedialog.askopenfilename(title=t)
        if (len(filename) > 0):
            data = self.commun.readB(filename)
            return [data,filename]
        else:
            return None

    #ouverture de plusieurs fichiers, pour la recuperation du couple clef publique/clef privée
    def openMultiB(self,label_file_explorer=""):
        filenames = filedialog.askopenfilenames()
        if (len(filenames) > 0):
            infos=""
            data=[]
            for filename in filenames:
                d = self.commun.readB(filename)
                data.append(d)
                infos=infos+filename + "\n"
            # message dans label pour l'user
            if(label_file_explorer):
                label_file_explorer.configure(text="Fichiers ouverts : \n" + infos)
            return data
        else:
            return None

    #pour enregistrer un fichier
    def save(self,label_file_explorer,data,msg=""):
        f = filedialog.asksaveasfile(mode='w')
        if f is None:  # asksaveasfile renvoie `None` quand clique sur "cancel" ==> sort de la méthode et ferme la fenêtre de dialogue
            return
        # enregistrement objet:
        self.commun.writeB(f.name, data)
        # message dans label pour l'user
        if(len(msg)>0):
            label_file_explorer.configure(text=msg)
        return f

    # pareil que save, mais sans demande de label, et message info via messagebox
    def saveMsgInfo(self,data,msg):
        f = filedialog.asksaveasfile(mode='w')
        if f is None:  # asksaveasfile renvoie `None` quand clique sur "cancel" ==> sort de la méthode et ferme la fenêtre de dialogue
            return
        self.commun.writeB(f.name, data)
        # message d'info
        messagebox.showinfo("Info", msg)

    #enregistrement fichier CSV
    def saveCSV(self,data,msg=""):
        filetype = [('fichier CSV', '.csv')]
        f = filedialog.asksaveasfile(mode='w',title="Enregistrer CSV",defaultextension=".csv", filetypes=filetype)
        if f is None:  # asksaveasfile renvoie `None` quand clique sur "cancel" ==> sort de la méthode et ferme la fenêtre de dialogue
            return
        # enregistrement dico
        self.commun.writeCSV(f.name,data)
        # message d'info
        if(msg):
            messagebox.showinfo("Info", msg)

    #pour enregistrer plusieurs fichiers ==> appelée dans le chargement des clefs en tab 1, "Clefs"
    def saveFiles(self, data,titles): #data est un array, titles est un array
        i=0
        filenames=[]
        for d in data:
            t="Enregistrer " + titles[i]
            f = filedialog.asksaveasfile(mode='w',title=t)
            if f is None:  # asksaveasfile renvoie `None` quand clique sur "cancel" ==> sort de la méthode et ferme la fenêtre de dialogue
                return
            i+=1
            self.commun.writeB(f.name, d)
            filenames.append(f.name)
        return filenames
