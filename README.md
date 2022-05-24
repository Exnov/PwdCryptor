# PwdCryptor
PwdCryptor est un programme en interface graphique pour crypter ses identifiants et ses mots de passe. Il fait aussi générateur de mots de passe.

## Version information

#### Version 1.0

## Comment ça marche ?

### Préalable :
- Les  identifiants et mots de passe à crypter doivent être enregistrés dans un fichier CSV que vous devez créer de la façon suivante : 
	- Mettre dans une première colonne vos identifiants, et réserver la 1ère cellule de cette colonne pour écrire "identifiants" (c'est la clef d'un dictionnaire python appelée par le programme)
	- Mettre dans une seconde colonne vos mots de passe, et réserver la 1ère cellule de cette colonne pour écrire "passwords" (c'est l'autre clef d'un dictionnaire python appelée par le programme)
		- Petite précision : mettez à côté de chaque identifiant, le mot de passe qui correspond.
- Autre condition pour crypter, et décrypter les données avec le programme, vous devez générer avec le programme un couple de clefs publique/privée. On utilise le chiffrement RSA. Une fois créées, ces clefs doivent être chargées dans le programme pour crypter et décrypter des données. Ces opérations de création et de chargement de clefs se passent dans l'onglet "Clefs".

### Pour crypter :
- RAPPEL : chargez d'abord vos clefs (publique et privée) dans le programme.
- Allez dans l'onglet "Cryptage", ouvrez votre fichier CSV et enregistrez un nouveau fichier qui contiendra vos données cryptées. 
- Toujours dans l'onglet "Cryptage", vous pouvez modifier directement votre fichier de données cryptées, en ajoutant un nouvel identifiant et son mot de passe, mettre à jour un mot de passe, ou encore supprimer un identifiant, et son mot de passe.

### Pour décrypter : 
- RAPPEL : chargez d'abord vos clefs (publique et privée) dans le programme. Le programme ne décrypte que les données d'un fichier qu'il a cryptées.
- Allez dans l'onglet "Decryptage", ouvrez votre fichier crypté, et affichez les données décryptées dans une liste déroulante, ou exportez-les dans un fichier CSV.

### Pour générer un mot de passe :
- Le dernier onglet vous propose de générer des mots de passe. Pas besoin là-bas de charger des clefs ou d'ouvrir un fichier.
- Conditions de création d'un mot de passe :
    - précisez la longueur du mot de passe, exprimée en nombre de caractères
	- choisissez les types de caractères (nombres, lettres, caractères spéciaux) qui composeront le mot de passe  : 4 combinaisons possibles :
		- avec seulement des chiffres
		- avec des chiffres et des lettres minuscules
		- avec des chiffres, des lettres minuscules et majuscules
		- avec des chiffres, des lettres minuscules, majuscules, et des caractères spéciaux
    - choisissez entre "Sans % de signes" et "Avec des % de signes" : ça ne change rien dans le cas où vous choisissez de créer un mot de passe avec uniquement des nombres
		- "Sans % de signes" : signifie que les types de caractères seront présents dans le mot de passe en quantité aléatoire ; sauf si vous choisissez de créer un mot de passe uniquement avec des nombres (100% forcément)
		- "Avec % de signes" : signifie que les types de caractères seront présents dans le mot de passe dans une quantité définie que vous indiquez en pourcentage ; sauf si vous choisissez de créer un mot de passe uniquement avec des nombres (100% forcément)

## Environnement d'utilisation :
- Dans l'IDE Pycharm. vous créez un nouveau projet, téléchargez les dossiers et fichiers de PwdCryptor depuis GitHub, puis PyCharm s'occupera d'importer pour vous les packages (comme pandas ou rsa) dans l'environnement virtuel du projet.
- Dans un dossier sur votre PC, téléchargez les dossiers et fichiers de PwdCryptor depuis GitHub, puis vous appelez en ligne de commandes le fichier "main.py". Il faudra au préalable que vous ayez installé sur votre PC les packages nécessaires à l'exécution du programme (comme pandas ou rsa).
- En créant un exécutable du programme. Pour ça, vous téléchargez les fichiers et dossiers de PwdCryptor depuis GitHub dans un dossier sur votre PC. Vous devrez avoir sur votre PC les packages nécessaires à l'exécution du programme (comme pandas ou rsa). Vous devrez avoir aussi le package pyinstaller, qui va vous permettre de créer l'exécutable. Une fois ces conditions remplies, allez avec votre invite de commandes dans le dossier de PwdCryptor qui contient le fichier "main.py", et tapez la commande suivante :
```
pyinstaller --onefile main.py
```
Et récupérez l’exécutable dans le dossier "dist".

Libre à vous ensuite de vous approprier le programme et son code comme bon vous semble ;)
