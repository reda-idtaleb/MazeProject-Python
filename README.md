# Le mode de fonctionnement

- Le programme consiste généralement à créer des labyrinthes au format txt, trouver la solution de chaque labyrinthe crée, et à lire les fichiers text dont leurs contenus sont des labyrinthes, puis l'affichage de ses résolutions.

- dès que vous lancez le programme, vous serez ramener à entrer le nom de votre fichier, la largeur, et la longueur du labyrinthe:
   * Le fichier text sera créer automatiquement après la saisie du nom de votre choix, on rapelle que l'extension doit être forcément (.txt).  
   * La destination du fichier crée sera initialement dans le même dossier du projet. Selon votre désire, vous pouvez le placer dans n'importe quel emplacement dans votre pc.
   * Pour Réussir à créer le labyrinthe qui sera afficher dans votre fichier, vous devrez d'abord choisir la taille (largueur et longueur) de votre labyrinthe.
   * dès que votre labyrinthe est créer, vous pouvez le consulter sur votre dossier, puis vous marquerez un labyrinthe qui est dessiné selon la taille choisit, ainsi sa solution qui apparait en bas du text.

- pour l'utilisation des méthodes du projet, vous devrez avant tous créer sur le shell du thonny ou sur le terminal une variable qui construit le labyrinthe:
   * exemple: 
   ```bash
   >>> maze = Labyrinthe(4,4)
   ```
après par la suite vous pouvez utiliser les méthodes sans problèmes.

- pour la génération d'un labyrinthe enutilisant la méthode asociée, c'est la méthode " generate_maze":
   * exemple: 
   ```bash
    >>> maze = Labyrinthe(5,4)
    >>> maze.generate_maze()
   ```
- pour l'affichage du chemin vous pouvez utiliser la méthode "find_a_way":
   * exemple: 
   ```bash
   >>> maze = Labyrinthe(5,4)
   >>> maze.generate_maze() 
   >>> maze.find_a_way()
   ```
- Ainsi, vous pouvez tester les autres méthodes qui exitent sur le fichier "cellule.py", généralement c'est un module qui crée une seule cellule d'un labyrinthe.

- généralement tous les fonctions bien, sauf la fonction "lire_fichier" qui va lire chaques fichiers et trouve leurs solutions.
