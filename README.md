# Selenium_Scraper

Ce projet contient des scripts pour le scraping de données à partir du site www.avito.ma.

## Fichiers

- `scraper.py`: Ce fichier contient les fonctions de scraping pour les offres d'emploi, les propriétés immobilières et les véhicules.
- `main.py`: Ce fichier contient le code principal pour exécuter le scraping avec des villes spécifiques.
- `scraper.log`: Ce fichier est un journal de log qui enregistre les informations de l'exécution du scraping.
- `config.json`: Ce fichier contient la configuration pour le scraping, y compris le chemin du pilote Chrome et les informations de connexion à la base de données MongoDB.

## Prérequis

Avant d'exécuter les scripts, assurez-vous d'installer les dépendances suivantes :

- Python 3.x
- Selenium
- pymongo

Vous pouvez installer les dépendances en exécutant la commande suivante :

```shell
pip install selenium pymongo
```


Assurez-vous également d'avoir téléchargé le pilote Chrome approprié et de spécifier le chemin du pilote dans le fichier `config.json`.

## Utilisation

1.  Assurez-vous d'avoir correctement configuré le fichier config.json avec les informations requises.
2.  Exécutez le script main.py à l'aide de la commande suivante :
```shell
python main.py
```
Le script récupérera les données des offres d'emploi, des propriétés immobilières et des véhicules pour les villes spécifiées dans le fichier main.py. Les données seront ensuite enregistrées dans une base de données MongoDB.

## Resultat

```JSON
// Voiture
  {
    _id: ObjectId("64723643c06bd5bf3f3836f3"),
    Category: 'Vehicle',
    Title: '3.7 ha titrés avec vue sur les collines',
    Price: '2226000',
    link: 'https://www.avito.ma/fr/autre_secteur/terrains_et_fermes/3_7_ha_titr%C3%A9s_avec_vue_sur_les_collines__52477058.htm',
    localisation: 'Benslimane, Autre secteur',
    image: 'https://content.avito.ma/images/10/10091676435.jpg',
    type: 'Terrains et fermes',
    platform: 'www.avito.ma'
  }

// Immo
  {
    _id: ObjectId("647237ef0f809fa16d0450c8"),
    Category: 'Property',
    Title: 'Appartement à Anoual sans vis à vis',
    Price: '1300000',
    link: 'https://www.avito.ma/fr/quartier_des_hopitaux/appartements/Appartement_%C3%A0_Anoual_sans_vis_%C3%A0_vis_52762041.htm',
    localisation: 'Casablanca, Quartier des Hôpitaux',
    image: 'https://content.avito.ma/images/10/10094912416.jpg',
    type: 'Appartements',
    platform: 'www.avito.ma'
  }

// Emploi
  {
    _id: ObjectId("647235bb414ba9df2467b4bd"),
    Category: 'Job',
    Title: "femme ménage/nounou/ marocaine. l'étranger",
    Price: 0,
    link: 'https://www.avito.ma/fr/souissi/femme_de_menage_nounou_chauffeurs/femme_m%C3%A9nage_nounou__marocaine__l_%C3%A9tranger__40325414.htm',

```
## Notes
- Assurez-vous d'avoir une connexion Internet active pendant l'exécution du scraping.
- Veuillez consulter le fichier de journal scraper.log pour suivre l'état et les éventuelles erreurs lors de l'exécution du scraping.
