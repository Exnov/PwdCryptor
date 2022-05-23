import pickle
import pandas as pd
from lib.libCryptor import FogData

"""
Contient :
- des variables, objets qui circulent d'un onglet à un autre
- la classe Commun() qui regroupe des méthodes appelées dans plusieurs onglets
"""

#VARIABLES ET OBJET
PUBLIC_KEY='' #contient la clef publique
PRIVATE_KEY='' #contient la clef privée
MNG_CRYPTOR=FogData(PUBLIC_KEY,PRIVATE_KEY) #objet FogData qui gere les operations de cryptage et decryptage avec le couple clef publique/clef privée
DATA='' #données chargées non cryptées
EDATA='' #données chargées cryptées

#CLASSE Commun() : classe pour des utilisations recurrentes à des endroits différents du programme
class Commun:

    # lecture de fichier bytes, en parametre le nom du fichier à lire ; renvoie la clef // AUSSI dans classe FogData() dans libCryptor.py
    def readB(self,nameFile):
        with open(nameFile, 'rb') as f:
            data = pickle.load(f)
            return data

    # ecriture de fichier bytes, en parametres le nom du fichier à écrire, et la string a écrire dessus // AUSSI dans classe FogData() dans libCryptor.py
    def writeB(self,nameFile, data):
        with open(nameFile, 'wb') as f:
            pickle.dump(data, f)

    #ecriture des données décryptées dans un fichier CSV:
    def writeCSV(self,nameFile,data): #nameFile est un str du path avec le nom du fichier, et data est un dico
        df = pd.DataFrame(data)
        df.to_csv(nameFile,index=False)