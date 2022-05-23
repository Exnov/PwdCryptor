import rsa
import pickle
import pandas as pd

"""
3 classes :
- Lockmith : pour creer le couple clef publique/clef privee : utilise la librairie rsa
- Cryptor : pour crypter/decrypter des données en utilisant le couple clef publique/clef privee
- FogData : enfant de Cryptor : classe Cryptor appliquée à notre modèle de données à crypter/decrypter, comme on les reprend dans le fichier decrypté de base :
    ==> 2 colonnes : la 1ère contient les identifiants et a pour titre "identifiants", la 2ème contient les passwords et a pour titre "passwords"
    ==> representation python de ces 2 colonnes en dictionnaire : qui contient donc... 2 elements : 
        ==> le 1er index est "identifiants" et sa valeur est un array de strings qui sont les identifiants
        ==> le 2eme index est "passwords" et sa valeur est un array de strings qui sont les passwords
"""

#creation de clefs, enregistrement dans fichier, et recuperation; locksmith pour serrurier
class Locksmith:

    def __init__(self):
        self.publicKey=''
        self.privateKey=''

    #creation de clefs
    def createKeys(self):  # renvoie un tuple avec en 1er la clef publique, et en 2eme la clef privée
        self.publicKey,self.privateKey= rsa.newkeys(512)

    #recuperations des clefs creees
    def getPublicKey(self):
        return self.publicKey

    def getPrivateKey(self):
        return self.privateKey

    #enregistrement d'une clef
    def writeKey(self,namefile,typeKey): #typeKey ==> str pour préciser si publicKey ou privateKey
        # ecriture de fichier bytes, en parametres le nom du fichier à écrire, et le string a écrire dessus
        key=''
        if(typeKey=='public'):
            key=self.publicKey
        if(typeKey=='private'):
            key=self.privateKey
        with open(namefile, 'wb') as f:
            pickle.dump(key, f)

    #lecture d'une clee contenue dans fichier, et assignation pour un getter
    def setKey(self,namefile,typeKey):
        key = ''
        # lecture de fichier bytes, en parametre le nom du fichier à lire ; renvoie la clef
        with open(namefile, 'rb') as f:
            key = pickle.load(f)
        if(typeKey=='public'):
            self.publicKey=key
        if(typeKey=='private'):
            self.privateKey=key

    def printKeys(self):
        print(f"publicKey : {self.publicKey}")
        print(f"privateKey : {self.privateKey}")

    def isPublicKey(self,obj):
        reponse=False
        if type(obj) is rsa.key.PublicKey:
            reponse=True
        return  reponse

    def isPrivateKey(self,obj):
        reponse=False
        if type(obj) is rsa.key.PrivateKey:
            reponse=True
        return  reponse

    #verifie si 2 cles appartiennent au même couple : renvoie un boolean
    def isSamePaire(self,publicKey,privateKey):
        limit = len(str(publicKey)) - 1
        refPublicKey = str(publicKey)[9:limit]
        refPrivateKey = str(privateKey)
        return refPublicKey in refPrivateKey

#=============================================================================================
class Cryptor:

    def __init__(self,publicKey,privateKey):
        self.publicKey=publicKey
        self.privateKey=privateKey

    def getPublicKey(self):
        return self.publicKey

    def getPrivateKey(self):
        return self.privateKey

    def setPublicKey(self,publicKey):
        self.publicKey=publicKey

    def setPrivateKey(self,privateKey):
        self.privateKey=privateKey

    #ENCRYPTAGE
    #crypter un str à partir d'une clef publique :
    def eStr(self,expression): #renvoie le str en crypté
        return rsa.encrypt(expression.encode(),self.publicKey)

    # crypter un array de str à partir d'une clef publique :
    def eArray(self,strs):  # strs pour un array de strs
        expressions = []
        for expression in strs:
            expressions.append(self.eStr(self.publicKey, expression))
        return expressions

    #DECRYPTAGE
    # decrypter un str (en fait sous la forme d'un byte) à partir d'une clef privee:
    def dStr(self, encExpression):  # renvoie le str decrypte
        return rsa.decrypt(encExpression, self.privateKey).decode()

    #decrypter un array de str cryptés à partir d'une clef privée:
    def dArray(self, encStrs):  # encStrs pour un array de strs cryptés
        expressions = []
        for enc in encStrs:
            expressions.append(self.dStr(self.privateKey, enc))
        return expressions


#=============================================================================================
class FogData(Cryptor):

    # ecriture de fichier en bytes, en parametres le nom du fichier à écrire, et la string a écrire dessus // AUSSI dans commun.py
    def writeB(self,nameFile, data):
        with open(nameFile, 'wb') as f:
            pickle.dump(data, f)

    # lecture de fichier en bytes, en parametre le nom du fichier à lire ; renvoie la clef // AUSSI dans commun.py
    def readB(self,nameFile):
        with open(nameFile, 'rb') as f:
            data = pickle.load(f)
            return data

    #encrypte les données et les renvoie
    def cwData(self,data):
        identifiants=data['identifiants']
        passwords=data['passwords']
        eIds=[]
        ePwds=[]
        #cryptage des données recuperees dans 2 arrays distincts
        for id in identifiants:
            eIds.append(self.eStr(id))
        for pwd in passwords:
            ePwds.append(self.eStr(pwd))
        # ecriture du dictionnaire avec les données cryptées
        eData={'identifiants': eIds, 'passwords': ePwds}
        return eData

    #encrypte les données d'un fichier CSV
    def cwDataCsv(self,namefileCSV):
        # recuperation des donnees non cryptées du CSV sous forme de dataframe
        df = pd.read_csv(namefileCSV)
        return self.cwData(df)

    #ouvre le fichier qui contient les données cryptées et renvoie un tuple de 2 arrays
    def getEdata(self, nameFile):
        # ouverture du fichier et recuperation des données cryptées dans dico
        # recuperation des donnees cryptées du fichier
        eData = self.readB(nameFile)  # dico
        return (eData['identifiants'],eData['passwords'] )

    #decrypte le fichier crypté
    def dData(self,namefile):  # renvoie les données du fichier decrypte via un dico
        # recuperation des donnees cryptées du fichier
        eIds,ePwds=self.getEdata(namefile)
        identifiants = []  # array pour les identifiants decryptes
        pwds = []  # array pour les passwords decryptes
        # decryptage des données recuperees dans 2 arrays distincts
        for eId in eIds:
            identifiants.append(self.dStr(eId))
        for ePwd in ePwds:
            pwds.append(self.dStr(ePwd))
        # renvoie d'un dico avec les données decryptees
        return {'identifiants': identifiants, 'passwords': pwds}

    #Pareil que dData() sans le namefile à fournir
    def decrypt(self,eData):  # renvoie les données du fichier decrype via un dico
        # recuperation des donnees cryptées du fichier
        eIds=eData['identifiants']
        ePwds=eData['passwords']
        #==
        identifiants = []  # array pour les identifiants decryptes
        pwds = []  # array pour les passwords decryptes
        # decryptage des données recuperees dans 2 arrays distincts
        for eId in eIds:
            identifiants.append(self.dStr(eId))
        for ePwd in ePwds:
            pwds.append(self.dStr(ePwd))
        # renvoie d'un dico avec les données decryptees
        return {'identifiants': identifiants, 'passwords': pwds}

    #pour afficher les données d'un fichier
    def printData(self,namefile):
        data=self.readB(namefile)
        print(f"data :\n{data}")


