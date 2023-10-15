Ce projet consiste à créer un site de partage de critiques littéraires :

- utilisation du framework Django,
- mise en place de gabarits partiels,  
- mise en place de filtres et de balises personnalisés,  
- mise en place d'un User (modèle d'utilisateur personnalisé),  
- utilisation d'une table intermédiaire pour une relation ManyToMany,  
- mise en place d'un système d'abonnement entre utilisateur.
Application du script
A partir du terminal, se placer dans le répertoire souhaité

1. Récupérer le repository GitHub et créer un environnement virtuel
Cloner le repository GitHub :
https://github.com/pemochamdev/OPC-PROJET9.git

Puis se placer dans le répertoire du projet :

cd OPC
Pour ma part, je travaille sous Ubuntu et avec l'IDE VSCode, la création d'un environnement virtuel se fait comme suis:

Depuis un terminal sous Linux ou Mac :

*Création d'un environnement virtuel
python3 -m venv env
*Activation d'un environnement virtuel
env/bin/activate

2. Ouvrir le site et le parcourir
Se placer dans le répertoire du projet Django :

cd P9
Lancer le script python :

python3 manage.py runserver
Ouvrir la page HTML et la parcourir

3. Détails de connexion des utilisateurs déjà inscrits
Quatre utilisateurs sont déjà inscrits et présents dans la base de données :

- un superuser : 
    * username : pemochamdev@gmail.com  
    * mot de passe : pmc  
    * abonné à : pemochamdev@gmail.com 
    * suiveurs :amissa@gmail.com


- un 1er utilisateur :  
    * username : pemochamdev@gmail.com
    * mot de passe : pmc
    * abonné à : néant
    * suiveurs :amissa@gmail.com ,  khalilou@gmail.com

- un 2e utilisateur :  
    * username : khalilou@gmail.com
    * mot de passe : pmc
    * abonné à : néant  
    * suiveurs : amissa@gmail.com 
