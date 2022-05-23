import random as rd
import numpy as np

"""
Classe pour créer des mots de passe dans l'onglet Password si l'user veut qu'on lui trouve un password dans l'onglet Cryptage
"""
class Password:

    def __init__(self):
        self.numbers=["1","2","3","4","5","6","7","8","9","0"]
        self.letters=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        self.lettersCapital=self.capital()
        self.speSigns=["?",",",".",";","/",":","!",">","<","&","é","#","{","'","(","[","-","|","è","_","ç","^","à","@",")","]","=","}","¨","€","$","ù","%"]


    #pour mettre les lettres en majuscule et remplir la liste de la propriete self.lettersCapital
    def capital(self):
        lettersCapital=[]
        for letter in self.letters:
            lettersCapital.append(letter.upper())
        return lettersCapital

    # ====================================================================================================
    #GESTION DES % DE SIGNES DANS LA CREATION DE PASSWORD : ==============================================

    #renvoie une liste correspondant au % d'elements d'une liste de signes que le user veut avoir dans son password : ex:50% de lettres et 50% de chiffres
    def applyPercent(self,arr,percent,n): #n est la taille en caracteres, du password à creer
        #ex: n est égale à 16 : le mtp fera 16 elements
        nElts=len(arr) #ex nElts=10 pour 10 elements dans la liste de signes
        #percent: ex 0.4 pour 40% ==> on veut que 40% des 16 elts de notre password soient composés de lettres soit 16*0.4=6.4 ==> pas rond alors on arrondit au chiffre le plus pres
        #==> ex : x=round(6.4) ==> renvoie 6
        #il reste maintenant à selectionner aléatoirement 6 lettres dans l'array de lettres
        nEltstoKeep=round(n*percent)
        #on cree une liste aléatoire de 6 nombres, qui seront les index des lettres à retenir
        elts=[]
        for i in range(0,nEltstoKeep):
            index=rd.randint(0, nElts-1)
            selection=arr[index]
            elts.append(selection)
        return elts #on renvoie la portion de signes dans un array

    #pour verifier les % : regroupe les listes et renvoie le password produit par la methode getPwdPercent()
    def byPercent(self,percents,arrs,n):
        refs = []
        check = 0
        for p in percents:
            check += p
        #on verifie si le pourcentage fait 1 : sinon on applique des valeurs par défaut pour avoir une somme de % == 1
        if (check != 1):
            if(len(percents)==2): #si nombres et lettres
                percents = [0.5, 0.5]
            elif(len(percents)==3): # si nombres et lettres et majuscules
                percents = [0.6, 0.2,0.2]
            else: #si tous les caracteres
                percents = [0.4, 0.2, 0.2,0.2]
        for i in range(0, len(percents)):
            ref = []
            ref.append(percents[i])
            ref.append(arrs[i])
            refs.append(ref)
        return self.getPwdByPercent(n, refs)

    # renvoie un password où chaque liste est présent selon un %
    def getPwdByPercent(self, n,refs):  # n est la taille en caracteres du password à créer, et refs est un array d'arrays (qui contiennent chacun 2 elements : un % et l'array des caracteres associes à ce %)
        arrsRef = []  # pour la verification du nombre exacte d'elements en fin de methode
        # on recupere les portions de chaque liste qu'on veut : les elements de chaque portion sont selectionnes de façon aléatoire
        arrs = []
        for data in refs:
            percent=data[0]
            arr=data[1]
            portion = self.applyPercent(arr, percent, n)
            arrs.append(portion)
            arrsRef.append(arr)  # ==
        # on melange les arrays:
        mix = self.mix(arrs)
        # on verifie qu'on a le bon nombre d'elements (parce que le découpage en portions avec les pourcentages a pu ajouter ou retirer un element)
        diff = n - len(mix)
        if (diff > 0):  # si manque 1 element
            # on ajoute un element : choix aleatoire entre les 3 listes
            index = rd.randint(0, len(arrs) - 1)
            arrAlea = arrsRef[index]
            # choix aleatoire d'1 element dans cette liste
            index = rd.randint(0, len(arrAlea) - 1)
            newElt = arrAlea[index]
            # on ajoute simplement cet element à la liste du mot de passe à renvoyer
            mix.append(newElt)
            pass
        elif (diff < 0):  # si 1 element en trop
            # on supprime aleatoirement un element
            index = rd.randint(0, n - 1)
            mix.pop(index)

        return ''.join(mix) #on renvoie le password en string

    #gere la creation de password avec ou sans % de signes
    def getPwdMix(self,arrs,percents,n):
        if (percents):
            return self.byPercent(percents, arrs, n)
        else:
            mix = self.mix(arrs)
            pwd = ''.join(mix[0:n])
            return pwd

    #renvoie une liste mélangée aléatoirement de données de plusieurs listes
    def mix(self,arrs): #où arrs est un array des arrays des signes (nombres, lettres...) qu'on veut pour creer le mot de passe
        arrNps=[]
        for arr in arrs:
            arrNps.append((np.array(arr)))
        mix=np.concatenate(arrNps).tolist()
        rd.shuffle(mix)
        return mix

    # ====================================================================================================
    #CREATION DE PASSWORD SELON TYPES DE SIGNES VOULUS PAR L'USER ========================================

    #un password avec juste avec des nombres
    def onlyNumbers(self,n): #n est la taille du password à créer
        numbers = []
        for i in range(0, n):
            number = rd.randint(0,9)
            numbers.append(str(number))
        return ''.join(numbers)

    #un mot de passe avec des nombres et des lettres (minuscules)
    def numbersAndLetters(self,n,percents=[]): #percents est un array qui contient 2 pourcentages : pour numbers et letters
        arrs = [self.numbers, self.letters]
        return self.getPwdMix(arrs,percents,n)

    #un mot de passe avec des nombres, des lettres (minuscules) et des majuscules
    def numbersAndAllLetters(self,n,percents=[]):
        arrs=[self.numbers,self.letters,self.lettersCapital]
        return self.getPwdMix(arrs,percents,n)

    #un mot de passe avec tous:
    def allSigns(self,n,percents=[]):
        arrs=[self.numbers,self.letters,self.lettersCapital,self.speSigns]
        return self.getPwdMix(arrs, percents, n)

#========================================================================================================


"""
#EXEMPLES d'utilisation
p=Password()

#SANS %
print("PWD SANS % :")
print("pwd avec juste des nombres : ")
pwd1=p.onlyNumbers(12)
print(pwd1)
print('++++++++++++++++')
print("pwd avec nombres et lettres :")
pwd2=p.numbersAndLetters(10)
print(pwd2)
print('++++++++++++++++')
print("pwds avec nombres et lettres et majuscules :")
pwd3=p.numbersAndAllLetters(10)
print(pwd3)
print('++++++++++++++++')
print("pwd avec tous les signes :")
pwd4=p.allSigns(10)
print(pwd4)
print("\n")
#AVEC %
print("PWD AVEC % :")
print("pwd avec nombres et lettres :")
pwd2P=p.numbersAndLetters(10,[0.5,0.5])
print(pwd2P)
print('++++++++++++++++')
print("pwds avec nombres et lettres et majuscules :")
pwd3P=p.numbersAndAllLetters(10,[0.4,0.2,0.2])
print(pwd3P)
print('++++++++++++++++')
print("pwd avec tous les signes :")
pwd4P=p.allSigns(14,[0.4,0.2,0.2,0.2])
print(pwd4P)
print('++++++++++++++++')
"""