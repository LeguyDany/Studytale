import pygame
import random
from math import *
from pygame import mixer
import pickle

#Initialise le pygame, se doit de toujours etre la
pygame.init()

#Creer l'ecran
screen = pygame.display.set_mode((800,600)) #set_mode(X, Y), set la taille de X (= abscisses) et Y (=ordonnees)

#Changer le titre de la fenetre
pygame.display.set_caption("Studytale")

#Joueur, signification des indices des listes respectivement :
    # [0] Lvl (niveau)
    # [1] PV
    # [2] ATK / PRD
    # [3] DEF / DSC
    # [4] EXP
    # [5] Argent
    # [6] PV_Actuel
    # [7] ATK initial (sans boost)
    # [8] DEF initial (sans boost)
PNAME = str()

Player = {"stats":[1, 0, 0, 0, 0, 50, 0, 0, 0], "name": PNAME, "Math": 0, "Francais": 0, "Anglais": 0, "jour":1}

#Inventaire, signification des indices des listes respectivement :
    # [0] quantite
    # [1] type (1 = equipement | 2 = consommable | 3 = Consommable en combat seulement)
    # [2] effet(1 = restaure la concentration | 2 = Boost la PRD | 3 = Boost la DSC | 4 = Boost la PRD et DSC )
    # [3] intensite de l'effet
    # [4] actif(=1) ou pas(=0)
    # [5] Prix d'achat
    # [6] Prix de vente
Inventaire = {"Boisson Energisante" : [5, 2, 1, 10, 0, 25, 10], "Burger" : [3, 2, 1, 20, 0, 50, 20], "Bubble Tea" : [1, 2, 1, 50, 0, 75, 30], "Dessert au Chocolat" : [0, 2, 1, 100, 0, 100, 40], "Cafe" : [1, 3, 2, 20, 0, 100, 30], "The" : [1, 3, 3, 20, 0, 80, 25], "Stylo et feuilles" : [1, 1, 4, 0.1, 0, 66, 15], "Cahier" : [0, 1, 4, 0.2, 0, 250, 50], "Tablette" : [0, 1, 2, 0.4, 0, 500, 200],"PC" : [0, 1, 2, 0.5, 0, 1500, 500]}

#Definit l'inventaire du joueur une fois qu'on commence un nouveau jeu
Inventaire_Reset = {}
for key, value in Inventaire.items():
    Inventaire_Reset[key] = value

Ennemi = {}
def Enemy_Update():
    """Met a jour les statistiques des ennemis"""

    #Calcul de stats pour l'ennemi
    def ES(StatAverage):
        """ES = Enemy Stats | Permet d'ecrire plus facilement et de maniere plus compacte les stats des ennemis. || Calcul: StatMin = (StatAverage - StatAverage*0.25)*Day | StatMax = (StatAverage + StatAverage*0.25)*Day"""
        StatMin = ceil((StatAverage - StatAverage * 0.25)*Player["jour"])
        StatMax = ceil((StatAverage + StatAverage * 0.25)*Player["jour"])
        Val = random.randint(StatMin, StatMax)
    
        return Val

    #Ennemi, signification des indices des listes respectivement :
        # [0] Lvl (niveau)
        # [1] PV
        # [2] ATK
        # [3] DEF
        # [4] EXP
        # [5] Argent
        # [6] ID
        # [7] Type (0 = Aucun | 1 = Math | 2 = Francais | 3 = Anglais)

    Ennemi["Telephone"] = [ES(0.3), ES(0.3)+10, ES(0.3)+4, ES(0.3)+1, ES(1)+30, ES(0.5)+15, 1, 0]
    Ennemi["Facebook"] = [ES(0.225), ES(0.17)+8, ES(0.25)+5, ES(0.3)+1, ES(1)+34, ES(0.75)+20, 2, 0]
    Ennemi["Reddit"] = [ES(0.25), ES(0.3)+14, ES(0.3)+4, ES(0.3), ES(1)+40, ES(1)+25, 3, 0]
    Ennemi["Twitter"] = [ES(0.275), ES(0.35)+16, ES(0.35)+4, ES(0.3)+1, ES(1)+44, ES(1.25)+30, 4, 0]
    Ennemi["Console"] = [ES(0.3), ES(0.4)+18, ES(0.4)+4, ES(0.3)+1, ES(1)+50, ES(1.5)+35, 5, 0]
    Ennemi["Television"] = [ES(0.4), ES(0.45)+20, ES(0.45)+4, ES(0.3)+1, ES(1)+54, ES(1.75)+40, 6, 0]
    Ennemi["Controle de Math"] = [ES(0.6), ES(0.6)+30, ES(0.5)+5, ES(0.4)+2, ES(3)+60, ES(2)+50, 7, 1]
    Ennemi["Controle de Francais"] = [ES(0.6), ES(0.6)+30, ES(0.5)+5, ES(0.4)+2, ES(3)+60, ES(2)+50, 8, 2]
    Ennemi["Controle d'Anglais"] = [ES(0.6), ES(0.6)+30, ES(0.5)+5, ES(0.4)+2, ES(3)+60, ES(2)+50, 9, 3]
    Ennemi["Partiels"] = [15, 125, 10, 5, 0, 0, 10, 0]
    
#Les fonctions utilisees a plein d'endroits du codes
def Player_Update(LVL):
    """Update les statistiques du personnage, utilise lorsque notre personnage monte de niveau pour recalculer les statistiques."""

    #Joueur, signification des indices des listes respectivement :
        # [0] Lvl (niveau)
        # [1] PV
        # [2] ATK / PRD
        # [3] DEF / DSC
        # [4] EXP
        # [5] Argent
        # [6] PV_Actuel
        # [7] ATK initial (sans boost)
        # [8] DEF initial (sans boost)

    #On remet a jour les statistiques du personnage
    Player["stats"] = [LVL, ceil(LVL*5)+40, ceil(LVL*0.4)+5, ceil(LVL*0.15)+2, Player["stats"][4], Player["stats"][5], ceil(LVL*5)+40, ceil(LVL*0.5)+5, ceil(LVL*0.5)+2]

    #On prend en compte si le personnage equipe quelque chose ou pas
    for key, value in Inventaire.items():
        #Si on equipe quelque chose qui boost la productivite
        if value[1] == 1 and value[4] == 1 and value[2] == 2:
            Player["stats"][2] = Player["stats"][2] + ceil(Player["stats"][2]*value[3])
        #Si on equipe quelque chose qui boost la discipline et la productivite
        elif value[1] == 1 and value[4] == 1 and value[2] == 4:
            Player["stats"][3] = Player["stats"][3] + ceil(Player["stats"][3]*value[3])
            Player["stats"][2] = Player["stats"][2] + ceil(Player["stats"][2]*value[3])

def SFX(sound):
    """Permet de jouer les effets sonores. Arguments : error | badnote | navitage | select | bopen | damage | hurt | defense | item | buy | save"""

    #Lorsqu'on fait une action qui mene normalement a une erreur
    if sound == "error":
        error_sound = mixer.Sound("Assets/SFX/mus_rotate.wav")
        error_sound.play()
    #Lorsqu'on fait une action qui n'est pas permise par le jeu
    elif sound == "badnote":
        mus_badnote1 = mixer.Sound("Assets/SFX/mus_badnote1.wav")
        mus_badnote1.play()
    #Lorsqu'on navigue dans les menus
    elif sound == "navigate":
        mus_sfx_a_target = mixer.Sound("Assets/SFX/mus_sfx_a_target.wav")
        mus_sfx_a_target.play()
    #Lorsqu'on selectionne quelque chose dans le menu
    elif sound == "select":
        snd_select = mixer.Sound("Assets/SFX/snd_select.wav")
        snd_select.play()

    #Lorsque le combat s'ouvre
    elif sound == "bopen":
        x = random.randint(0, 100)
        if x < 50:
            snd_b = mixer.Sound("Assets/SFX/snd_b.wav")
            snd_b.play()
        else:
            snd_battlefall = mixer.Sound("Assets/SFX/snd_battlefall.wav")
            snd_battlefall.play()
    #Lorsqu'on attaque l'ennemi et que l'attaque reussie
    elif sound == "damage":
        snd_damage = mixer.Sound("Assets/SFX/snd_damage.wav")
        snd_damage.play()
    #Lorsqu'on se prend des degats
    elif sound == "hurt":
        snd_hurt1 = mixer.Sound("Assets/SFX/snd_hurt1.wav")
        snd_hurt1.play()
    #Lorsqu'on se defend
    elif sound == "defense":
        snd_block2 = mixer.Sound("Assets/SFX/snd_block2.wav")
        snd_block2.play()

    #Lorsqu'on utilise un objet
    elif sound == "item":
        snd_power = mixer.Sound("Assets/SFX/snd_power.wav")
        snd_power.play()
    #Lorsqu'on achete un objet
    elif sound == "buy":
        snd_buyitem = mixer.Sound("Assets/SFX/snd_buyitem.wav")
        snd_buyitem.play()
    #Lorsqu'on sauvegarde
    elif sound == "save":
        snd_save = mixer.Sound("Assets/SFX/snd_save.wav")
        snd_save.play()

def valider():
    """Fonction qui va attendre que le joueur valide ce qu'il voit en appuyant sur ESPACE."""

    valider = 0
    while valider == 0:
        #Gere les input du joueur
        for event in pygame.event.get():
            #Si on souhaite fermer le jeu
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Si la touche espace est pressee, le joueur valide et le combat passe a la phase suivante.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    valider += 1

def window_draw_rect(COLOR, ALPHA, PositionX, PositionY, Largeur, Hauteur):
    """Dessine un rectangle."""

    #Dessine le fond du rectangle
    s = pygame.Surface((Largeur, Hauteur), pygame.SRCALPHA)   # alpha par pixel
    s.fill((0,0,0,ALPHA))                                     # remarquez la valeur alpha dans les couleurs
    screen.blit(s, (PositionX,PositionY))

    #Dessine les bordures du rectangle
    Epaisseur = 5 #Pixels
    #Bordure Haute, Droite, Gauche, Basse
    BH = pygame.draw.rect(screen, COLOR, (PositionX, PositionY, Largeur, Epaisseur))
    BD = pygame.draw.rect(screen, COLOR, (PositionX + Largeur, PositionY, Epaisseur, Hauteur))
    BG = pygame.draw.rect(screen, COLOR, (PositionX, PositionY, Epaisseur, Hauteur))
    BB = pygame.draw.rect(screen, COLOR, (PositionX, PositionY + Hauteur, Largeur + Epaisseur, Epaisseur))

def afficher(texte, taille, couleur, position):
    """Permet d'afficher un text sur l'ecran"""

    #Police d'ecriture
    font = pygame.font.Font('Assets/pixelmix.ttf', taille)

    #Sous quelle forme va apparaitre le texte
    afficher = font.render(texte, True, couleur) 
    screen.blit(afficher, position)

def Couleurs():
        """Retourne les couleurs qu'on utilise, retourne dans l'ordre : blanc, orange, alpha"""
        WHITE = [255,255,255]
        ORANGE = [255,158,46]
        ALPHA = 170
        return WHITE, ORANGE, ALPHA

def BARREVIE(PVActuel, PVMAX, X, Y):
    """Dessiner une barre de vie"""

    #Coordonnees X et Y de la barre de vie
    X_Barre = X
    Y_Barre = Y

    #Dessiner la barre de vie de l'ennemi
    Pourcentage_vie = PVActuel / PVMAX
    pygame.draw.rect(screen, (255, 51, 51), (X_Barre, Y_Barre, 150, 15)) #Barre rouge
    pygame.draw.rect(screen, (28, 209, 41), (X_Barre, Y_Barre, Pourcentage_vie*150, 15)) #Barre verte

def Music(Song):
    """Permet de jouer une musique avec pour argument (en chaine de caractere): battle, nav, mag, start"""

    if Song == "battle": #Jouer la musique de combat
        battle = mixer.music.load('Assets/music/toby fox - UNDERTALE Soundtrack - 09 Enemy Approaching.mp3')
        battle = mixer.music.play(-1) #Permet de la jouer en boucle
    elif Song == "BossF": #Jouer la musique de combat
        battle = mixer.music.load('Assets/music/toby fox - UNDERTALE Soundtrack - 100 MEGALOVANIA.mp3')
        battle = mixer.music.play(-1) 
    elif Song == "nav": #Jouer la musique du menu de navigation
        nav = mixer.music.load('Assets/music/toby fox - UNDERTALE Soundtrack - 12 Home.mp3')
        nav = mixer.music.play(-1) 
    elif Song == "mag": #Jouer la musique du magasin
        nav = mixer.music.load('Assets/music/toby fox - UNDERTALE Soundtrack - 23 Shop.mp3')
        nav = mixer.music.play(-1) 
    elif Song == "start": #Jouer la musique du menu principal
        nav = mixer.music.load('Assets/music/toby fox - UNDERTALE Soundtrack - 02 Start Menu.mp3')
        nav = mixer.music.play(-1) 
    elif Song == "end": #Jouer le generique de fin
        nav = mixer.music.load('Assets/music/ending-theme-kirbys-dream-land.mp3')
        nav = mixer.music.play()
        pygame.time.wait(600)

def Sauvegarde():
    """Permet de sauvegarder l'avancee du jeu"""

    with open("Sauvegarde_Joueur","wb") as folder: # with: manipule un objet (fichier dans notre cas), ferme le fichier à la fin  |  as: "en tant que"
	# Nous allons chercher a sauvegarder les donnees de l'objet score dans un fichier.

        mon_pickler = pickle.Pickler(folder) # Operation qui sera execute
        mon_pickler.dump(Player)
    
    with open("Sauvegarde_Inventaire","wb") as folder: 

        mon_pickler = pickle.Pickler(folder) 
        mon_pickler.dump(Inventaire)

def Charger():
    """Permet de charger une sauvegarde. Retourne le dictionnaire du joueur et de l'inventaire respectivement."""

    try:
        with open("Sauvegarde_Joueur", "rb") as folder:
            # Nous allons chercher a acceder aux donnees presentes dans le fichier score.

            mon_depickler = pickle.Unpickler(folder) 
            load_score = mon_depickler.load()

        Sauvegarde_Player = load_score

        with open("Sauvegarde_Inventaire", "rb") as folder:
            # Nous allons chercher a acceder aux donnees presentes dans le fichier score.

            mon_depickler = pickle.Unpickler(folder) 
            load_score = mon_depickler.load()

        Sauvegarde_Inventaire = load_score

        for key, value in Sauvegarde_Player.items():
            Player[key] = value

        for key, value in Sauvegarde_Inventaire.items():
            Inventaire[key] = value
    
    #Si le jeu ne detecte aucune sauvegarde
    except FileNotFoundError:
        afficher("Aucune sauvegarde est detectee.", 20, [255,255,255], (165, 280))
        SFX("error")
        pygame.display.update() #Permet de update l'ecran
        valider()
        
        return 0
        
    with open("Sauvegarde_Joueur", "rb") as folder:
        # Nous allons chercher a acceder aux donnees presentes dans le fichier score.

        mon_depickler = pickle.Unpickler(folder) 
        load_score = mon_depickler.load()

    Sauvegarde_Joueur = load_score

    return Sauvegarde_Joueur, Sauvegarde_Inventaire

#Les grandes fonctions du jeu (menu principal, menu de navigation et combat)
def MainMenu(PNAME):
    """Le menu principal"""

    WHITE, ORANGE, ALPHA = Couleurs()
    ALPHA = 215

    # Background 
    background = pygame.image.load('Assets/Main_Menu/Img/FOND.jpg')

    #Permet de jouer la musique du menu
    Music("start")

    #Fonction qui permet de reinitialiser tout l'inventaire et les caracteristiques du joueur
    def Player_resetting():
        """Fonction qui permet de reinitialiser tout l'inventaire et les caracteristiques du joueur"""

        #Remet a l'etat d'origine l'inventaire du joueur
        for key, value in Inventaire_Reset.items():
            Inventaire[key] = value

        #Remet a 0 les carcteristiques et l'inventaire du joueur.
        Player_Update(1)
        Player["stats"][4] = 0
        Player["stats"][5] = 50
        Player["jour"] = 1
        Player["Math"] = 0
        Player["Francais"] = 0
        Player["Anglais"] = 0

        

        

    def Avancee000():
        """Phase idle du menu principal"""

        #Afficher le titre du jeu
        #Afficher les boutons Commencer, Charger, Aide, Quitter
        #Interaction, pouvoir naviguer entre les boutons et choisir

        #Position des rectangles du bas de l'ecran
        X_RecBas = 30
        Y_RecBas = 500

        choix = 1

        #La boucle de la fonction
        Menu_Run_Idle = True
        while Menu_Run_Idle == True: 

            #title_font = pygame.font.Font('Assets/pixelmix_bold.ttf', 100)
            #title_text = title_font.render("Studytale", True, (255, 255, 255))
            #screen.blit(title_text, (50, 80))
            screen.blit(background, (0, 0))
            afficher("Studytale", 100, WHITE, (X_RecBas+53, Y_RecBas-400))

            #Affiche les boutons commencer, charger, aide, quitter
            if choix == 1:
                #Rectangle commencer
                window_draw_rect(ORANGE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
                afficher("Commencer", 20, ORANGE, (X_RecBas+22, Y_RecBas+20))
                #Rectangle Charger
                window_draw_rect(WHITE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
                afficher("Charger", 20, WHITE, (X_RecBas+229, Y_RecBas+20))
                #Rectangle Aide
                window_draw_rect(WHITE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
                afficher("Aide", 20, WHITE, (X_RecBas+442, Y_RecBas+20))
                #Rectangle Quitter
                window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
                afficher("Quitter", 20, WHITE, (X_RecBas+611, Y_RecBas+20))
            elif choix == 2:
                #Rectangle commencer
                window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
                afficher("Commencer", 20, WHITE, (X_RecBas+22, Y_RecBas+20))
                #Rectangle Charger
                window_draw_rect(ORANGE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
                afficher("Charger", 20, ORANGE, (X_RecBas+229, Y_RecBas+20))
                #Rectangle Aide
                window_draw_rect(WHITE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
                afficher("Aide", 20, WHITE, (X_RecBas+442, Y_RecBas+20))
                #Rectangle Quitter
                window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
                afficher("Quitter", 20, WHITE, (X_RecBas+611, Y_RecBas+20))
            elif choix == 3:
                #Rectangle commencer
                window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
                afficher("Commencer", 20, WHITE, (X_RecBas+22, Y_RecBas+20))
                #Rectangle Charger
                window_draw_rect(WHITE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
                afficher("Charger", 20, WHITE, (X_RecBas+229, Y_RecBas+20))
                #Rectangle Aide
                window_draw_rect(ORANGE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
                afficher("Aide", 20, ORANGE, (X_RecBas+442, Y_RecBas+20))
                #Rectangle Quitter
                window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
                afficher("Quitter", 20, WHITE, (X_RecBas+611, Y_RecBas+20))
            elif choix == 4:
                #Rectangle commencer
                window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
                afficher("Commencer", 20, WHITE, (X_RecBas+22, Y_RecBas+20))
                #Rectangle Charger
                window_draw_rect(WHITE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
                afficher("Charger", 20, WHITE, (X_RecBas+229, Y_RecBas+20))
                #Rectangle Aide
                window_draw_rect(WHITE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
                afficher("Aide", 20, WHITE, (X_RecBas+442, Y_RecBas+20))
                #Rectangle Quitter
                window_draw_rect(ORANGE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
                afficher("Quitter", 20, ORANGE, (X_RecBas+611, Y_RecBas+20))

            for event in pygame.event.get():
                #Si on souhaite fermer le jeu
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # Si une touche est pressee, on se deplace dans le menu
                if event.type == pygame.KEYDOWN:
                    #Permet de se deplacer dans le menu
                    if event.key == pygame.K_LEFT:
                        choix -= 1
                        SFX("navigate")
                    if event.key == pygame.K_RIGHT:
                        choix += 1
                        SFX("navigate")
                    
                    #Permet de selectionner ce que l'on veut dans le menu
                    if event.key == pygame.K_SPACE:
                        #Si on selectionne le bouton commencer
                        if choix == 1:
                            SFX("select")
                            return 11
                        #Si on selectionne le bouton Charger
                        elif choix == 2:
                            SFX("select")
                            return 12
                        #Si on selectionne le bouton Aide
                        elif choix == 3:
                            SFX("select")
                            screen.blit(background, (0,0))
                            #Rectangle commencer
                            window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
                            afficher("Commencer", 20, WHITE, (X_RecBas+22, Y_RecBas+20))
                            #Rectangle Charger
                            window_draw_rect(WHITE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
                            afficher("Charger", 20, WHITE, (X_RecBas+229, Y_RecBas+20))
                            #Rectangle Aide
                            window_draw_rect(ORANGE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
                            afficher("Aide", 20, ORANGE, (X_RecBas+442, Y_RecBas+20))
                            #Rectangle Quitter
                            window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
                            afficher("Quitter", 20, WHITE, (X_RecBas+611, Y_RecBas+20))
                            
                            window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas-450, 738, 430)
                            
                            afficher("Le jeu se joue entierement avec les touches directionnelles ", 17, WHITE, (X_RecBas+17, Y_RecBas-415))
                            afficher("(se deplacer) et la barre ESPACE (valider)", 17, WHITE, (X_RecBas+17, Y_RecBas-385))
                            
                            
                            afficher("Math/Francais/Anglais : Bonus de degats vs. les ennemis de", 17, WHITE, (X_RecBas+17, Y_RecBas-315))
                            afficher("la matiere en question selon votre niveau dans la matiere.", 17, WHITE, (X_RecBas+17, Y_RecBas-285))

                            afficher("Objectif : Travailler en combattant ses distractions pour", 17, WHITE, (X_RecBas+17, Y_RecBas-225))
                            afficher("reussir son annee.", 17, WHITE, (X_RecBas+20, Y_RecBas-195))

                            afficher("Productivite (PRD) = Vos degats", 18, WHITE, (X_RecBas+17, Y_RecBas-135))
                            afficher("Discipline (DSC) = Votre defense", 18, WHITE, (X_RecBas+17, Y_RecBas-105))
                            afficher("Concentration (CON) = Votre sante", 18, WHITE, (X_RecBas+17, Y_RecBas-75))

                            pygame.display.update()
                            valider()
                            SFX("select")
                            return 0
                        #Si on selectionne le bouton Quitte
                        else:
                            pygame.quit()
                            exit()

            if choix < 1 :
                choix = 1
            elif choix > 4 :
                choix = 4

            pygame.display.update() #Permet de update l'ecran

    def Avancee111(PNAME):
        """Permet de nommer le personage. Retourne le nom du personnage."""

        def ordre():
            """Retourne une lettre de l'alphabet en fonction de ce que l'on tappe"""

            if event.key == pygame.K_a:
                return "A"
            elif event.key == pygame.K_b:
                return "B"
            elif event.key == pygame.K_c:
                return "C"
            elif event.key == pygame.K_d:
                return "D"
            elif event.key == pygame.K_e:
                return "E"
            elif event.key == pygame.K_f:
                return "F"
            elif event.key == pygame.K_g:
                return "G"
            elif event.key == pygame.K_h:
                return "H"
            elif event.key == pygame.K_i:
                return "I"
            elif event.key == pygame.K_j:
                return "J"
            elif event.key == pygame.K_k:
                return "K"
            elif event.key == pygame.K_l:
                return "L"
            elif event.key == pygame.K_m:
                return "M"
            elif event.key == pygame.K_n:
                return "N"
            elif event.key == pygame.K_o:
                return "O"
            elif event.key == pygame.K_p:
                return "P"
            elif event.key == pygame.K_q:
                return "Q"
            elif event.key == pygame.K_r:
                return "R"
            elif event.key == pygame.K_s:
                return "S"
            elif event.key == pygame.K_t:
                return "T"
            elif event.key == pygame.K_u:
                return "U"
            elif event.key == pygame.K_v:
                return "V"
            elif event.key == pygame.K_w:
                return "W"
            elif event.key == pygame.K_x:
                return "X"
            elif event.key == pygame.K_y:
                return "Y"
            elif event.key == pygame.K_z:
                return "Z"
            elif event.key == pygame.K_BACKSPACE:
                return "BACKSPACE"
            elif event.key == pygame.K_RETURN:
                return "ENTER"
            
        PNAME = str()
        lettre = str()
        text = "Veuillez entrer votre nom"
        textx = 220

        naming_run = True
        while naming_run == True:

            #Affiche le backgound et le rectangle ou on rentre le nom du personnage
            screen.blit(background, (0,0))
            window_draw_rect(WHITE, ALPHA, 340, 330, 120, 60)
            afficher("_______", 23, WHITE, (352, 360))
            afficher("{}".format(PNAME), 20, ORANGE, (352, 354))
            afficher(text, 20, WHITE, (textx, 280))


            #Gere les inputs du joueur
            for event in pygame.event.get():
                #Lorsqu'on clique sur fermer la fenetre
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Si une lettre de l'alphabet est pressee, fait apparaitre la lettre au dessus des tirets du 8. Si on appuie sur effacer, ca enleve une lettre
                if event.type == pygame.KEYDOWN:

                    #On va choisir quelle lettre on veut tapper avec la fonction ordre()
                    lettre = str(ordre())
                    #Si on appuie sur la touche effacer
                    if lettre == "BACKSPACE" and len(PNAME)>0:
                        #On va effacer l'ensemble des lettres presents dans la variable lettre
                        for char in lettre: 
                            lettre = lettre.replace(char, '')
                        #On va effacer la derniere lettre de la variable PNAME
                        for char in PNAME[len(PNAME)-1]:
                            PNAME = PNAME[:len(PNAME)-1]
                    #Si on n'a pas un nom de plus de 7 lettres
                    elif len(PNAME) < 7 and lettre in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                        #On concataine a PNAME la nouvelle lettre qu'on a choisie
                        PNAME += lettre
                        #On efface la lettre qu'on a choisie pour pouvoir choisir une nouvelle lettre
                        for char in lettre: 
                            lettre.replace(char, '')
                    elif lettre == "ENTER":
                        if len(PNAME) < 3:
                            text = "Veuillez selectionner un nom plus long"
                            SFX("badnote")
                            textx = 130
                        if len(PNAME) >= 3:
                            SFX("select")
                            return 1, PNAME

            pygame.display.update() #Permet de update l'ecran

    #Avancee
        #Avancee = 0 => Phase idle du menu. On va choisir parmi les differents boutons
        #Avancee = 1 => Phase commencer le jeu
        #Avancee = 2 => Phase Charger
        #Avancee = 3 => Phase aide
        #Avancee = 11 => Conclusion pour lancer le jeu
        #Avancee = 12 => Conclusion pour charger la sauvegarde
    Avancee = 0

    #Boucle de la fonction MainMenu
    Main_Menu_Run = True
    while Main_Menu_Run == True :
        
        if Avancee == 0: #Si on se trouve dans la phase idle
            Avancee = Avancee000()
        elif Avancee == 11: #Si on commence le jeu et rentre dans le menu pour nommer le personnage
            Player_resetting()
            Avancee, PNAME = Avancee111(PNAME)
            return PNAME
        elif Avancee == 12: #Si on charge une sauvegarde
            Avancee = Charger()
            if Avancee == 0:
                continue
            else: 
                return Player["name"]
            
def battle(Ennemi, Joueur):
    """Fonction qui gere les combats dans le jeu. Retourne 1(gagne), 2(perd), 3(fuite) ou 4(ferme le jeu) en 1ere valeur. Puis, 
    retourneV_Actuel, PEXP et PARGENT. | Exemple d'usage : battle(Ennemi["telephone"], Joueur)"""

    Music("battle")

    #background du combat
    background = pygame.image.load('Assets/battle/battle_background.jpg') #Provient de freepik.com

    #Les caracteristiques de l'ennemi (E = Enemy)
    ELVL = Ennemi[0]
    EPV = Ennemi[1]
    EATK = Ennemi[2]
    EDEF = Ennemi[3]
    EEXP = Ennemi[4]
    EARGENT = Ennemi[5]
    ETYPE = Ennemi[7]
    ENAME = str()

    #Assigne l'ID de l'ennemi a un nom
    if Ennemi[6] == 1 :
        ENAME = "votre portable"
        E_IMG = pygame.image.load('Assets/Battle/Enemy/smartphone.png')
    elif Ennemi[6] == 2 :
        ENAME = "Facebook" 
        E_IMG = pygame.image.load('Assets/Battle/Enemy/facebook.png')
    elif Ennemi[6] == 3 :
        ENAME = "Reddit" 
        E_IMG = pygame.image.load('Assets/Battle/Enemy/reddit.png')
    elif Ennemi[6] == 4 :
        ENAME = "Twitter" 
        E_IMG = pygame.image.load('Assets/Battle/Enemy/twitter.png')
    elif Ennemi[6] == 5 :
        ENAME = "Console" 
        E_IMG = pygame.image.load('Assets/Battle/Enemy/console.png')
    elif Ennemi[6] == 6 :
        ENAME = "Television" 
        E_IMG = pygame.image.load('Assets/Battle/Enemy/tv.png')
    elif Ennemi[6] == 7 :
        ENAME = "Devoir de math" 
        E_IMG = pygame.image.load('Assets/Battle/Enemy/document.png')
    elif Ennemi[6] == 8 :
        ENAME = "Devoir de francais" 
        E_IMG = pygame.image.load('Assets/Battle/Enemy/document.png')
    elif Ennemi[6] == 9 :
        ENAME = "Devoir d'anglais" 
        E_IMG = pygame.image.load('Assets/Battle/Enemy/document.png')
    elif Ennemi[6] == 10 :
        ENAME = "Partiels" 
        E_IMG = pygame.image.load('Assets/Battle/Enemy/document.png')
        Music("BossF")

    #Les caracteristiques du joueur (P = Player)
    PLVL = Joueur[0]
    PPV = Joueur[1]
    PATK = Joueur[2]
    PDEF = Joueur[3]
    PEXP = Joueur[4]
    PARGENT = Joueur[5]

    #Flag qui permet de lancer le combat et de le terminer
    Victoire = True

    #Si l'ennemi fait une attaque chargee (Charge = 1) ou pas (Charge = 0)
    Charge = 0

    #Si le joueur se defend (Defendre = 1) ou pas (Defendre = 0)
    Defendre = 0

    #Les differentes phases du combat
        #Avancee = 0 => Combat phase idle
        #Avancee = 1 => Joueur attaque
        #Avancee = 2 => Joueur se defend
        #Avancee = 3 => Joueur utilise un objet
        #Avancee = 4 => Joueur fuit
        #Avancee = 5 => Joueur quitte  
        #Avancee = 6 => Tour de l'ennemi
        #Avancee = 7 => Victoire
        #Avancee = 8 => Defaite
        #Avancee = 9 => Fuite reussie
    Avancee = 0 

    #Initialisation des donnees du combat
    EPV_Actuel = EPV
    PPV_Actuel = Player["stats"][6]

    def rect_haut(texte):
        """Dessine le rectangle en haut de l'ecran et gere le texte a l'interieur"""

        #Dessiner un rectangle, les arguments : (sur quoi, couleur, (position X, position Y, largeur, hauteur))
        pygame.draw.rect(screen, (255, 255, 255), (50, 50, 700, 60))
        pygame.draw.rect(screen, (0, 0, 0), (55, 55, 690, 50))

        afficher(texte, 20, (255,255,255), (65,70))

    def Pinfo(PV_Actuel, PV, LVL, PR, DSC):
        """Informations sur le joueur (P = Player)"""

        #Dessine un rectangle pour contenir les informations
        pygame.draw.rect(screen, (255, 255, 255), (50, 440, 700, 50))
        pygame.draw.rect(screen, (0, 0, 0), (55, 445, 690, 40))

        X = 70

        #La barre de vie du joueur
        BARREVIE(PV_Actuel, PV, X + 515, 460)
        #Affiche le mot Concentration a cote de la barre de vie du joueur et les points de vies dans la barre
        afficher("CON", 20, (255,255,255), (X + 465, 455))
        afficher("{} / {}".format(PV_Actuel, PV), 20, (255,255,255), (X + 520, 455))

        #Afficher le nom du joueur et son niveau.
        afficher("Nv.{} {}".format(LVL, Player["name"]), 20, (255,255,255), (X, 455))
        afficher("PRD : {} | DSC : {}".format(PR, DSC), 20, (255,255,255), (X+215, 455))

    def Draw_Enemy(EPV_Actuel, EPV, E_IMG, screen):
        """Dessine l'ennemi et ses informations sur l'ecran"""
        #Dessiner un rectangle, les arguments : (sur quoi, couleur, (position X, position Y, largeur, hauteur))
        pygame.draw.rect(screen, (255, 255, 255), (280, 140, 260, 260))
        pygame.draw.rect(screen, (0, 0, 0), (285, 145, 250, 250))
        #Depose le sprite de l'ennemi
        screen.blit(E_IMG, (350,200))
        #La barre de vie de l'ennemi
        BARREVIE(EPV_Actuel, EPV, 350, 360)
        #Affiche le mot PV a cote de la barre de vie de l'ennemi
        afficher("PV", 20, (255,255,255), (315, 355))

        #Affiche les PV (= CON = concentration) et les infos du joueur
        Pinfo(PPV_Actuel, PPV, PLVL, PATK, PDEF)

    def Avancee0():
        """Phase idle du combat, on choisie entre attaquer, se defendre, inventaire, abandonner."""

        #Gere le rectangle en haut de l'ecran pour la phase idle.
        rect_haut("Vous vous confrontez a {} Nv.{} !".format(ENAME, ELVL))

        #Definit les couleurs des rectangles en bas de l'ecran.
        rect_couleur_ATK = [255,158,46]
        rect_couleur_DEF = [255,255,255]
        rect_couleur_INV = [255,255,255]
        rect_couleur_ESC = [255,255,255]

        #Choix durant cette phase d'idle
            #Choix = 1 : Attaquer
            #Choix = 2 : Defendre
            #Choix = 3 : Inventaire
            #Choix = 4 : Fuir
        Choix_idle = 1
                
        Avancee00 = 0

        while Avancee00 == 0 :
            #Tant qu'on est encore dans cette phase idle, on execute la fonction

            #Rectangle "Attaquer"
            RectATKX = 30
            RectATKY = 500
            pygame.draw.rect(screen, rect_couleur_ATK, (RectATKX, RectATKY, 170, 60))
            pygame.draw.rect(screen, (0, 0, 0), (RectATKX+5, RectATKY+5, 160, 50))
            afficher("Attaquer", 20, rect_couleur_ATK, (RectATKX+20, RectATKY+18))

            #Retangle "Se defendre"
            pygame.draw.rect(screen, rect_couleur_DEF, (RectATKX+190, RectATKY, 170, 60))
            pygame.draw.rect(screen, (0, 0, 0), (RectATKX+195, RectATKY+5, 160, 50))
            afficher("Defendre", 20, rect_couleur_DEF, (RectATKX+210, RectATKY+18))

            #Retangle "Inventaire"
            pygame.draw.rect(screen, rect_couleur_INV, (RectATKX+380, RectATKY, 170, 60))
            pygame.draw.rect(screen, (0, 0, 0), (RectATKX+385, RectATKY+5, 160, 50))
            afficher("Inventaire", 20, rect_couleur_INV, (RectATKX+400, RectATKY+18))

            #Retangle "Fuir"
            pygame.draw.rect(screen, rect_couleur_ESC, (RectATKX+570, RectATKY, 170, 60))
            pygame.draw.rect(screen, (0, 0, 0), (RectATKX+575, RectATKY+5, 160, 50))
            afficher("Fuir", 20, rect_couleur_ESC, (RectATKX+590, RectATKY+18))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #Si on souhaite fermer le jeu
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                # Si une touche est pressee, on se deplace dans le menu
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        Choix_idle -= 1
                        SFX("navigate")

                    if event.key == pygame.K_RIGHT:
                        Choix_idle += 1
                        SFX("navigate")

                    if event.key == pygame.K_SPACE:
                        Avancee00 = Choix_idle
                        SFX("select")
                        return Avancee00

            #Passer sur les choix sans les valider
            if Choix_idle < 1 :
                Choix_idle = 1
            elif Choix_idle == 1:
                rect_couleur_ATK = [255,158,46]
                rect_couleur_DEF = [255,255,255]
                rect_couleur_INV = [255,255,255]
                rect_couleur_ESC = [255,255,255]
            elif Choix_idle == 2:
                rect_couleur_ATK = [255,255,255]
                rect_couleur_DEF = [255,158,46]
                rect_couleur_INV = [255,255,255]
                rect_couleur_ESC = [255,255,255]
            elif Choix_idle == 3:
                rect_couleur_ATK = [255,255,255]
                rect_couleur_DEF = [255,255,255]
                rect_couleur_INV = [255,158,46]
                rect_couleur_ESC = [255,255,255]
            elif Choix_idle == 4:
                rect_couleur_ATK = [255,255,255]
                rect_couleur_DEF = [255,255,255]
                rect_couleur_INV = [255,255,255]
                rect_couleur_ESC = [255,158,46]
            elif Choix_idle > 4: 
                Choix_idle = 4

            pygame.display.update() #Update l'ecran

    def Avancee1(PATK, EDEF, EPV_Actuel, EPV, EEXP, EARGENT, PPV_Actuel, PPV, ETYPE):
        """Phase d'attaque du combat."""

        #Gere les types de l'ennemi, le joueur inflige 10% de degats en plus par 
        if ETYPE == 1 : #Si l'ennemi a un raport avec les maths
            PATK = PATK + ceil(PATK*Player["Math"]*0.05)
        elif ETYPE == 2 : #Si l'ennemi a un rapport avec le francais
            PATK = PATK + ceil(PATK*Player["Francais"]*0.05)
        elif ETYPE == 3 : #Si l'ennemi a un rapport avec l'anglais
            PATK = PATK + ceil(PATK*Player["Anglais"]*0.05)
            

        #Change le message dans le rectangle en haut
        rect_haut("Appuyer sur ESPACE au bon moment !")

        PPV_Pourcent = PPV_Actuel / PPV

        #---Affiche le rectangle d'attaque---
        TailleY = 10 #Epaisseur Y des barres
        Taille_BarreXR = 80*PPV_Pourcent+20 #Taille X de la barre rouge. Plus on perd de vie, plus la barre rouge est petite
        Taille_BarreXJ = 7 #Taille Y de la barre jaune
        X_Cursor = 740 #Position X du curseur

        #Animation pour laisser au joueur le temps de se preparer a appuyer au bon moment
        while TailleY < 50:
            pygame.draw.rect(screen, (255, 255, 255), (50, 440, 700, TailleY))
            pygame.draw.rect(screen, (0, 0, 0), (55, 445, 690, TailleY-10))
            pygame.draw.rect(screen, (255, 67, 67), (404 - Taille_BarreXR/2, 445, Taille_BarreXR, TailleY-10))
            pygame.draw.rect(screen, (255, 255, 67), (404 - Taille_BarreXJ/2, 445, Taille_BarreXJ, TailleY-10))
            pygame.draw.rect(screen, (67, 255, 67), (X_Cursor, 445, 5, TailleY-10))

            TailleY += 0.1
            pygame.display.update() #Update l'ecran

        Pos_Cursor = X_Cursor
        #Deplace le curseur et demande au joueur d'appuyer au bon moment.
        while X_Cursor > 55 :
            pygame.draw.rect(screen, (255, 255, 255), (50, 440, 700, TailleY))
            pygame.draw.rect(screen, (0, 0, 0), (55, 445, 690, TailleY-10))
            pygame.draw.rect(screen, (255, 67, 67), (404 - Taille_BarreXR/2, 445, Taille_BarreXR, TailleY-10))
            pygame.draw.rect(screen, (255, 255, 67), (404 - Taille_BarreXJ/2, 445, Taille_BarreXJ, TailleY-10))
            pygame.draw.rect(screen, (67, 255, 67), (X_Cursor, 445, 5, TailleY-10))

            X_Cursor += -0.4 - 0.4*(1-PPV_Pourcent) #Plus on perd de vie, plus le curseur est rapide
            pygame.display.update() #Update l'ecran

            #Gere les input du joueur
            for event in pygame.event.get():
                #Si on souhaite fermer le jeu
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # Si la touche espace est pressee, arrete le curseur
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:
                        Pos_Cursor = X_Cursor
                        X_Cursor = 55

        #Calcul des degats
        #Si on a arrete le curseur dans la zone jaune, on fait un coup critique
        if abs(Pos_Cursor - 404 + 2.5) < Taille_BarreXJ/2 and PATK - EDEF > 0:
            Degats = ceil(PATK * 1.5 - EDEF)
            SFX("damage")
            #Change le message dans le rectangle en haut pour afficher nos degats.
            rect_haut("Coup critique ! Vous infligez {} degats !".format(Degats))

        #Si on arrete le curseur dans la zone rouge, on fait une attaque normale
        elif abs(Pos_Cursor - 404 + 2.5) < Taille_BarreXR/2 and PATK - EDEF > 0:
            Degats = ceil(PATK - EDEF)
            SFX("damage")
            #Change le message dans le rectangle en haut pour afficher nos degats.
            rect_haut("Vous infligez {} degats !".format(Degats))

        #Si on arrete le curseur en dehors de la zone rouge, on rate
        else:
            Degats = 0
            #Change le message dans le rectangle en haut pour afficher nos degats.
            rect_haut("Vous ratez votre attaque !")
            pygame.display.update() #Update l'ecran

        #Condition qui permet d'eviter d'avoir une sante dans le negatif
        if EPV_Actuel < Degats :
            Degats = EPV_Actuel
        #Diminue la sante de l'ennemi
        EPV_Degats = EPV_Actuel - Degats #La sante de l'ennemi apres avoir recu une attaque
        while EPV_Actuel > EPV_Degats :
            #La barre de vie de l'ennemi diminue progressivement
            EPV_Actuel -= 1
            BARREVIE(EPV_Actuel, EPV, 350, 360)
            pygame.display.update() #Update l'ecran
            pygame.time.wait(25)
        valider()

        #Passage vers la phase suivante du combat. Si le joueur tue l'ennemi, termine, sinon, l'ennemi attaque
        if EPV_Actuel > 0 :
            return 6, EPV_Actuel
        else :
            if ENAME == "Partiels":
                #Gere les input du joueur
                rect_haut("Victoires ! Vous avez reussi vos partiels !")
                pygame.display.update() #Update l'ecran
                valider()
                #Gere les input du joueur
                rect_haut("Vous terminez ainsi le jeu, bravo !")
                pygame.display.update() #Update l'ecran
                valider()
                return 7, EPV_Actuel
            else :
                #Affiche le message de fin
                rect_haut("Victoire ! Vous recevez {} EXP et {} euros.".format(EEXP, EARGENT))
                pygame.display.update() #Update l'ecran
                valider()

                #Si on monte de niveau, affiche qu'on monte de niveau
                if Player["stats"][4] + EEXP > 100:
                    rect_haut("Vous montez au niveau {} !".format(Player["stats"][0]+1))
                    pygame.display.update() #Update l'ecran
                    valider()

                return 7, EPV_Actuel

    def Avancee2():
        """Permet au joueur de se defendre et de diviser par 2 les degats recus durant le tour de l'ennemi. Apres quoi, ca se reset"""

        #Affiche dans le rectangle en haut de l'ecran qu'on se defend.
        rect_haut("Vous vous defendez !")
        SFX("defense")
        pygame.display.update() #Update l'ecran
        valider()
        
        return 6, 1

    def Avancee3(PPV_Actuel, PPV, PATK, PDEF):
        """Gestion de l'inventaire en combat. Retourne l'avancee du combat, le PPV_Actuel, PATK et PDEF respectivement."""

        #Couleurs
        WHITE = [255,255,255]
        BLACK = [0,0,0]
        ORANGE = [255,158,46]

        #Dessiner un rectangle, les arguments : (sur quoi, couleur, (position X, position Y, largeur, hauteur))
        pygame.draw.rect(screen, WHITE, (50, 430, 700, 130))
        pygame.draw.rect(screen, BLACK, (55, 435, 690, 120))
        

        #Permet de naviguer dans le menu
        decision = 1

        #Je sais, c'est pas beau du tout mais c'est rapide a ecrire en tout cas. Du quick and dirty.
        while 1 <= decision <= 7 :

            #Va gerer l'affichage du rectangle en haut de l'ecran et la couleur des mots en fonction d'ou on est.
            if decision == 1: #On assigne a chaque decision un affichage different. Tous les mots sont blancs, sauf celui sur lequel on est
                afficher("{}x Boisson Energisante".format(Inventaire["Boisson Energisante"][0]), 20, ORANGE, (60, 450))
                afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (60, 480))
                afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (60, 510))
                afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE, (405, 450))
                afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE, (405, 480))
                afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (405, 510))
                afficher("Retour", 20, WHITE, (640, 510))
                rect_haut("Restaure {} CON".format(Inventaire["Boisson Energisante"][3])) #Le message en haut de l'ecran
            elif decision == 2:
                afficher("{}x Boisson Energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (60, 450))
                afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, ORANGE, (60, 480))
                afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (60, 510))
                afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE, (405, 450))
                afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE, (405, 480))
                afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (405, 510))
                afficher("Retour", 20, WHITE, (640, 510))
                rect_haut("Restaure {} CON".format(Inventaire["Burger"][3]))
            elif decision == 3:
                afficher("{}x Boisson Energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (60, 450))
                afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (60, 480))
                afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, ORANGE, (60, 510))
                afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE, (405, 450))
                afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE, (405, 480))
                afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (405, 510))
                afficher("Retour", 20, WHITE, (640, 510))
                rect_haut("Restaure {} CON".format(Inventaire["Bubble Tea"][3]))
            elif decision == 4:
                afficher("{}x Boisson Energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (60, 450))
                afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (60, 480))
                afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (60, 510))
                afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, ORANGE, (405, 450))
                afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE, (405, 480))
                afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (405, 510))
                afficher("Retour", 20, WHITE, (640, 510))
                rect_haut("Restaure {} CON".format(Inventaire["Dessert au Chocolat"][3]))
            elif decision == 5:
                afficher("{}x Boisson Energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (60, 450))
                afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (60, 480))
                afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (60, 510))
                afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE, (405, 450))
                afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, ORANGE, (405, 480))
                afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (405, 510))
                afficher("Retour", 20, WHITE, (640, 510))
                rect_haut("Augmente la PRD de {}% (Que en combat)".format(Inventaire["Cafe"][3]))
            elif decision == 6:
                afficher("{}x Boisson Energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (60, 450))
                afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (60, 480))
                afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (60, 510))
                afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE, (405, 450))
                afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE, (405, 480))
                afficher("{}x The".format(Inventaire["The"][0]), 20, ORANGE, (405, 510))
                afficher("Retour", 20, WHITE, (640, 510))
                rect_haut("Augmente la DSC de {}% (Que en combat)".format(Inventaire["The"][3]))
            elif decision == 7:
                afficher("{}x Boisson Energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (60, 450))
                afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (60, 480))
                afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (60, 510))
                afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE, (405, 450))
                afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE, (405, 480))
                afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (405, 510))
                afficher("Retour", 20, ORANGE, (640, 510))
                rect_haut("Sortir de l'inventaire")


            #Va gerer les inputs du joueur pour naviguer dans le menu
            for event in pygame.event.get():
                #Si on souhaite fermer le jeu
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # Si une touche est pressee, on se deplace dans le menu
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        if decision == 7: #Si on se trouve sur le bouton "retour", en appuant a gauche on va sur The.
                            decision -= 1
                            SFX("navigate")
                        else:
                            decision -= 3 #Si on se trouve autre part que "retour", en appuyant a gauche on change de colonne ou on revient sur la boisson energisante.
                            SFX("navigate")
                        
                    if event.key == pygame.K_RIGHT:
                        decision += 3
                        SFX("navigate")

                    if event.key == pygame.K_UP:
                        decision -= 1
                        SFX("navigate")

                    if event.key == pygame.K_DOWN:
                        decision += 1
                        SFX("navigate")

                    #Si on selectionne l'un des choix
                    if event.key == pygame.K_SPACE:

                        if decision == 1:
                            #Selectionne la boisson energisante
                            #Si on a encore de cet objet dans son inventaire
                            if Inventaire["Boisson Energisante"][0] > 0:
                                Inventaire["Boisson Energisante"][0] -= 1 #Diminue la quantite de 1 dans l'inventaire
                                PPV_Actuel = PPV_Actuel + Inventaire["Boisson Energisante"][3] #Nous soigne
                                rect_haut("Vous vous restaurez {} CON !".format(Inventaire["Boisson Energisante"][3])) #Affiche sur l'ecran que ça nous soigne
                                SFX("item")
                                pygame.display.update() #Update l'ecran
                                valider() #Demande au joueur de valider
                                if PPV_Actuel > PPV: #Si notre sante apres s'etre fait soigner depasse la sante max
                                    PPV_Actuel = PPV #On remet la sante a son max
                                return 6, PPV_Actuel, PATK, PDEF

                            #Si on n'a plus de cet objet dans son inventaire
                            else :
                                rect_haut("Vous n'en n'avez pas...") #Affiche dans le message dans le rectangle en haut qu'on n'en a plus
                                pygame.display.update() #Update l'ecran
                                SFX("badnote")
                                valider()

                        elif decision == 2:
                            #Selectionne la burger
                            if Inventaire["Burger"][0] > 0:
                                Inventaire["Burger"][0] -= 1
                                PPV_Actuel = PPV_Actuel + Inventaire["Burger"][3]
                                rect_haut("Vous vous restaurez {} CON !".format(Inventaire["Burger"][3]))
                                SFX("item")
                                pygame.display.update() #Update l'ecran
                                valider()
                                if PPV_Actuel > PPV:
                                    PPV_Actuel = PPV
                                return 6, PPV_Actuel, PATK, PDEF

                            #Si on n'a plus de cet objet dans son inventaire
                            else :
                                rect_haut("Vous n'en n'avez pas...")
                                pygame.display.update() #Update l'ecran
                                SFX("badnote")
                                valider()

                        elif decision == 3:
                            #Selectionne du bubble tea
                            if Inventaire["Bubble Tea"][0] > 0:
                                Inventaire["Bubble Tea"][0] -= 1
                                PPV_Actuel = PPV_Actuel + Inventaire["Bubble Tea"][3]
                                rect_haut("Vous vous restaurez {} CON !".format(Inventaire["Bubble Tea"][3]))
                                SFX("item")
                                pygame.display.update() #Update l'ecran
                                valider()
                                if PPV_Actuel > PPV:
                                    PPV_Actuel = PPV
                                return 6, PPV_Actuel, PATK, PDEF

                            #Si on n'a plus de cet objet dans son inventaire
                            else :
                                rect_haut("Vous n'en n'avez pas...")
                                pygame.display.update() #Update l'ecran
                                SFX("badnote")
                                valider()

                        elif decision == 4:
                            #Selectionne du dessert au chocolat
                            if Inventaire["Dessert au Chocolat"][0] > 0:
                                Inventaire["Dessert au Chocolat"][0] -= 1
                                PPV_Actuel = PPV_Actuel + Inventaire["Dessert au Chocolat"][3]
                                rect_haut("Vous vous restaurez {} CON !".format(Inventaire["Dessert au Chocolat"][3]))
                                SFX("item")
                                pygame.display.update() #Update l'ecran
                                valider()
                                if PPV_Actuel > PPV:
                                    PPV_Actuel = PPV
                                return 6, PPV_Actuel, PATK, PDEF

                            #Si on n'a plus de cet objet dans son inventaire
                            else :
                                rect_haut("Vous n'en n'avez pas...")
                                pygame.display.update() #Update l'ecran
                                SFX("badnote")
                                valider()

                        elif decision == 5:
                            #Selectionne du cafe
                            if Inventaire["Cafe"][0] > 0 and Inventaire["Cafe"][4] == 0:
                                Inventaire["Cafe"][0] -= 1
                                rect_haut("Vous augmentez votre PRD de {}% !".format(Inventaire["Cafe"][3]))
                                SFX("item")
                                pygame.display.update() #Update l'ecran
                                valider()
                                PATK = ceil(PATK + PATK*Inventaire["Cafe"][3]/100)
                                Inventaire["Cafe"][4] += 1
                                return 6, PPV_Actuel, PATK, PDEF

                            #Si on n'a plus de cet objet dans son inventaire
                            elif Inventaire["Cafe"][0] <= 0:
                                rect_haut("Vous n'en n'avez pas...")
                                pygame.display.update() #Update l'ecran
                                SFX("badnote")
                                valider()
                                
                            #Si on en a deja bu durant le combat
                            else :
                                rect_haut("Vous avez deja bu du cafe durant le combat.")
                                pygame.display.update() #Update l'ecran
                                SFX("badnote")
                                valider()

                        elif decision == 6:
                            #Selectionne du the
                            if Inventaire["The"][0] > 0 and Inventaire["The"][4] == 0:
                                Inventaire["The"][0] -= 1
                                rect_haut("Vous augmentez votre DSC de {}% !".format(Inventaire["The"][3]))
                                SFX("item")
                                pygame.display.update() #Update l'ecran
                                valider()
                                PDEF = ceil(PDEF + PDEF*Inventaire["The"][3]/100)
                                Inventaire["The"][4] += 1

                                return 6, PPV_Actuel, PATK, PDEF

                            #Si on n'a plus de cet objet dans son inventaire
                            elif Inventaire["The"][0] <= 0:
                                rect_haut("Vous n'en n'avez pas...")
                                pygame.display.update() #Update l'ecran
                                SFX("badnote")
                                valider()

                            #Si on en a deja bu durant le combat
                            else :
                                rect_haut("Vous avez deja bu du the durant le combat.")
                                pygame.display.update() #Update l'ecran
                                SFX("badnote")
                                valider()

                        elif decision == 7 :
                            #Selectionne retour
                            return 0, PPV_Actuel, PATK, PDEF

            #Les bordures, pour ne pas naviguer au dela de l'inventaire
            if decision < 1:
                decision = 1
            elif decision > 7:
                decision = 7

            pygame.display.update() #Update l'ecran

        return 0, PPV_Actuel, PATK, PDEF

    def Avancee4(PARGENT, PLVL, PATK, PDEF, ELVL):
        """Fonction qui gere la phase de fuite du combat."""

        #Les chances de fuire.
        Chance_Fuite = 50 + (PLVL - ELVL) * 5
        Hasard = random.randint(0,100)

        if Hasard < Chance_Fuite:
            #Si on arrive a fuire
            rect_haut("Vous parvenez a fuire !")
            pygame.display.update() #Update l'ecran
            valider()

            #Message qui annonce qu'on perd de l'argent.
            rect_haut("Vous perdez {} euro(s) durant votre fuite.".format(ceil(PARGENT*0.1)))
            pygame.display.update() #Update l'ecran
            SFX("hurt")
            valider()

            #On perd de l'argent lorsqu'on fuit. 10% de perte.
            PARGENT = PARGENT - ceil(PARGENT*0.1)

            return PARGENT, 9


        else:
            #Si la fuite echoue
            rect_haut("Vous tentez de fuir mais echouez !")
            pygame.display.update() #Update l'ecran
            SFX("badnote")
            valider()

            return PARGENT, 6

    def Avancee6(PPV_Actuel, PPV, PATK, PDEF, PLVL, EATK, Charge, Defendre):
        """Phase ou l'ennemi nous attaque."""

        #Calcul de ses degats
        #Si l'ennemi charge son attaque
        if Charge == 1:
            Degats = ceil(EATK*2 - PDEF)
        else :
            Degats = ceil(EATK - PDEF)

        #Si le joueur se defend
        if Defendre == 1:
            Degats = ceil(Degats/3)
        
        if Degats < 0 : #Pour eviter de soigner le joueur si les degats sont inferieurs a 0
            Degats = 0

        #Hit value, determine si l'ennemi rate, fait un coup critique ou une attaque normale
        CC = random.randint(0, 100)

        #Si l'ennemi rate son attaque
        if CC < 5 :
            Degats = 0
            #Change le message dans le rectangle en haut pour afficher nos degats.
            rect_haut("L'ennemi vous attaque et rate !")
            pygame.display.update() #Update l'ecran
            valider()

        #Si l'ennemi reussit son attaque
        elif CC < 90 :
            #Change le message dans le rectangle en haut pour afficher nos degats.
            rect_haut("L'ennemi attaque ! Vous perdez {} CON !".format(Degats))
            SFX("hurt")
            pygame.display.update() #Update l'ecran

            if PPV_Actuel < Degats :
                Degats = PPV_Actuel
            #Diminue la sante du joueur
            PPV_Degats = PPV_Actuel - Degats
            while PPV_Actuel > PPV_Degats :
                #Les infos du joueur
                PPV_Actuel -= 1
                Pinfo(PPV_Actuel, PPV, PLVL, PATK, PDEF)
                pygame.display.update() #Update l'ecran
                pygame.time.wait(25)
            valider()
            
        #Si l'ennemi fait un coup critique
        else :
            Degats = Degats * 2
            #Change le message dans le rectangle en haut pour afficher nos degats.
            rect_haut("L'ennemi attaque ! Coup critique !")
            pygame.display.update() #Update l'ecran
            valider()
            rect_haut("Vous perdez {} CON !".format(Degats))
            SFX("hurt")
            pygame.display.update() #Update l'ecran

            if PPV_Actuel < Degats :
                Degats = PPV_Actuel
            #Diminue la sante du joueur
            PPV_Degats = PPV_Actuel - Degats
            while PPV_Actuel > PPV_Degats :

                #Les infos du joueur
                PPV_Actuel -= 1
                Pinfo(PPV_Actuel, PPV, PLVL, PATK, PDEF)
                pygame.display.update() #Update l'ecran
                pygame.time.wait(25)
            
            valider()

        #Si l'ennemi fait une attaque chargee ou pas pour son prochain tour
        CC = random.randint(0,100)
        if CC < 85 and PPV_Actuel > 0:
            Charge = 0
        elif PPV_Actuel > 0 :
            Charge = 1
            rect_haut("L'ennemi charge sa prochaine attaque...")
            pygame.display.update() #Update l'ecran
            valider()

        #Reset de la fonction defendre
        Defendre = 0

        #Si le joueur est encore en vie, ou s'il est mort
        if PPV_Actuel > 0 :
            return 0, Charge, PPV_Actuel, Defendre
        else :
            rect_haut("Vous avez perdu...")
            pygame.display.update() #Update l'ecran
            valider()
            return 8, Charge, PPV_Actuel, Defendre

    #Boucle du combat
    while Victoire == True :

        #Background
        screen.blit(background, (0, 0))

        #Afficher l'ennemi a l'ecran avec ses informations et son rectangle
        Draw_Enemy(EPV_Actuel, EPV, E_IMG, screen)

        if Avancee == 0 :
            #Phase idle du combat
            Avancee = Avancee0()
        elif Avancee == 1 :
            #Phase d'attaque du joueur
            Avancee, EPV_Actuel = Avancee1(PATK, EDEF, EPV_Actuel, EPV, EEXP, EARGENT, PPV_Actuel, PPV, ETYPE)
        elif Avancee == 2 :
            #Phase de defense du joueur
            Avancee, Defendre = Avancee2()
        elif Avancee == 3 :
            #Phase ou le joueur choisie un objet a utiliser dans son inventaire
            Avancee, PPV_Actuel, PATK, PDEF = Avancee3(PPV_Actuel, PPV, PATK, PDEF)
        elif Avancee == 4 :
            #Phase ou le joueur essaie de fuir
            PARGENT, Avancee = Avancee4(PARGENT, PLVL, PATK, PDEF, ELVL)
        elif Avancee == 6 :
            #Tour de l'ennemi
            Avancee, Charge, PPV_Actuel, Defendre = Avancee6(PPV_Actuel, PPV, PATK, PDEF, PLVL, EATK, Charge, Defendre)

        #____________________________ Les conclusions ____________________________
        elif Avancee == 7 : #On gagne
            Player["stats"][4] += EEXP
            #On monte de niveau si on atteint 100 d'experience
            while Player["stats"][4] >= 100 :
                Player["stats"][4] = Player["stats"][4] - 100
                Player["stats"][0] += 1
                Player_Update(Player["stats"][0])

            Player["stats"][6] = PPV_Actuel
            Player["stats"][5] += EARGENT
            Inventaire["The"][4], Inventaire["Cafe"][4] = 0, 0 #Reset l'effet galvanisant du the et cafe
            return 1
        elif Avancee == 8 : #On perd
            return 0
        elif Avancee == 9 : #On fuit
            Player["stats"][5] = Player["stats"][5] - ceil(Player["stats"][5]*0.1)
            Inventaire["The"][4], Inventaire["Cafe"][4] = 0, 0 #Reset l'effet galvanisant du the et cafe
            return 1

def menu_nav(Joueur):
    """Gere le menu de navigation, permettant de se deplacer, voir l'inventaire et utiliser des objets, acheter des objets et quitter le jeu. """

    #____________________Rentre les variables qui seront utilisee tout au long de la fonction____________________
    #Les caracteristiques du joueur (P = Player)
    PLVL = Joueur[0]
    PPV = Joueur[1]
    PATK = Joueur[2]
    PDEF = Joueur[3]
    PEXP = Joueur[4]
    PARGENT = Joueur[5]
    PPV_Actuel = Joueur[6]


    #Les differentes phases du menu
        #Avancee = 0 => La phase idle, permettant d'acceder au deplacement et autres parties du menu de navigation
        #Avancee = 1 => Gere le deplacement
        #Avancee = 2 => Gere l'inventaire
        #Avancee = 3 => Gere le shop
        #Avancee = 4 => Gere le menu (pour afficher les stats du perso, gere les options, revenir au menu principal, sauvegarder...)
        #Avancee = 5 => On ferme la fenetre
        #Avancee = 6 => 
    Avancee = 0

    #Les conclusions
        #Conclu = 0 => Aucune conclusion, on est encore dans le menu de navigation et on choisie ce qu'on fait
        #Conclu = 1 => On se deplace et avance en jour
    Conclu = 0

    def PStatsIni(PATK, PDEF, equip):
        """Permet le calcul des stats du personnage selon les equipements qu'il porte. equip : 1 = Stylo et feuilles | 2 = Cahier | 3 = Tablette | 4 = PC"""

        #La phase d'initialisation. Permet de savoir quel equipement est equipe
        if equip == 0: #Rien
            Inventaire["Stylo et feuilles"][4] = 0
            Inventaire["Cahier"][4] = 0
            Inventaire["Tablette"][4] = 0
            Inventaire["PC"][4] = 0
        elif equip == 1: #Stylo et feuilles
            Inventaire["Stylo et feuilles"][4] = 1
            Inventaire["Cahier"][4] = 0
            Inventaire["Tablette"][4] = 0
            Inventaire["PC"][4] = 0
        elif equip == 2: #Cahier
            Inventaire["Stylo et feuilles"][4] = 0
            Inventaire["Cahier"][4] = 1
            Inventaire["Tablette"][4] = 0
            Inventaire["PC"][4] = 0
        elif equip == 3: #Tablette
            Inventaire["Stylo et feuilles"][4] = 0
            Inventaire["Cahier"][4] = 0
            Inventaire["Tablette"][4] = 1
            Inventaire["PC"][4] = 0
        elif equip == 4: #PC
            Inventaire["Stylo et feuilles"][4] = 0
            Inventaire["Cahier"][4] = 0
            Inventaire["Tablette"][4] = 0
            Inventaire["PC"][4] = 1

        #Rien d'equipe
        if Inventaire["Stylo et feuilles"][4] == 0 and Inventaire["Cahier"][4] == 0 and Inventaire["Tablette"][4] == 0 and Inventaire["PC"][4] == 0:
            PATK = Player["stats"][7]
            PDEF = Player["stats"][8]
        #Le stylo et les feuilles
        if Inventaire["Stylo et feuilles"][4] == 1:
            PATK = Player["stats"][7] + ceil(Player["stats"][7]*Inventaire["Stylo et feuilles"][3])
            PDEF = Player["stats"][8] + ceil(Player["stats"][8]*Inventaire["Stylo et feuilles"][3])
        #Le cahier
        if Inventaire["Cahier"][4] == 1:
            PATK = Player["stats"][7] + ceil(Player["stats"][7]*Inventaire["Cahier"][3])
            PDEF = Player["stats"][8] + ceil(Player["stats"][8]*Inventaire["Cahier"][3])
        #La tablette
        if Inventaire["Tablette"][4] == 1:
            PATK = Player["stats"][7] + ceil(Player["stats"][7]*Inventaire["Tablette"][3])
            PDEF = Player["stats"][8]
        #Le PC
        if Inventaire["PC"][4] == 1:
            PATK = Player["stats"][7] + ceil(Player["stats"][7]*Inventaire["PC"][3])
            PDEF = Player["stats"][8]

        return PATK, PDEF

    def Rec_Haut():
        """Gere l'affichage du rectangle en haut de l'ecran dans le menu de navigation"""

        WHITE, ORANGE, ALPHA = Couleurs()
        #Affiche le background
        background = pygame.image.load('Assets/Menu_de_navigation/Background/Menu_Nav_Background.gif')
        screen.blit(background, (-210, 0))

        window_draw_rect(WHITE, ALPHA, 600, 25, 170, 50)
        afficher("Jour {}".format(Player["jour"]), 20, (255,255,255), (628, 40))

        #Rectangle du haut, qui affiche des messages en fonctions de ce qu'on regarde
        window_draw_rect(WHITE, ALPHA, 30, 25, 570, 50)

    def Avancee0():
        """L'idle du menu de navigation. La page d'accueil ou on selectionne ce qu'on veut faire (agir, inventaire, magasin, autre)."""

        WHITE, ORANGE, ALPHA = Couleurs()

        #Position des rectangles du bas de l'ecran
        X_RecBas = 30
        Y_RecBas = 500

        #Va permettre de choisir entre les differents choix
        choix = 1

        idle_running = True
        while idle_running == True:

            #Dessine le rectangle en haut de l'ecran permettant d'afficher n'importe quel message et le jour.
            Rec_Haut()

            if choix == 1:
                #Affiche dans le rectangle du haut
                afficher("Travailler ou se reposer.", 20, WHITE, (50, 40))
                #Rectangle agir
                window_draw_rect(ORANGE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
                afficher("Agir", 20, ORANGE, (X_RecBas+60, Y_RecBas+20))
                #Rectangle Inventaire
                window_draw_rect(WHITE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
                afficher("Inventaire", 20, WHITE, (X_RecBas+209, Y_RecBas+20))
                #Rectangle Shop
                window_draw_rect(WHITE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
                afficher("Magasin", 20, WHITE, (X_RecBas+418, Y_RecBas+20))
                #Rectangle Options
                window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
                afficher("Autre", 20, WHITE, (X_RecBas+621, Y_RecBas+20))
            elif choix == 2:
                #Affiche dans le rectangle du haut
                afficher("Utiliser ou equiper un objet.", 20, WHITE, (50, 40))
                #Rectangle agir
                window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
                afficher("Agir", 20, WHITE, (X_RecBas+60, Y_RecBas+20))
                #Rectangle Inventaire
                window_draw_rect(ORANGE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
                afficher("Inventaire", 20, ORANGE, (X_RecBas+209, Y_RecBas+20))
                #Rectangle Shop
                window_draw_rect(WHITE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
                afficher("Magasin", 20, WHITE, (X_RecBas+418, Y_RecBas+20))
                #Rectangle Options
                window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
                afficher("Autre", 20, WHITE, (X_RecBas+621, Y_RecBas+20))
            elif choix == 3:
                #Affiche dans le rectangle du haut
                afficher("Acheter ou vendre un objet.", 20, WHITE, (50, 40))
                #Rectangle agir
                window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
                afficher("Agir", 20, WHITE, (X_RecBas+60, Y_RecBas+20))
                #Rectangle Inventaire
                window_draw_rect(WHITE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
                afficher("Inventaire", 20, WHITE, (X_RecBas+209, Y_RecBas+20))
                #Rectangle Shop
                window_draw_rect(ORANGE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
                afficher("Magasin", 20, ORANGE, (X_RecBas+418, Y_RecBas+20))
                #Rectangle Options
                window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
                afficher("Autre", 20, WHITE, (X_RecBas+621, Y_RecBas+20))
            elif choix == 4:
                #Affiche dans le rectangle du haut
                afficher("Aide, sauvegarder, quitter.", 20, WHITE, (50, 40))
                #Rectangle agir
                window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
                afficher("Agir", 20, WHITE, (X_RecBas+60, Y_RecBas+20))
                #Rectangle Inventaire
                window_draw_rect(WHITE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
                afficher("Inventaire", 20, WHITE, (X_RecBas+209, Y_RecBas+20))
                #Rectangle Shop
                window_draw_rect(WHITE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
                afficher("Magasin", 20, WHITE, (X_RecBas+418, Y_RecBas+20))
                #Rectangle Options
                window_draw_rect(ORANGE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
                afficher("Autre", 20, ORANGE, (X_RecBas+621, Y_RecBas+20))

            #Gere les inputs
            for event in pygame.event.get():
                #Fermer la fenetre du jeu
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
               
                # Si une touche est pressee, on se deplace dans le menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        choix -= 1
                        SFX("navigate")
                    if event.key == pygame.K_RIGHT:
                        choix += 1
                        SFX("navigate")

                    #Selection du menu
                    if event.key== pygame.K_UP:
                        SFX("navigate")
                        if choix == 1: #Selection du bouton agir
                            return 1
                        elif choix == 2: #Selection du bouton inventaire
                            return 2
                        elif choix == 3: #Selection du bouton magasin
                            return 3
                        else: #Selection du bouton autre
                            return 4

                    #Selection du menu
                    if event.key == pygame.K_SPACE:
                        SFX("select")
                        if choix == 1: #Selection du bouton agir
                            return 1
                        elif choix == 2: #Selection du bouton agir
                            return 2
                        elif choix == 3: #Selection du bouton agir
                            return 3
                        else: #Selection du bouton Option
                            return 4

            if choix < 1:
                choix = 1
            elif choix > 4:
                choix = 4
            
            pygame.display.update() #Update l'ecran

    def Avancee1(PPV_Actuel, PPV):
        """Le bouton Agir. Le joueur choisit s'il veut se reposer, travailler une certaine matiere ou bien revenir dans le menu de navigation idle."""

        #Depose les couleurs dans des variables.
        WHITE, ORANGE, ALPHA = Couleurs()
        YELLOW = [255,255,85]

        #Position des rectangles du bas de l'ecran
        X_RecBas = 30
        Y_RecBas = 500
        
        #Va permettre de choisir entre les differents choix
        choix = 1

        #Va permettre de gerer la boucle de la fonction
        Avancee11 = 0

        while Avancee11 == 0:

            #Affiche le rectangle du haut
            Rec_Haut()

            #Les rectangles sur le bas de l'ecran
            #Rectangle agir
            window_draw_rect(ORANGE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
            afficher("Agir", 20, ORANGE, (X_RecBas+60, Y_RecBas+20))
            #Rectangle Inventaire
            window_draw_rect(WHITE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
            afficher("Inventaire", 20, WHITE, (X_RecBas+209, Y_RecBas+20))
            #Rectangle Shop
            window_draw_rect(WHITE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
            afficher("Magasin", 20, WHITE, (X_RecBas+418, Y_RecBas+20))
            #Rectangle Options
            window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
            afficher("Autre", 20, WHITE, (X_RecBas+621, Y_RecBas+20))

            #Affiche le grand cadre sur la droite de l'ecran avec les messages a l'interieur
            window_draw_rect(WHITE, ALPHA, X_RecBas+190, Y_RecBas-384, 550, 348)

            #Le niveau et le nom
            afficher("{} | Niveau {} (EXP = {}%)".format(Player["name"], PLVL, PEXP), 20, WHITE, (X_RecBas+210,Y_RecBas-344 ))

            #L'argent
            afficher("Argent : {} euros".format(PARGENT), 20, WHITE, (X_RecBas+210,Y_RecBas-294 ))

            #La concentration
            BARREVIE(PPV_Actuel, PPV, X_RecBas+510, Y_RecBas-240)
            afficher("Concentration(CON) = {} / {}".format(PPV_Actuel, PPV), 20, WHITE, (X_RecBas+210,Y_RecBas-244 ))

            #La productivite
            afficher("Productivite(PRD) : {}".format(PATK), 20, WHITE, (X_RecBas+210,Y_RecBas-194 ))

            #La discipline
            afficher("Discipline(DSC) : {}".format(PDEF), 20, WHITE, (X_RecBas+210,Y_RecBas-144 ))

            #Les niveaux dans les differentes matieres
            afficher("Math : {} | Francais : {} | Anglais : {}".format(Player["Math"], Player["Francais"], Player["Anglais"]), 20, WHITE, (X_RecBas+210,Y_RecBas-94 ))

            if choix == 1:
                #Affiche dans le rectangle du haut
                afficher("Travailler les maths.", 20, WHITE, (50, 40))
                #Math
                window_draw_rect(YELLOW, ALPHA, X_RecBas, Y_RecBas-96, 170, 60)
                afficher("Math", 20, YELLOW, (X_RecBas+60, Y_RecBas-76))
                #Francais
                window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas-192, 170, 60)
                afficher("Francais", 20, WHITE, (X_RecBas+34, Y_RecBas-172))
                #Anglais
                window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas-288, 170, 60)
                afficher("Anglais", 20, WHITE, (X_RecBas+40, Y_RecBas-268))
                #Reposer
                window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas-384, 170, 60)
                afficher("Reposer", 20, WHITE, (X_RecBas+40, Y_RecBas-364))
            elif choix == 2:
                #Affiche dans le rectangle du haut
                afficher("Travailler le francais.", 20, WHITE, (50, 40))
                #Math
                window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas-96, 170, 60)
                afficher("Math", 20, WHITE, (X_RecBas+60, Y_RecBas-76))
                #Francais
                window_draw_rect(YELLOW, ALPHA, X_RecBas, Y_RecBas-192, 170, 60)
                afficher("Francais", 20, YELLOW, (X_RecBas+34, Y_RecBas-172))
                #Anglais
                window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas-288, 170, 60)
                afficher("Anglais", 20, WHITE, (X_RecBas+40, Y_RecBas-268))
                #Reposer
                window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas-384, 170, 60)
                afficher("Reposer", 20, WHITE, (X_RecBas+40, Y_RecBas-364))
            elif choix == 3:
                #Affiche dans le rectangle du haut
                afficher("Travailler l'anglais.", 20, WHITE, (50, 40))
                #Math
                window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas-96, 170, 60)
                afficher("Math", 20, WHITE, (X_RecBas+60, Y_RecBas-76))
                #Francais
                window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas-192, 170, 60)
                afficher("Francais", 20, WHITE, (X_RecBas+34, Y_RecBas-172))
                #Anglais
                window_draw_rect(YELLOW, ALPHA, X_RecBas, Y_RecBas-288, 170, 60)
                afficher("Anglais", 20, YELLOW, (X_RecBas+40, Y_RecBas-268))
                #Reposer
                window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas-384, 170, 60)
                afficher("Reposer", 20, WHITE, (X_RecBas+40, Y_RecBas-364))
            else:
                #Affiche dans le rectangle du haut
                afficher("Se reposer et regagner sa CON.", 20, WHITE, (50, 40))
                #Math
                window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas-96, 170, 60)
                afficher("Math", 20, WHITE, (X_RecBas+60, Y_RecBas-76))
                #Francais
                window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas-192, 170, 60)
                afficher("Francais", 20, WHITE, (X_RecBas+34, Y_RecBas-172))
                #Anglais
                window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas-288, 170, 60)
                afficher("Anglais", 20, WHITE, (X_RecBas+40, Y_RecBas-268))
                #Reposer
                window_draw_rect(YELLOW, ALPHA, X_RecBas, Y_RecBas-384, 170, 60)
                afficher("Reposer", 20, YELLOW, (X_RecBas+40, Y_RecBas-364))


            #Gere les inputs
            for event in pygame.event.get():
                #Fermer la fenetre du jeu
                if event.type == pygame.QUIT:
                    Avancee00 = 5
                    return Avancee00, PPV_Actuel
               
                 # Si une touche est pressee, on se deplace dans le menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        SFX("navigate")
                        choix -= 1
                    if event.key == pygame.K_UP:
                        SFX("navigate")
                        choix += 1

                    #Selection du menu
                    if event.key == pygame.K_SPACE:
                        SFX("select")
                        if choix == 1: #Selection du bouton agir
                            Avancee11 = 11
                            Rec_Haut()
                            afficher("Vous travaillez toute la soiree.", 20, WHITE, (50, 40))
                            pygame.display.update() #Update l'ecran
                            valider()
                            Player["Math"] += 1
                            
                        elif choix == 2: #Selection du bouton agir
                            Avancee11 = 12
                            Rec_Haut()
                            afficher("Vous travaillez toute la soiree.", 20, WHITE, (50, 40))
                            pygame.display.update() #Update l'ecran
                            valider()
                            Player["Francais"] += 1

                        elif choix == 3: #Selection du bouton agir
                            Avancee11 = 13
                            Rec_Haut()
                            afficher("Vous travaillez toute la soiree.", 20, WHITE, (50, 40))
                            pygame.display.update() #Update l'ecran
                            valider()
                            Player["Anglais"] += 1

                        else: #Selection du bouton Option
                            Avancee11 = 14
                            Rec_Haut()
                            afficher("Vous vous reposez toute la soiree.", 20, WHITE, (50, 40))
                            PPV_Actuel = PPV
                            pygame.display.update() #Update l'ecran
                            valider()


            if choix > 4:
                choix = 4
            if choix == 0:
                return 0, PPV_Actuel

            pygame.display.update() #Update l'ecran
        
        return Avancee11, PPV_Actuel

    def Avancee2(PPV_Actuel, PPV, PATK, PDEF):
        """Le bouton inventaire. Gestion de l'inventaire du personnage"""

        #Depose les couleurs dans des variables.
        WHITE, ORANGE, ALPHA = Couleurs()
        YELLOW = [255,255,85]

        #Initialisation de variables qui seront utilisees par la suite. 
        choix = 1 #Permet de se deplacer dans le menu et de choisir un objet
        
        #Permet d'equiper un objet
            #equip = 0 => On a rien d'equipe
            #equip = 1 => On est equipe d'un stylo et de feuilles
            #equip = 2 => On est equipe d'un cahier
            #equip = 3 => On est equipe d'un tablette
            #equip = 4 => On est equipe d'une PC
        equip = 0 

        #Si quelque chose est deja equipe avant de rentrer dans le menu
        if Inventaire["Stylo et feuilles"][4] == 1:
            equip = 1
        elif Inventaire["Cahier"][4] == 1:
            equip = 2
        elif Inventaire["Tablette"][4] == 1:
            equip = 3
        elif Inventaire["PC"][4] == 1:
            equip = 4

        #Position des rectangles du bas de l'ecran
        X_RecBas = 30
        Y_RecBas = 500

        Inventaire_run = True
        #Tant que la boucle du magasin tourne
        while Inventaire_run == True :

            #Affiche le rectangle en haut de l'ecran
            Rec_Haut()

            #Les rectangles sur le bas de l'ecran
            #Rectangle agir
            window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
            afficher("Agir", 20, WHITE, (X_RecBas+60, Y_RecBas+20))
            #Rectangle Inventaire
            window_draw_rect(ORANGE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
            afficher("Inventaire", 20, ORANGE, (X_RecBas+209, Y_RecBas+20))
            #Rectangle Shop
            window_draw_rect(WHITE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
            afficher("Magasin", 20, WHITE, (X_RecBas+418, Y_RecBas+20))
            #Rectangle Options
            window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
            afficher("Autre", 20, WHITE, (X_RecBas+621, Y_RecBas+20))

            #Permet d'afficher les differents objets
            #(COLOR, ALPHA, PositionX, PositionY, Largeur, Hauteur)

            if choix == 1 : #Boisson energisante
                window_draw_rect(WHITE, ALPHA, 150, 90, 500, 390) #710 à 490   #X : 717
                #afficher("ATK +10, DEF +10").format(Inventaire["Boisson Energisante"][0], Inventaire["Boisson Energistante"][0] 20, WHITE, (60, 60)
                afficher("Restaure 10 CON.".format(Inventaire["Boisson Energisante"][0], Inventaire["Boisson Energisante"][0] ), 20, WHITE, (60, 44))
                afficher("{}x Boisson energisante".format(Inventaire["Boisson Energisante"][0]), 20, ORANGE, (180, 130))
                afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (180, 160))
                afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (180, 190))
                afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE,(180, 220))
                afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE,(180, 250))
                afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (180, 280))
                afficher("{}x Stylo et feuilles".format(Inventaire["Stylo et feuilles"][0]), 20, WHITE, (180, 310))
                afficher("{}x Cahier".format(Inventaire["Cahier"][0]), 20, WHITE, (180, 340))
                afficher("{}x Tablette".format(Inventaire["Tablette"][0]), 20, WHITE, (180, 370))
                afficher("{}x PC".format(Inventaire["PC"][0]), 20, WHITE, (180, 400))
            elif choix == 2 : #Burger
                window_draw_rect(WHITE, ALPHA, 150, 90, 500, 390)
                afficher("Redonne 20 CON.".format(Inventaire["Burger"][0], Inventaire["Burger"][0] ), 20, WHITE, (60, 44))
                afficher("{}x Boisson energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (180, 130))
                afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, ORANGE, (180, 160))
                afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (180, 190))
                afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE,(180, 220))
                afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE,(180, 250))
                afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (180, 280))
                afficher("{}x Stylo et feuilles".format(Inventaire["Stylo et feuilles"][0]), 20, WHITE, (180, 310))
                afficher("{}x Cahier".format(Inventaire["Cahier"][0]), 20, WHITE, (180, 340))
                afficher("{}x Tablette".format(Inventaire["Tablette"][0]), 20, WHITE, (180, 370))
                afficher("{}x PC".format(Inventaire["PC"][0]), 20, WHITE, (180, 400))
            elif choix == 3 : #Bubble tea
                window_draw_rect(WHITE, ALPHA, 150, 90, 500, 390)
                afficher("Redonne 50 points de CON".format(Inventaire["Bubble Tea"][0], Inventaire["Bubble Tea"][0] ), 20, WHITE, (60, 44))
                afficher("{}x Boisson energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (180, 130))
                afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (180, 160))
                afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, ORANGE, (180, 190))
                afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE,(180, 220))
                afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE,(180, 250))
                afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (180, 280))
                afficher("{}x Stylo et feuilles".format(Inventaire["Stylo et feuilles"][0]), 20, WHITE, (180, 310))
                afficher("{}x Cahier".format(Inventaire["Cahier"][0]), 20, WHITE, (180, 340))
                afficher("{}x Tablette".format(Inventaire["Tablette"][0]), 20, WHITE, (180, 370))
                afficher("{}x PC".format(Inventaire["PC"][0]), 20, WHITE, (180, 400))
            elif choix == 4 : #Dessert au chocolat
                window_draw_rect(WHITE, ALPHA, 150, 90, 500, 390)
                afficher("Redonne 100 points de CON".format(Inventaire["Dessert au Chocolat"][0], Inventaire["Dessert au Chocolat"][0] ), 20, WHITE, (60, 44))
                afficher("{}x Boisson energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (180, 130))
                afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (180, 160))
                afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (180, 190))
                afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, ORANGE,(180, 220))
                afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE,(180, 250))
                afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (180, 280))
                afficher("{}x Stylo et feuilles".format(Inventaire["Stylo et feuilles"][0]), 20, WHITE, (180, 310))
                afficher("{}x Cahier".format(Inventaire["Cahier"][0]), 20, WHITE, (180, 340))
                afficher("{}x Tablette".format(Inventaire["Tablette"][0]), 20, WHITE, (180, 370))
                afficher("{}x PC".format(Inventaire["PC"][0]), 20, WHITE, (180, 400))
            elif choix == 5: #Café
                window_draw_rect(WHITE, ALPHA, 150, 90, 500, 390)
                afficher("Productivite +20%".format(Inventaire["Cafe"][0], Inventaire["Cafe"][0] ), 20, WHITE, (60, 44))
                afficher("{}x Boisson energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (180, 130))
                afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (180, 160))
                afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (180, 190))
                afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE,(180, 220))
                afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, ORANGE,(180, 250))
                afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (180, 280))
                afficher("{}x Stylo et feuilles".format(Inventaire["Stylo et feuilles"][0]), 20, WHITE, (180, 310))
                afficher("{}x Cahier".format(Inventaire["Cahier"][0]), 20, WHITE, (180, 340))
                afficher("{}x Tablette".format(Inventaire["Tablette"][0]), 20, WHITE, (180, 370))
                afficher("{}x PC".format(Inventaire["PC"][0]), 20, WHITE, (180, 400))
            elif choix == 6 : #The
                window_draw_rect(WHITE, ALPHA, 150, 90, 500, 390)
                afficher("Discipline +20%".format(Inventaire["The"][0], Inventaire["The"][0] ), 20, WHITE, (60, 44))
                afficher("{}x Boisson energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (180, 130))
                afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (180, 160))
                afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (180, 190))
                afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE,(180, 220))
                afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE,(180, 250))
                afficher("{}x The".format(Inventaire["The"][0]), 20, ORANGE, (180, 280))
                afficher("{}x Stylo et feuilles".format(Inventaire["Stylo et feuilles"][0]), 20, WHITE, (180, 310))
                afficher("{}x Cahier".format(Inventaire["Cahier"][0]), 20, WHITE, (180, 340))
                afficher("{}x Tablette".format(Inventaire["Tablette"][0]), 20, WHITE, (180, 370))
                afficher("{}x PC".format(Inventaire["PC"][0]), 20, WHITE, (180, 400))
            elif choix == 7 : #Stylo et feuilles
                window_draw_rect(WHITE, ALPHA, 150, 90, 500, 390)
                afficher("Equipement | ATK +10% DEF +10%".format(Inventaire["Stylo et feuilles"][0], Inventaire["Stylo et feuilles"][0] ), 20, WHITE, (60, 44))
                afficher("{}x Boisson energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (180, 130))
                afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (180, 160))
                afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (180, 190))
                afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE,(180, 220))
                afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE,(180, 250))
                afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (180, 280))
                afficher("{}x Stylo et feuilles".format(Inventaire["Stylo et feuilles"][0]), 20, ORANGE, (180, 310))
                afficher("{}x Cahier".format(Inventaire["Cahier"][0]), 20, WHITE, (180, 340))
                afficher("{}x Tablette".format(Inventaire["Tablette"][0]), 20, WHITE, (180, 370))
                afficher("{}x PC".format(Inventaire["PC"][0]), 20, WHITE, (180, 400))
            elif choix == 8 : #Cahier
                window_draw_rect(WHITE, ALPHA, 150, 90, 500, 390)
                afficher("Equipement | ATK +20% DEF +20%".format(Inventaire["Cahier"][0], Inventaire["Cahier"][0] ), 20, WHITE, (60, 44))
                afficher("{}x Boisson energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (180, 130))
                afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (180, 160))
                afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (180, 190))
                afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE,(180, 220))
                afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE,(180, 250))
                afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (180, 280))
                afficher("{}x Stylo et feuilles".format(Inventaire["Stylo et feuilles"][0]), 20, WHITE, (180, 310))
                afficher("{}x Cahier".format(Inventaire["Cahier"][0]), 20, ORANGE, (180, 340))
                afficher("{}x Tablette".format(Inventaire["Tablette"][0]), 20, WHITE, (180, 370))
                afficher("{}x PC".format(Inventaire["PC"][0]), 20, WHITE, (180, 400))
            elif choix == 9 : #Tablette
                window_draw_rect(WHITE, ALPHA, 150, 90, 500, 390)
                afficher("Equipement | ATK +40%".format(Inventaire["Tablette"][0], Inventaire["Tablette"][0] ), 20, WHITE, (60, 44))
                afficher("{}x Boisson energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (180, 130))
                afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (180, 160))
                afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (180, 190))
                afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE,(180, 220))
                afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE,(180, 250))
                afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (180, 280))
                afficher("{}x Stylo et feuilles".format(Inventaire["Stylo et feuilles"][0]), 20, WHITE, (180, 310))
                afficher("{}x Cahier".format(Inventaire["Cahier"][0]), 20, WHITE, (180, 340))
                afficher("{}x Tablette".format(Inventaire["Tablette"][0]), 20, ORANGE, (180, 370))
                afficher("{}x PC".format(Inventaire["PC"][0]), 20, WHITE, (180, 400))
            elif choix == 10 : #PC
                window_draw_rect(WHITE, ALPHA, 150, 90, 500, 390)
                afficher("Equipement | ATK +50%".format(ceil(Inventaire["PC"][0]), Inventaire["PC"][0] ), 20, WHITE, (60, 44))
                afficher("{}x Boisson energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (180, 130))
                afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (180, 160))
                afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (180, 190))
                afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE,(180, 220))
                afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE,(180, 250))
                afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (180, 280))
                afficher("{}x Stylo et feuilles".format(Inventaire["Stylo et feuilles"][0]), 20, WHITE, (180, 310))
                afficher("{}x Cahier".format(Inventaire["Cahier"][0]), 20, WHITE, (180, 340))
                afficher("{}x Tablette".format(Inventaire["Tablette"][0]), 20, WHITE, (180, 370))
                afficher("{}x PC".format(Inventaire["PC"][0]), 20, ORANGE, (180, 400))

            #Permet de montrer si un equipement est equipe ou non en affichant [E] a cote des objets equipes
            if equip == 1: #Stylo et feuilles
                afficher("[E]", 20, ORANGE, (463, 310)) #60 190    #old : 350 280
            elif equip == 2: #Cahier
                afficher("[E]", 20, ORANGE, (315, 340)) #220 310
            elif equip == 3: #Tablette
                afficher("[E]", 20, ORANGE, (345, 370)) #230 340
            elif equip == 4: #PC
                afficher("[E]", 20, ORANGE, (257, 400)) #145 370

            #Gere les inputs
            for event in pygame.event.get():
                #Fermer la fenetre du jeu
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # Si une touche est pressee, on se deplace dans le menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        choix -= 1
                        SFX("navigate")
                    if event.key == pygame.K_DOWN:
                        choix += 1
                        SFX("navigate")
                
                    #Permet de selectionner un objet et de l'utiliser
                    if event.key == pygame.K_SPACE:
                        #Si on se trouve sur la boisson energisante et que sa quantite est superieure a 1
                        if choix == 1 and Inventaire["Boisson Energisante"][0] >= 1:
                            SFX("item")
                            #Diminue quantite de 1
                            Inventaire["Boisson Energisante"][0] -= 1
                            #Si la sante du personnage apres les soins est superieure a la sante max
                            if PPV_Actuel + Inventaire["Boisson Energisante"][3] > PPV:
                                #La sante actuelle du joueur a pour valeur la sante max
                                PPV_Actuel = PPV
                            #Sinon, si la sante du joueur apres les soins est inferieure a la sante max
                            else:
                                #L'objet soigne le joueur normalement
                                PPV_Actuel += Inventaire["Boisson Energisante"][3]
                        
                        #Si on se trouve sur la boisson energisante mais que la quantite est egale a 0. Recharge l'ecran et le message du haut change
                        elif choix == 1 and Inventaire["Boisson Energisante"][0] < 1:
                            SFX("error")
                            Rec_Haut()

                            #Les rectangles sur le bas de l'ecran
                            #Rectangle agir
                            window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
                            afficher("Agir", 20, WHITE, (X_RecBas+60, Y_RecBas+20))
                            #Rectangle Inventaire
                            window_draw_rect(ORANGE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
                            afficher("Inventaire", 20, ORANGE, (X_RecBas+209, Y_RecBas+20))
                            #Rectangle Shop
                            window_draw_rect(WHITE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
                            afficher("Magasin", 20, WHITE, (X_RecBas+418, Y_RecBas+20))
                            #Rectangle Options
                            window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
                            afficher("Autre", 20, WHITE, (X_RecBas+621, Y_RecBas+20))

                            window_draw_rect(WHITE, ALPHA, 150, 90, 500, 390)

                            afficher("Vous n'en avez plus.", 20, WHITE, (60, 44))
                            afficher("{}x Boisson energisante".format(Inventaire["Boisson Energisante"][0]), 20, ORANGE, (180, 130))
                            afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (180, 160))
                            afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (180, 190))
                            afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE,(180, 220))
                            afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE,(180, 250))
                            afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (180, 280))
                            afficher("{}x Stylo et feuilles".format(Inventaire["Stylo et feuilles"][0]), 20, WHITE, (180, 310))
                            afficher("{}x Cahier".format(Inventaire["Cahier"][0]), 20, WHITE, (180, 340))
                            afficher("{}x Tablette".format(Inventaire["Tablette"][0]), 20, WHITE, (180, 370))
                            afficher("{}x PC".format(Inventaire["PC"][0]), 20, WHITE, (180, 400))

                            #Permet de montrer si un equipement est equipe ou non en affichant [E] a cote des objets equipes
                            if equip == 1: #Stylo et feuilles
                                afficher("[E]", 20, ORANGE, (463, 310)) #60 190    #old : 350 280
                            elif equip == 2: #Cahier
                                afficher("[E]", 20, ORANGE, (315, 340)) #220 310
                            elif equip == 3: #Tablette
                                afficher("[E]", 20, ORANGE, (345, 370)) #230 340
                            elif equip == 4: #PC
                                afficher("[E]", 20, ORANGE, (257, 400)) #145 370

                            pygame.display.update()
                            valider()


                        #Si on se trouve sur le burger
                        elif choix == 2 and Inventaire["Burger"][0] >= 1:
                            SFX("item")
                            #Diminue quantite de 1
                            Inventaire["Burger"][0] -= 1
                            if PPV_Actuel + Inventaire["Burger"][3] > PPV:
                                PPV_Actuel = PPV
                            else:
                                PPV_Actuel += Inventaire["Burger"][3]
                        
                        elif choix == 2 and Inventaire["Burger"][0] < 1:
                            SFX("error")
                            Rec_Haut()

                            #Les rectangles sur le bas de l'ecran
                            #Rectangle agir
                            window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
                            afficher("Agir", 20, WHITE, (X_RecBas+60, Y_RecBas+20))
                            #Rectangle Inventaire
                            window_draw_rect(ORANGE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
                            afficher("Inventaire", 20, ORANGE, (X_RecBas+209, Y_RecBas+20))
                            #Rectangle Shop
                            window_draw_rect(WHITE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
                            afficher("Magasin", 20, WHITE, (X_RecBas+418, Y_RecBas+20))
                            #Rectangle Options
                            window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
                            afficher("Autre", 20, WHITE, (X_RecBas+621, Y_RecBas+20))

                            window_draw_rect(WHITE, ALPHA, 150, 90, 500, 390)

                            afficher("Vous n'en avez plus.", 20, WHITE, (60, 44))
                            afficher("{}x Boisson energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (180, 130))
                            afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, ORANGE, (180, 160))
                            afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (180, 190))
                            afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE,(180, 220))
                            afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE,(180, 250))
                            afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (180, 280))
                            afficher("{}x Stylo et feuilles".format(Inventaire["Stylo et feuilles"][0]), 20, WHITE, (180, 310))
                            afficher("{}x Cahier".format(Inventaire["Cahier"][0]), 20, WHITE, (180, 340))
                            afficher("{}x Tablette".format(Inventaire["Tablette"][0]), 20, WHITE, (180, 370))
                            afficher("{}x PC".format(Inventaire["PC"][0]), 20, WHITE, (180, 400))

                            #Permet de montrer si un equipement est equipe ou non en affichant [E] a cote des objets equipes
                            if equip == 1: #Stylo et feuilles
                                afficher("[E]", 20, ORANGE, (463, 310)) #60 190    #old : 350 280
                            elif equip == 2: #Cahier
                                afficher("[E]", 20, ORANGE, (315, 340)) #220 310
                            elif equip == 3: #Tablette
                                afficher("[E]", 20, ORANGE, (345, 370)) #230 340
                            elif equip == 4: #PC
                                afficher("[E]", 20, ORANGE, (257, 400)) #145 370

                            pygame.display.update()
                            valider()

                         #Si on se trouve sur le bubble tea
                        elif choix == 3 and Inventaire["Bubble Tea"][0] >= 1:
                            SFX("item")
                            Inventaire["Bubble Tea"][0] -= 1
                            if PPV_Actuel + Inventaire["Bubble Tea"][3] > PPV:
                                PPV_Actuel = PPV
                            else:
                                PPV_Actuel += Inventaire["Bubble Tea"][3]

                        elif choix == 3 and Inventaire ["Bubble Tea"][0] < 1:
                            SFX("error")
                            Rec_Haut()

                            #Les rectangles sur le bas de l'ecran
                            #Rectangle agir
                            window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
                            afficher("Agir", 20, WHITE, (X_RecBas+60, Y_RecBas+20))
                            #Rectangle Inventaire
                            window_draw_rect(ORANGE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
                            afficher("Inventaire", 20, ORANGE, (X_RecBas+209, Y_RecBas+20))
                            #Rectangle Shop
                            window_draw_rect(WHITE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
                            afficher("Magasin", 20, WHITE, (X_RecBas+418, Y_RecBas+20))
                            #Rectangle Options
                            window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
                            afficher("Autre", 20, WHITE, (X_RecBas+621, Y_RecBas+20))

                            window_draw_rect(WHITE, ALPHA, 150, 90, 500, 390)

                            afficher("Vous n'en avez plus.", 20, WHITE, (60, 44))
                            afficher("{}x Boisson energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (180, 130))
                            afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (180, 160))
                            afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, ORANGE, (180, 190))
                            afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE,(180, 220))
                            afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE,(180, 250))
                            afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (180, 280))
                            afficher("{}x Stylo et feuilles".format(Inventaire["Stylo et feuilles"][0]), 20, WHITE, (180, 310))
                            afficher("{}x Cahier".format(Inventaire["Cahier"][0]), 20, WHITE, (180, 340))
                            afficher("{}x Tablette".format(Inventaire["Tablette"][0]), 20, WHITE, (180, 370))
                            afficher("{}x PC".format(Inventaire["PC"][0]), 20, WHITE, (180, 400))

                            #Permet de montrer si un equipement est equipe ou non en affichant [E] a cote des objets equipes
                            if equip == 1: #Stylo et feuilles
                                afficher("[E]", 20, ORANGE, (463, 310)) #60 190    #old : 350 280
                            elif equip == 2: #Cahier
                                afficher("[E]", 20, ORANGE, (315, 340)) #220 310
                            elif equip == 3: #Tablette
                                afficher("[E]", 20, ORANGE, (345, 370)) #230 340
                            elif equip == 4: #PC
                                afficher("[E]", 20, ORANGE, (257, 400)) #145 370

                            pygame.display.update()
                            valider()

                         #Si on se trouve sur le Dessert au Chocolat
                        elif choix == 4 and Inventaire["Dessert au Chocolat"][0] >= 1:
                            SFX("item")
                            Inventaire["Dessert au Chocolat"][0] -= 1
                            if PPV_Actuel + Inventaire["Dessert au Chocolat"][3] > PPV:
                                PPV_Actuel = PPV
                            else:
                                PPV_Actuel += Inventaire["Dessert au Chocolat"][3]
                        elif choix == 4 and Inventaire ["Dessert au Chocolat"][0] < 1:
                            SFX("error")
                            Rec_Haut()

                            #Les rectangles sur le bas de l'ecran
                            #Rectangle agir
                            window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
                            afficher("Agir", 20, WHITE, (X_RecBas+60, Y_RecBas+20))
                            #Rectangle Inventaire
                            window_draw_rect(ORANGE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
                            afficher("Inventaire", 20, ORANGE, (X_RecBas+209, Y_RecBas+20))
                            #Rectangle Shop
                            window_draw_rect(WHITE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
                            afficher("Magasin", 20, WHITE, (X_RecBas+418, Y_RecBas+20))
                            #Rectangle Options
                            window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
                            afficher("Autre", 20, WHITE, (X_RecBas+621, Y_RecBas+20))

                            window_draw_rect(WHITE, ALPHA, 150, 90, 500, 390)
                            
                            afficher("Vous n'en avez plus.", 20, WHITE, (60, 44))
                            afficher("{}x Boisson energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (180, 130))
                            afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (180, 160))
                            afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (180, 190))
                            afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, ORANGE,(180, 220))
                            afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE,(180, 250))
                            afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (180, 280))
                            afficher("{}x Stylo et feuilles".format(Inventaire["Stylo et feuilles"][0]), 20, WHITE, (180, 310))
                            afficher("{}x Cahier".format(Inventaire["Cahier"][0]), 20, WHITE, (180, 340))
                            afficher("{}x Tablette".format(Inventaire["Tablette"][0]), 20, WHITE, (180, 370))
                            afficher("{}x PC".format(Inventaire["PC"][0]), 20, WHITE, (180, 400))

                            #Permet de montrer si un equipement est equipe ou non en affichant [E] a cote des objets equipes
                            if equip == 1: #Stylo et feuilles
                                afficher("[E]", 20, ORANGE, (463, 310)) #60 190    #old : 350 280
                            elif equip == 2: #Cahier
                                afficher("[E]", 20, ORANGE, (315, 340)) #220 310
                            elif equip == 3: #Tablette
                                afficher("[E]", 20, ORANGE, (345, 370)) #230 340
                            elif equip == 4: #PC
                                afficher("[E]", 20, ORANGE, (257, 400)) #145 370

                            pygame.display.update()
                            valider()


                         #Si on se trouve sur le cafe
                        elif choix == 5 and Inventaire["Cafe"][0] >= 1:

                            SFX("error")

                            Rec_Haut()

                            #Les rectangles sur le bas de l'ecran
                            #Rectangle agir
                            window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
                            afficher("Agir", 20, WHITE, (X_RecBas+60, Y_RecBas+20))
                            #Rectangle Inventaire
                            window_draw_rect(ORANGE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
                            afficher("Inventaire", 20, ORANGE, (X_RecBas+209, Y_RecBas+20))
                            #Rectangle Shop
                            window_draw_rect(WHITE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
                            afficher("Magasin", 20, WHITE, (X_RecBas+418, Y_RecBas+20))
                            #Rectangle Options
                            window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
                            afficher("Autre", 20, WHITE, (X_RecBas+621, Y_RecBas+20))

                            window_draw_rect(WHITE, ALPHA, 150, 90, 500, 390)

                            afficher("Consommable en combat uniquement.", 20, WHITE, (60, 44))
                            afficher("{}x Boisson energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (180, 130))
                            afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (180, 160))
                            afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (180, 190))
                            afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE,(180, 220))
                            afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, ORANGE,(180, 250))
                            afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (180, 280))
                            afficher("{}x Stylo et feuilles".format(Inventaire["Stylo et feuilles"][0]), 20, WHITE, (180, 310))
                            afficher("{}x Cahier".format(Inventaire["Cahier"][0]), 20, WHITE, (180, 340))
                            afficher("{}x Tablette".format(Inventaire["Tablette"][0]), 20, WHITE, (180, 370))
                            afficher("{}x PC".format(Inventaire["PC"][0]), 20, WHITE, (180, 400))

                            #Permet de montrer si un equipement est equipe ou non en affichant [E] a cote des objets equipes
                            if equip == 1: #Stylo et feuilles
                                afficher("[E]", 20, ORANGE, (463, 310)) #60 190    #old : 350 280
                            elif equip == 2: #Cahier
                                afficher("[E]", 20, ORANGE, (315, 340)) #220 310
                            elif equip == 3: #Tablette
                                afficher("[E]", 20, ORANGE, (345, 370)) #230 340
                            elif equip == 4: #PC
                                afficher("[E]", 20, ORANGE, (257, 400)) #145 370

                            pygame.display.update()
                            valider()


                         #Si on se trouve sur le the
                        
                        elif choix == 6 and Inventaire["The"][0] >= 1:

                            SFX("error")
                            Rec_Haut()

                            #Les rectangles sur le bas de l'ecran
                            #Rectangle agir
                            window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
                            afficher("Agir", 20, WHITE, (X_RecBas+60, Y_RecBas+20))
                            #Rectangle Inventaire
                            window_draw_rect(ORANGE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
                            afficher("Inventaire", 20, ORANGE, (X_RecBas+209, Y_RecBas+20))
                            #Rectangle Shop
                            window_draw_rect(WHITE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
                            afficher("Magasin", 20, WHITE, (X_RecBas+418, Y_RecBas+20))
                            #Rectangle Options
                            window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
                            afficher("Autre", 20, WHITE, (X_RecBas+621, Y_RecBas+20))

                            window_draw_rect(WHITE, ALPHA, 150, 90, 500, 390)

                            afficher("Consommable en combat uniquement.", 20, WHITE, (60, 44))
                            afficher("{}x Boisson energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (180, 130))
                            afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (180, 160))
                            afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (180, 190))
                            afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE,(180, 220))
                            afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE,(180, 250))
                            afficher("{}x The".format(Inventaire["The"][0]), 20, ORANGE, (180, 280))
                            afficher("{}x Stylo et feuilles".format(Inventaire["Stylo et feuilles"][0]), 20, WHITE, (180, 310))
                            afficher("{}x Cahier".format(Inventaire["Cahier"][0]), 20, WHITE, (180, 340))
                            afficher("{}x Tablette".format(Inventaire["Tablette"][0]), 20, WHITE, (180, 370))
                            afficher("{}x PC".format(Inventaire["PC"][0]), 20, WHITE, (180, 400))

                            #Permet de montrer si un equipement est equipe ou non en affichant [E] a cote des objets equipes
                            if equip == 1: #Stylo et feuilles
                                afficher("[E]", 20, ORANGE, (463, 310)) #60 190    #old : 350 280
                            elif equip == 2: #Cahier
                                afficher("[E]", 20, ORANGE, (315, 340)) #220 310
                            elif equip == 3: #Tablette
                                afficher("[E]", 20, ORANGE, (345, 370)) #230 340
                            elif equip == 4: #PC
                                afficher("[E]", 20, ORANGE, (257, 400)) #145 370

                            pygame.display.update()
                            valider()


                        #__________Les equipements__________

                        #Le stylo et les feuilles
                        #Equiper
                        if choix == 7 and Inventaire["Stylo et feuilles"][0] >= 1 and Inventaire["Stylo et feuilles"][4] == 0:
                            SFX("defense")
                            PATK, PDEF = PStatsIni(PATK, PDEF, 1)
                            equip = 1
                        #Desequiper
                        elif choix == 7 and Inventaire["Stylo et feuilles"][0] >= 1 and Inventaire["Stylo et feuilles"][4] == 1:
                            PATK, PDEF = PStatsIni(PATK, PDEF, 0)
                            equip = 0

                        #Si on n'a plus de stylo et feuilles
                        elif choix == 7 and Inventaire["Stylo et feuilles"][0] < 1:
                            SFX("error")
                            Rec_Haut()

                            #Les rectangles sur le bas de l'ecran
                            #Rectangle agir
                            window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
                            afficher("Agir", 20, WHITE, (X_RecBas+60, Y_RecBas+20))
                            #Rectangle Inventaire
                            window_draw_rect(ORANGE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
                            afficher("Inventaire", 20, ORANGE, (X_RecBas+209, Y_RecBas+20))
                            #Rectangle Shop
                            window_draw_rect(WHITE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
                            afficher("Magasin", 20, WHITE, (X_RecBas+418, Y_RecBas+20))
                            #Rectangle Options
                            window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
                            afficher("Autre", 20, WHITE, (X_RecBas+621, Y_RecBas+20))

                            window_draw_rect(WHITE, ALPHA, 150, 90, 500, 390)

                            afficher("Vous n'en avez plus.", 20, WHITE, (60, 44))
                            afficher("{}x Boisson energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (180, 130))
                            afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (180, 160))
                            afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (180, 190))
                            afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE,(180, 220))
                            afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE,(180, 250))
                            afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (180, 280))
                            afficher("{}x Stylo et feuilles".format(Inventaire["Stylo et feuilles"][0]), 20, ORANGE, (180, 310))
                            afficher("{}x Cahier".format(Inventaire["Cahier"][0]), 20, WHITE, (180, 340))
                            afficher("{}x Tablette".format(Inventaire["Tablette"][0]), 20, WHITE, (180, 370))
                            afficher("{}x PC".format(Inventaire["PC"][0]), 20, WHITE, (180, 400))

                            #Permet de montrer si un equipement est equipe ou non en affichant [E] a cote des objets equipes
                            if equip == 1: #Stylo et feuilles
                                afficher("[E]", 20, ORANGE, (463, 310)) #60 190    #old : 350 280
                            elif equip == 2: #Cahier
                                afficher("[E]", 20, ORANGE, (315, 340)) #220 310
                            elif equip == 3: #Tablette
                                afficher("[E]", 20, ORANGE, (345, 370)) #230 340
                            elif equip == 4: #PC
                                afficher("[E]", 20, ORANGE, (257, 400)) #145 370

                            pygame.display.update()
                            valider()

                        #Le cahier
                        #Equiper
                        if choix == 8 and Inventaire["Cahier"][0] >= 1 and Inventaire["Cahier"][4] == 0:
                            SFX("defense")
                            PATK, PDEF = PStatsIni(PATK, PDEF, 2)
                            equip = 2

                        #Si on n'a plus de cahier
                        elif choix == 8 and Inventaire["Cahier"][0] < 1:
                            SFX("error")
                            Rec_Haut()

                            #Les rectangles sur le bas de l'ecran
                            #Rectangle agir
                            window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
                            afficher("Agir", 20, WHITE, (X_RecBas+60, Y_RecBas+20))
                            #Rectangle Inventaire
                            window_draw_rect(ORANGE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
                            afficher("Inventaire", 20, ORANGE, (X_RecBas+209, Y_RecBas+20))
                            #Rectangle Shop
                            window_draw_rect(WHITE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
                            afficher("Magasin", 20, WHITE, (X_RecBas+418, Y_RecBas+20))
                            #Rectangle Options
                            window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
                            afficher("Autre", 20, WHITE, (X_RecBas+621, Y_RecBas+20))

                            window_draw_rect(WHITE, ALPHA, 150, 90, 500, 390)

                            afficher("Vous n'en avez plus.", 20, WHITE, (60, 44))
                            afficher("{}x Boisson energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (180, 130))
                            afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (180, 160))
                            afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (180, 190))
                            afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE,(180, 220))
                            afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE,(180, 250))
                            afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (180, 280))
                            afficher("{}x Stylo et feuilles".format(Inventaire["Stylo et feuilles"][0]), 20, WHITE, (180, 310))
                            afficher("{}x Cahier".format(Inventaire["Cahier"][0]), 20, ORANGE, (180, 340))
                            afficher("{}x Tablette".format(Inventaire["Tablette"][0]), 20, WHITE, (180, 370))
                            afficher("{}x PC".format(Inventaire["PC"][0]), 20, WHITE, (180, 400))

                            #Permet de montrer si un equipement est equipe ou non en affichant [E] a cote des objets equipes
                            if equip == 1: #Stylo et feuilles
                                afficher("[E]", 20, ORANGE, (463, 310)) #60 190    #old : 350 280
                            elif equip == 2: #Cahier
                                afficher("[E]", 20, ORANGE, (315, 340)) #220 310
                            elif equip == 3: #Tablette
                                afficher("[E]", 20, ORANGE, (345, 370)) #230 340
                            elif equip == 4: #PC
                                afficher("[E]", 20, ORANGE, (257, 400)) #145 370

                            pygame.display.update()
                            valider()
 
                        #Desequiper
                        elif choix == 8 and Inventaire["Cahier"][0] >= 1 and Inventaire["Cahier"][4] == 1:
                            PATK, PDEF = PStatsIni(PATK, PDEF, 0)
                            equip = 0

                        #La tablette
                        #Equiper
                        if choix == 9 and Inventaire["Tablette"][0] >= 1 and Inventaire["Tablette"][4] == 0:
                            SFX("defense")
                            PATK, PDEF = PStatsIni(PATK, PDEF, 3)
                            equip = 3

                        #Si on n'a plus de tablette
                        elif choix == 9 and Inventaire["Tablette"][0] < 1:
                            SFX("error")
                            Rec_Haut()

                            #Les rectangles sur le bas de l'ecran
                            #Rectangle agir
                            window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
                            afficher("Agir", 20, WHITE, (X_RecBas+60, Y_RecBas+20))
                            #Rectangle Inventaire
                            window_draw_rect(ORANGE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
                            afficher("Inventaire", 20, ORANGE, (X_RecBas+209, Y_RecBas+20))
                            #Rectangle Shop
                            window_draw_rect(WHITE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
                            afficher("Magasin", 20, WHITE, (X_RecBas+418, Y_RecBas+20))
                            #Rectangle Options
                            window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
                            afficher("Autre", 20, WHITE, (X_RecBas+621, Y_RecBas+20))

                            window_draw_rect(WHITE, ALPHA, 150, 90, 500, 390)

                            afficher("Vous n'en avez plus.", 20, WHITE, (60, 44))
                            afficher("{}x Boisson energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (180, 130))
                            afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (180, 160))
                            afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (180, 190))
                            afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE,(180, 220))
                            afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE,(180, 250))
                            afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (180, 280))
                            afficher("{}x Stylo et feuilles".format(Inventaire["Stylo et feuilles"][0]), 20, WHITE, (180, 310))
                            afficher("{}x Cahier".format(Inventaire["Cahier"][0]), 20, WHITE, (180, 340))
                            afficher("{}x Tablette".format(Inventaire["Tablette"][0]), 20, ORANGE, (180, 370))
                            afficher("{}x PC".format(Inventaire["PC"][0]), 20, WHITE, (180, 400))

                            #Permet de montrer si un equipement est equipe ou non en affichant [E] a cote des objets equipes
                            if equip == 1: #Stylo et feuilles
                                afficher("[E]", 20, ORANGE, (463, 310)) #60 190    #old : 350 280
                            elif equip == 2: #Cahier
                                afficher("[E]", 20, ORANGE, (315, 340)) #220 310
                            elif equip == 3: #Tablette
                                afficher("[E]", 20, ORANGE, (345, 370)) #230 340
                            elif equip == 4: #PC
                                afficher("[E]", 20, ORANGE, (257, 400)) #145 370

                            pygame.display.update()
                            valider()

                        #Desequiper
                        elif choix == 9 and Inventaire["Tablette"][0] >= 1 and Inventaire["Tablette"][4] == 1:
                            PATK, PDEF = PStatsIni(PATK, PDEF, 0)
                            equip = 0

                        #Le PC
                        #Equiper
                        if choix == 10 and Inventaire["PC"][0] >= 1 and Inventaire["PC"][4] == 0:
                            SFX("defense")
                            PATK, PDEF = PStatsIni(PATK, PDEF, 4)
                            equip = 4
                        #Desequiper
                        elif choix == 10 and Inventaire["PC"][0] >= 1 and Inventaire["PC"][4] == 1:
                            PATK, PDEF = PStatsIni(PATK, PDEF, 0)
                            equip = 0

                        #Si on n'a plus de PC
                        elif choix == 10 and Inventaire["PC"][0] < 1:
                            SFX("error")
                            Rec_Haut()
                            #Les rectangles sur le bas de l'ecran
                            #Rectangle agir
                            window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
                            afficher("Agir", 20, WHITE, (X_RecBas+60, Y_RecBas+20))
                            #Rectangle Inventaire
                            window_draw_rect(ORANGE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
                            afficher("Inventaire", 20, ORANGE, (X_RecBas+209, Y_RecBas+20))
                            #Rectangle Shop
                            window_draw_rect(WHITE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
                            afficher("Magasin", 20, WHITE, (X_RecBas+418, Y_RecBas+20))
                            #Rectangle Options
                            window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
                            afficher("Autre", 20, WHITE, (X_RecBas+621, Y_RecBas+20))

                            window_draw_rect(WHITE, ALPHA, 150, 90, 500, 390)

                            afficher("Vous n'en avez plus.", 20, WHITE, (60, 44))
                            afficher("{}x Boisson energisante".format(Inventaire["Boisson Energisante"][0]), 20, WHITE, (180, 130))
                            afficher("{}x Burger".format(Inventaire["Burger"][0]), 20, WHITE, (180, 160))
                            afficher("{}x Bubble Tea".format(Inventaire["Bubble Tea"][0]), 20, WHITE, (180, 190))
                            afficher("{}x Dessert au Chocolat".format(Inventaire["Dessert au Chocolat"][0]), 20, WHITE,(180, 220))
                            afficher("{}x Cafe".format(Inventaire["Cafe"][0]), 20, WHITE,(180, 250))
                            afficher("{}x The".format(Inventaire["The"][0]), 20, WHITE, (180, 280))
                            afficher("{}x Stylo et feuilles".format(Inventaire["Stylo et feuilles"][0]), 20, WHITE, (180, 310))
                            afficher("{}x Cahier".format(Inventaire["Cahier"][0]), 20, WHITE, (180, 340))
                            afficher("{}x Tablette".format(Inventaire["Tablette"][0]), 20, WHITE, (180, 370))
                            afficher("{}x PC".format(Inventaire["PC"][0]), 20, ORANGE, (180, 400))

                            #Permet de montrer si un equipement est equipe ou non en affichant [E] a cote des objets equipes
                            if equip == 1: #Stylo et feuilles
                                afficher("[E]", 20, ORANGE, (463, 310)) #60 190    #old : 350 280
                            elif equip == 2: #Cahier
                                afficher("[E]", 20, ORANGE, (315, 340)) #220 310
                            elif equip == 3: #Tablette
                                afficher("[E]", 20, ORANGE, (345, 370)) #230 340
                            elif equip == 4: #PC
                                afficher("[E]", 20, ORANGE, (257, 400)) #145 370

                            pygame.display.update()
                            valider()

            if choix < 1:
                choix = 1
            if choix == 11:
                return 0, PPV_Actuel, PATK, PDEF

            pygame.display.update() #Update l'ecran

    def Avancee3(PARGENT):
        """Menu du magasin, on peut acheter et vendre des objets."""

        #Depose les couleurs dans des variables.
        WHITE, ORANGE, ALPHA = Couleurs()
        YELLOW = [255,255,85]
   
        #Joue la musique du magasin
        Music("mag")

        #Affiche le fond et le rectangle en haut de l'ecran
        def Rec_Haut_mag():
            """Gere l'affichage du rectangle en haut de l'ecran"""

            WHITE, ORANGE, ALPHA = Couleurs()
            #Affiche le background
            background = pygame.image.load('Assets/Menu_de_navigation/Background/shop_backgroun_v1.png')
            screen.blit(background, (-195, 0))

            #Rectangle du haut, qui affiche des messages en fonctions de ce qu'on regarde
            window_draw_rect(WHITE, ALPHA, 40, 40, 715, 60)

        def Acheter(PARGENT):
            """Permet d'acheter des objets"""

            #Initialisation des variables
            choix = 1

            #Depose les couleurs dans des variables.
            WHITE, ORANGE, ALPHA = Couleurs()
            YELLOW = [255,255,85]

            def load_page():
                """Affiche tout ce qu'il y a a afficher sur la page d'achat du magasin."""

                #Affiche le fond et le rectangle en haut de l'ecran
                Rec_Haut_mag()

                #Dessine tous les rectangles en haut de l'ecran
                window_draw_rect(WHITE, ALPHA, 540, 130, 215, 60)
                window_draw_rect(WHITE, ALPHA, 190, 130, 150, 60)
                window_draw_rect(WHITE, ALPHA, 340, 130, 150, 60)
                window_draw_rect(ORANGE, ALPHA, 40, 130, 150, 60)
                afficher("Acheter", 20, ORANGE, (67, 150))
                afficher("Vendre", 20, WHITE, (217, 150))
                afficher("Quitter", 20, WHITE, (367, 150))
                afficher("Argent : {}".format(PARGENT), 20, WHITE, (560, 150))

                #Dessine la fenetre qui contiendra tous les elements du shop
                window_draw_rect(WHITE, ALPHA, 40, 220, 490, 330)


            #Boucle qui tourne tant qu'on se trouve dans le bouton "Acheter"
            Acheter_run = True
            while Acheter_run == True:

                load_page()

                #Affiche les differents objets du magasin
                #Boisson energisante
                if choix == 1:
                    afficher("Redonne {} points de CON. (Possede : {})".format(Inventaire["Boisson Energisante"][3], Inventaire["Boisson Energisante"][0] ), 20, WHITE, (60, 60))
                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][5]), 20, ORANGE, (60, 240))
                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][5]), 20, WHITE, (60, 270))
                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][5]), 20, WHITE, (60, 300))
                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][5]), 20, WHITE, (60, 330))
                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][5]), 20, WHITE, (60, 360))
                    afficher("The................................ {} euros".format(Inventaire["The"][5]), 20, WHITE, (60, 390))
                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][5]), 20, WHITE, (60, 420))
                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][5]), 20, WHITE, (60, 450))
                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][5]), 20, WHITE, (60, 480))
                    afficher("PC.................................. {} euros".format(Inventaire["PC"][5]), 20, WHITE, (60, 510))
                #Burger
                elif choix == 2:
                    afficher("Redonne {} points de CON. (Possede : {})".format(Inventaire["Burger"][3], Inventaire["Burger"][0] ), 20, WHITE, (60, 60))
                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][5]), 20, WHITE, (60, 240))
                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][5]), 20, ORANGE, (60, 270))
                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][5]), 20, WHITE, (60, 300))
                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][5]), 20, WHITE, (60, 330))
                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][5]), 20, WHITE, (60, 360))
                    afficher("The................................ {} euros".format(Inventaire["The"][5]), 20, WHITE, (60, 390))
                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][5]), 20, WHITE, (60, 420))
                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][5]), 20, WHITE, (60, 450))
                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][5]), 20, WHITE, (60, 480))
                    afficher("PC.................................. {} euros".format(Inventaire["PC"][5]), 20, WHITE, (60, 510))
                #Bubble Tea
                elif choix == 3:
                    afficher("Redonne {} points de CON. (Possede : {})".format(Inventaire["Bubble Tea"][3], Inventaire["Bubble Tea"][0] ), 20, WHITE, (60, 60))
                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][5]), 20, WHITE, (60, 240))
                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][5]), 20, WHITE, (60, 270))
                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][5]), 20, ORANGE, (60, 300))
                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][5]), 20, WHITE, (60, 330))
                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][5]), 20, WHITE, (60, 360))
                    afficher("The................................ {} euros".format(Inventaire["The"][5]), 20, WHITE, (60, 390))
                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][5]), 20, WHITE, (60, 420))
                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][5]), 20, WHITE, (60, 450))
                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][5]), 20, WHITE, (60, 480))
                    afficher("PC.................................. {} euros".format(Inventaire["PC"][5]), 20, WHITE, (60, 510))
                #Dessert au chocolat
                elif choix == 4:
                    afficher("Redonne {} points de CON. (Possede : {})".format(Inventaire["Dessert au Chocolat"][3], Inventaire["Dessert au Chocolat"][0] ), 20, WHITE, (60, 60))
                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][5]), 20, WHITE, (60, 240))
                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][5]), 20, WHITE, (60, 270))
                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][5]), 20, WHITE, (60, 300))
                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][5]), 20, ORANGE, (60, 330))
                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][5]), 20, WHITE, (60, 360))
                    afficher("The................................ {} euros".format(Inventaire["The"][5]), 20, WHITE, (60, 390))
                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][5]), 20, WHITE, (60, 420))
                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][5]), 20, WHITE, (60, 450))
                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][5]), 20, WHITE, (60, 480))
                    afficher("PC.................................. {} euros".format(Inventaire["PC"][5]), 20, WHITE, (60, 510))
                #Cafe
                elif choix == 5:
                    afficher("PRD+{}% | Consommable pour combat | Possede : {}".format(Inventaire["Cafe"][3], Inventaire["Cafe"][0] ), 20, WHITE, (60, 60))
                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][5]), 20, WHITE, (60, 240))
                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][5]), 20, WHITE, (60, 270))
                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][5]), 20, WHITE, (60, 300))
                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][5]), 20, WHITE, (60, 330))
                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][5]), 20, ORANGE, (60, 360))
                    afficher("The................................ {} euros".format(Inventaire["The"][5]), 20, WHITE, (60, 390))
                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][5]), 20, WHITE, (60, 420))
                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][5]), 20, WHITE, (60, 450))
                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][5]), 20, WHITE, (60, 480))
                    afficher("PC.................................. {} euros".format(Inventaire["PC"][5]), 20, WHITE, (60, 510))
                #The
                elif choix == 6:
                    afficher("DSC+{}% | Consommable pour combat | Possede : {}".format(Inventaire["The"][3], Inventaire["The"][0] ), 20, WHITE, (60, 60))
                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][5]), 20, WHITE, (60, 240))
                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][5]), 20, WHITE, (60, 270))
                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][5]), 20, WHITE, (60, 300))
                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][5]), 20, WHITE, (60, 330))
                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][5]), 20, WHITE, (60, 360))
                    afficher("The................................ {} euros".format(Inventaire["The"][5]), 20, ORANGE, (60, 390))
                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][5]), 20, WHITE, (60, 420))
                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][5]), 20, WHITE, (60, 450))
                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][5]), 20, WHITE, (60, 480))
                    afficher("PC.................................. {} euros".format(Inventaire["PC"][5]), 20, WHITE, (60, 510))
                #Stylo et feuilles
                elif choix == 7:
                    afficher("Equipement | PRD & DSC + {}% | Possede : {}".format(ceil(Inventaire["Stylo et feuilles"][3]*100), Inventaire["Stylo et feuilles"][0] ), 20, WHITE, (60, 60))
                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][5]), 20, WHITE, (60, 240))
                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][5]), 20, WHITE, (60, 270))
                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][5]), 20, WHITE, (60, 300))
                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][5]), 20, WHITE, (60, 330))
                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][5]), 20, WHITE, (60, 360))
                    afficher("The................................ {} euros".format(Inventaire["The"][5]), 20, WHITE, (60, 390))
                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][5]), 20, ORANGE, (60, 420))
                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][5]), 20, WHITE, (60, 450))
                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][5]), 20, WHITE, (60, 480))
                    afficher("PC.................................. {} euros".format(Inventaire["PC"][5]), 20, WHITE, (60, 510))
                #Cahier
                elif choix == 8:
                    afficher("Equipement | PRD & DSC + {}% | Possede : {}".format(ceil(Inventaire["Cahier"][3]*100), Inventaire["Cahier"][0] ), 20, WHITE, (60, 60))
                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][5]), 20, WHITE, (60, 240))
                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][5]), 20, WHITE, (60, 270))
                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][5]), 20, WHITE, (60, 300))
                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][5]), 20, WHITE, (60, 330))
                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][5]), 20, WHITE, (60, 360))
                    afficher("The................................ {} euros".format(Inventaire["The"][5]), 20, WHITE, (60, 390))
                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][5]), 20, WHITE, (60, 420))
                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][5]), 20, ORANGE, (60, 450))
                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][5]), 20, WHITE, (60, 480))
                    afficher("PC.................................. {} euros".format(Inventaire["PC"][5]), 20, WHITE, (60, 510))
                #Tablette
                elif choix == 9:
                    afficher("Equipement | PRD + {}% | Possede : {}".format(ceil(Inventaire["Tablette"][3]*100), Inventaire["Tablette"][0] ), 20, WHITE, (60, 60))
                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][5]), 20, WHITE, (60, 240))
                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][5]), 20, WHITE, (60, 270))
                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][5]), 20, WHITE, (60, 300))
                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][5]), 20, WHITE, (60, 330))
                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][5]), 20, WHITE, (60, 360))
                    afficher("The................................ {} euros".format(Inventaire["The"][5]), 20, WHITE, (60, 390))
                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][5]), 20, WHITE, (60, 420))
                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][5]), 20, WHITE, (60, 450))
                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][5]), 20, ORANGE, (60, 480))
                    afficher("PC.................................. {} euros".format(Inventaire["PC"][5]), 20, WHITE, (60, 510))
                #PC
                elif choix == 10:
                    afficher("Equipement | PRD + {}% | Possede : {}".format(ceil(Inventaire["PC"][3]*100), Inventaire["PC"][0] ), 20, WHITE, (60, 60))
                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][5]), 20, WHITE, (60, 240))
                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][5]), 20, WHITE, (60, 270))
                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][5]), 20, WHITE, (60, 300))
                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][5]), 20, WHITE, (60, 330))
                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][5]), 20, WHITE, (60, 360))
                    afficher("The................................ {} euros".format(Inventaire["The"][5]), 20, WHITE, (60, 390))
                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][5]), 20, WHITE, (60, 420))
                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][5]), 20, WHITE, (60, 450))
                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][5]), 20, WHITE, (60, 480))
                    afficher("PC.................................. {} euros".format(Inventaire["PC"][5]), 20, ORANGE, (60, 510))
                
                #Gere les inputs
                for event in pygame.event.get():
                    #Fermer la fenetre du jeu
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    # Si une touche est pressee, on se deplace dans le menu
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            choix -= 1
                            SFX("navigate")
                        if event.key == pygame.K_DOWN:
                            choix += 1
                            SFX("navigate")
                        if event.key == pygame.K_RIGHT:
                            SFX("navigate")
                            return 2, PARGENT


                        #Si on achete ou essaie d'acheter un objet
                        if event.key == pygame.K_SPACE:

                            #Boisson Energisante
                            if choix == 1:
                                #Si on n'a pas assez d'argent pour acheter
                                if PARGENT - Inventaire["Boisson Energisante"][5] < 0:
                                    SFX("badnote")
                                    load_page()
                                    afficher("Vous n'avez pas assez d'argent pour acheter ca.", 20, WHITE, (60, 60))
                                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][5]), 20, ORANGE, (60, 240))
                                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][5]), 20, WHITE, (60, 270))
                                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][5]), 20, WHITE, (60, 300))
                                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][5]), 20, WHITE, (60, 330))
                                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][5]), 20, WHITE, (60, 360))
                                    afficher("The................................ {} euros".format(Inventaire["The"][5]), 20, WHITE, (60, 390))
                                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][5]), 20, WHITE, (60, 420))
                                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][5]), 20, WHITE, (60, 450))
                                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][5]), 20, WHITE, (60, 480))
                                    afficher("PC.................................. {} euros".format(Inventaire["PC"][5]), 20, WHITE, (60, 510))
                                    pygame.display.update() #Update l'ecran
                                    valider()
                                #Si on a assez d'argent pour acheter l'objet
                                else:
                                    SFX("buy")
                                    PARGENT = PARGENT - Inventaire["Boisson Energisante"][5]
                                    Inventaire["Boisson Energisante"][0] += 1
                            #Burger
                            elif choix == 2:
                                if PARGENT - Inventaire["Burger"][5] < 0:
                                    SFX("badnote")
                                    load_page()
                                    afficher("Vous n'avez pas assez d'argent pour acheter ca.", 20, WHITE, (60, 60))
                                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][5]), 20, WHITE, (60, 240))
                                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][5]), 20, ORANGE, (60, 270))
                                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][5]), 20, WHITE, (60, 300))
                                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][5]), 20, WHITE, (60, 330))
                                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][5]), 20, WHITE, (60, 360))
                                    afficher("The................................ {} euros".format(Inventaire["The"][5]), 20, WHITE, (60, 390))
                                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][5]), 20, WHITE, (60, 420))
                                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][5]), 20, WHITE, (60, 450))
                                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][5]), 20, WHITE, (60, 480))
                                    afficher("PC.................................. {} euros".format(Inventaire["PC"][5]), 20, WHITE, (60, 510))
                                    pygame.display.update() #Update l'ecran
                                    valider()
                                else:
                                    SFX("buy")
                                    PARGENT = PARGENT - Inventaire["Burger"][5]
                                    Inventaire["Burger"][0] += 1
                            #Bubble Tea
                            elif choix == 3:
                                if PARGENT - Inventaire["Bubble Tea"][5] < 0:
                                    SFX("badnote")
                                    load_page()
                                    afficher("Vous n'avez pas assez d'argent pour acheter ca.", 20, WHITE, (60, 60))
                                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][5]), 20, WHITE, (60, 240))
                                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][5]), 20, WHITE, (60, 270))
                                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][5]), 20, ORANGE, (60, 300))
                                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][5]), 20, WHITE, (60, 330))
                                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][5]), 20, WHITE, (60, 360))
                                    afficher("The................................ {} euros".format(Inventaire["The"][5]), 20, WHITE, (60, 390))
                                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][5]), 20, WHITE, (60, 420))
                                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][5]), 20, WHITE, (60, 450))
                                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][5]), 20, WHITE, (60, 480))
                                    afficher("PC.................................. {} euros".format(Inventaire["PC"][5]), 20, WHITE, (60, 510))
                                    pygame.display.update() #Update l'ecran
                                    valider()
                                else:
                                    SFX("buy")
                                    PARGENT = PARGENT - Inventaire["Bubble Tea"][5]
                                    Inventaire["Bubble Tea"][0] += 1
                            #Dessert au Chocolat
                            elif choix == 4:
                                if PARGENT - Inventaire["Dessert au Chocolat"][5] < 0:
                                    SFX("badnote")
                                    load_page()
                                    afficher("Vous n'avez pas assez d'argent pour acheter ca.", 20, WHITE, (60, 60))
                                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][5]), 20, WHITE, (60, 240))
                                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][5]), 20, WHITE, (60, 270))
                                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][5]), 20, WHITE, (60, 300))
                                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][5]), 20, ORANGE, (60, 330))
                                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][5]), 20, WHITE, (60, 360))
                                    afficher("The................................ {} euros".format(Inventaire["The"][5]), 20, WHITE, (60, 390))
                                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][5]), 20, WHITE, (60, 420))
                                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][5]), 20, WHITE, (60, 450))
                                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][5]), 20, WHITE, (60, 480))
                                    afficher("PC.................................. {} euros".format(Inventaire["PC"][5]), 20, WHITE, (60, 510))
                                    pygame.display.update() #Update l'ecran
                                    valider()
                                else:
                                    SFX("buy")
                                    PARGENT = PARGENT - Inventaire["Dessert au Chocolat"][5]
                                    Inventaire["Dessert au Chocolat"][0] += 1
                            #Cafe
                            elif choix == 5:
                                if PARGENT - Inventaire["Cafe"][5] < 0:
                                    SFX("badnote")
                                    load_page()
                                    afficher("Vous n'avez pas assez d'argent pour acheter ca.", 20, WHITE, (60, 60))
                                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][5]), 20, WHITE, (60, 240))
                                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][5]), 20, WHITE, (60, 270))
                                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][5]), 20, WHITE, (60, 300))
                                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][5]), 20, WHITE, (60, 330))
                                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][5]), 20, ORANGE, (60, 360))
                                    afficher("The................................ {} euros".format(Inventaire["The"][5]), 20, WHITE, (60, 390))
                                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][5]), 20, WHITE, (60, 420))
                                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][5]), 20, WHITE, (60, 450))
                                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][5]), 20, WHITE, (60, 480))
                                    afficher("PC.................................. {} euros".format(Inventaire["PC"][5]), 20, WHITE, (60, 510))
                                    pygame.display.update() #Update l'ecran
                                    valider()
                                else:
                                    SFX("buy")
                                    PARGENT = PARGENT - Inventaire["Cafe"][5]
                                    Inventaire["Cafe"][0] += 1
                            #The
                            elif choix == 6:
                                if PARGENT - Inventaire["The"][5] < 0:
                                    SFX("badnote")
                                    load_page()
                                    afficher("Vous n'avez pas assez d'argent pour acheter ca.", 20, WHITE, (60, 60))
                                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][5]), 20, WHITE, (60, 240))
                                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][5]), 20, WHITE, (60, 270))
                                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][5]), 20, WHITE, (60, 300))
                                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][5]), 20, WHITE, (60, 330))
                                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][5]), 20, WHITE, (60, 360))
                                    afficher("The................................ {} euros".format(Inventaire["The"][5]), 20, ORANGE, (60, 390))
                                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][5]), 20, WHITE, (60, 420))
                                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][5]), 20, WHITE, (60, 450))
                                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][5]), 20, WHITE, (60, 480))
                                    afficher("PC.................................. {} euros".format(Inventaire["PC"][5]), 20, WHITE, (60, 510))
                                    pygame.display.update() #Update l'ecran
                                    valider()
                                else:
                                    SFX("buy")
                                    PARGENT = PARGENT - Inventaire["The"][5]
                                    Inventaire["The"][0] += 1
                            #Stylo et feuilles
                            elif choix == 7:
                                if PARGENT - Inventaire["Stylo et feuilles"][5] < 0:
                                    SFX("badnote")
                                    load_page()
                                    afficher("Vous n'avez pas assez d'argent pour acheter ca.", 20, WHITE, (60, 60))
                                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][5]), 20, WHITE, (60, 240))
                                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][5]), 20, WHITE, (60, 270))
                                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][5]), 20, WHITE, (60, 300))
                                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][5]), 20, WHITE, (60, 330))
                                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][5]), 20, WHITE, (60, 360))
                                    afficher("The................................ {} euros".format(Inventaire["The"][5]), 20, WHITE, (60, 390))
                                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][5]), 20, ORANGE, (60, 420))
                                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][5]), 20, WHITE, (60, 450))
                                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][5]), 20, WHITE, (60, 480))
                                    afficher("PC.................................. {} euros".format(Inventaire["PC"][5]), 20, WHITE, (60, 510))
                                    pygame.display.update() #Update l'ecran
                                    valider()
                                else:
                                    SFX("buy")
                                    PARGENT = PARGENT - Inventaire["Stylo et feuilles"][5]
                                    Inventaire["Stylo et feuilles"][0] += 1
                            #Cahier
                            elif choix == 8:
                                if PARGENT - Inventaire["Cahier"][5] < 0:
                                    SFX("badnote")
                                    load_page()
                                    afficher("Vous n'avez pas assez d'argent pour acheter ca.", 20, WHITE, (60, 60))
                                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][5]), 20, WHITE, (60, 240))
                                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][5]), 20, WHITE, (60, 270))
                                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][5]), 20, WHITE, (60, 300))
                                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][5]), 20, WHITE, (60, 330))
                                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][5]), 20, WHITE, (60, 360))
                                    afficher("The................................ {} euros".format(Inventaire["The"][5]), 20, WHITE, (60, 390))
                                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][5]), 20, WHITE, (60, 420))
                                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][5]), 20, ORANGE, (60, 450))
                                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][5]), 20, WHITE, (60, 480))
                                    afficher("PC.................................. {} euros".format(Inventaire["PC"][5]), 20, WHITE, (60, 510))
                                    pygame.display.update() #Update l'ecran
                                    valider()
                                else:
                                    SFX("buy")
                                    PARGENT = PARGENT - Inventaire["Cahier"][5]
                                    Inventaire["Cahier"][0] += 1
                            #Tablette
                            elif choix == 9:
                                if PARGENT - Inventaire["Tablette"][5] < 0:
                                    SFX("badnote")
                                    load_page()
                                    afficher("Vous n'avez pas assez d'argent pour acheter ca.", 20, WHITE, (60, 60))
                                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][5]), 20, WHITE, (60, 240))
                                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][5]), 20, WHITE, (60, 270))
                                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][5]), 20, WHITE, (60, 300))
                                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][5]), 20, WHITE, (60, 330))
                                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][5]), 20, WHITE, (60, 360))
                                    afficher("The................................ {} euros".format(Inventaire["The"][5]), 20, WHITE, (60, 390))
                                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][5]), 20, WHITE, (60, 420))
                                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][5]), 20, WHITE, (60, 450))
                                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][5]), 20, ORANGE, (60, 480))
                                    afficher("PC.................................. {} euros".format(Inventaire["PC"][5]), 20, WHITE, (60, 510))
                                    pygame.display.update() #Update l'ecran
                                    valider()
                                else:
                                    SFX("buy")
                                    PARGENT = PARGENT - Inventaire["Tablette"][5]
                                    Inventaire["Tablette"][0] += 1
                            #PC
                            elif choix == 10:
                                if PARGENT - Inventaire["PC"][5] < 0:
                                    SFX("badnote")
                                    load_page()
                                    afficher("Vous n'avez pas assez d'argent pour acheter ca.", 20, WHITE, (60, 60))
                                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][5]), 20, WHITE, (60, 240))
                                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][5]), 20, WHITE, (60, 270))
                                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][5]), 20, WHITE, (60, 300))
                                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][5]), 20, WHITE, (60, 330))
                                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][5]), 20, WHITE, (60, 360))
                                    afficher("The................................ {} euros".format(Inventaire["The"][5]), 20, WHITE, (60, 390))
                                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][5]), 20, WHITE, (60, 420))
                                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][5]), 20, WHITE, (60, 450))
                                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][5]), 20, WHITE, (60, 480))
                                    afficher("PC.................................. {} euros".format(Inventaire["PC"][5]), 20, ORANGE, (60, 510))
                                    pygame.display.update() #Update l'ecran
                                    valider()
                                else:
                                    SFX("buy")
                                    PARGENT = PARGENT - Inventaire["PC"][5]
                                    Inventaire["PC"][0] += 1

                if choix < 1:
                    return 1, PARGENT
                if choix > 10:
                    choix = 10

                pygame.display.update() #Update l'ecran

        def Vendre(PARGENT):
            """Permet de vendre des objets"""

            #Initialisation des variables
            choix = 1

            #Depose les couleurs dans des variables.
            WHITE, ORANGE, ALPHA = Couleurs()
            YELLOW = [255,255,85]

            def load_page():
                """Affiche tout ce qu'il y a a afficher sur la page d'achat du magasin."""

                #Affiche le fond et le rectangle en haut de l'ecran
                Rec_Haut_mag()

                #Dessine tous les rectangles en haut de l'ecran
                window_draw_rect(WHITE, ALPHA, 540, 130, 215, 60)
                window_draw_rect(WHITE, ALPHA, 340, 130, 150, 60)
                window_draw_rect(WHITE, ALPHA, 40, 130, 150, 60)
                window_draw_rect(ORANGE, ALPHA, 190, 130, 150, 60)
                afficher("Acheter", 20, WHITE, (67, 150))
                afficher("Vendre", 20, ORANGE, (217, 150))
                afficher("Quitter", 20, WHITE, (367, 150))
                afficher("Argent : {}".format(PARGENT), 20, WHITE, (560, 150))

                #Dessine la fenetre qui contiendra tous les elements du shop
                window_draw_rect(WHITE, ALPHA, 40, 220, 490, 330)


            #Boucle qui tourne tant qu'on se trouve dans le bouton "Acheter"
            Acheter_run = True
            while Acheter_run == True:

                load_page()

                #Affiche les differents objets du magasin
                #Boisson energisante
                if choix == 1:
                    afficher("Redonne {} points de CON. (Possede : {})".format(Inventaire["Boisson Energisante"][3], Inventaire["Boisson Energisante"][0] ), 20, WHITE, (60, 60))
                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][6]), 20, ORANGE, (60, 240))
                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][6]), 20, WHITE, (60, 270))
                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][6]), 20, WHITE, (60, 300))
                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][6]), 20, WHITE, (60, 330))
                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][6]), 20, WHITE, (60, 360))
                    afficher("The................................ {} euros".format(Inventaire["The"][6]), 20, WHITE, (60, 390))
                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][6]), 20, WHITE, (60, 420))
                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][6]), 20, WHITE, (60, 450))
                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][6]), 20, WHITE, (60, 480))
                    afficher("PC.................................. {} euros".format(Inventaire["PC"][6]), 20, WHITE, (60, 510))
                #Burger
                elif choix == 2:
                    afficher("Redonne {} points de CON. (Possede : {})".format(Inventaire["Burger"][3], Inventaire["Burger"][0] ), 20, WHITE, (60, 60))
                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][6]), 20, WHITE, (60, 240))
                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][6]), 20, ORANGE, (60, 270))
                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][6]), 20, WHITE, (60, 300))
                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][6]), 20, WHITE, (60, 330))
                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][6]), 20, WHITE, (60, 360))
                    afficher("The................................ {} euros".format(Inventaire["The"][6]), 20, WHITE, (60, 390))
                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][6]), 20, WHITE, (60, 420))
                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][6]), 20, WHITE, (60, 450))
                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][6]), 20, WHITE, (60, 480))
                    afficher("PC.................................. {} euros".format(Inventaire["PC"][6]), 20, WHITE, (60, 510))
                #Bubble Tea
                elif choix == 3:
                    afficher("Redonne {} points de CON. (Possede : {})".format(Inventaire["Bubble Tea"][3], Inventaire["Bubble Tea"][0] ), 20, WHITE, (60, 60))
                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][6]), 20, WHITE, (60, 240))
                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][6]), 20, WHITE, (60, 270))
                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][6]), 20, ORANGE, (60, 300))
                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][6]), 20, WHITE, (60, 330))
                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][6]), 20, WHITE, (60, 360))
                    afficher("The................................ {} euros".format(Inventaire["The"][6]), 20, WHITE, (60, 390))
                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][6]), 20, WHITE, (60, 420))
                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][6]), 20, WHITE, (60, 450))
                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][6]), 20, WHITE, (60, 480))
                    afficher("PC.................................. {} euros".format(Inventaire["PC"][6]), 20, WHITE, (60, 510))
                #Dessert au chocolat
                elif choix == 4:
                    afficher("Redonne {} points de CON. (Possede : {})".format(Inventaire["Dessert au Chocolat"][3], Inventaire["Dessert au Chocolat"][0] ), 20, WHITE, (60, 60))
                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][6]), 20, WHITE, (60, 240))
                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][6]), 20, WHITE, (60, 270))
                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][6]), 20, WHITE, (60, 300))
                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][6]), 20, ORANGE, (60, 330))
                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][6]), 20, WHITE, (60, 360))
                    afficher("The................................ {} euros".format(Inventaire["The"][6]), 20, WHITE, (60, 390))
                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][6]), 20, WHITE, (60, 420))
                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][6]), 20, WHITE, (60, 450))
                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][6]), 20, WHITE, (60, 480))
                    afficher("PC.................................. {} euros".format(Inventaire["PC"][6]), 20, WHITE, (60, 510))
                #Cafe
                elif choix == 5:
                    afficher("PRD+{}% | Consommable pour combat | Possede : {}".format(Inventaire["Cafe"][3], Inventaire["Cafe"][0] ), 20, WHITE, (60, 60))
                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][6]), 20, WHITE, (60, 240))
                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][6]), 20, WHITE, (60, 270))
                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][6]), 20, WHITE, (60, 300))
                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][6]), 20, WHITE, (60, 330))
                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][6]), 20, ORANGE, (60, 360))
                    afficher("The................................ {} euros".format(Inventaire["The"][6]), 20, WHITE, (60, 390))
                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][6]), 20, WHITE, (60, 420))
                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][6]), 20, WHITE, (60, 450))
                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][6]), 20, WHITE, (60, 480))
                    afficher("PC.................................. {} euros".format(Inventaire["PC"][6]), 20, WHITE, (60, 510))
                #The
                elif choix == 6:
                    afficher("DSC+{}% | Consommable pour combat | Possede : {}".format(Inventaire["The"][3], Inventaire["The"][0] ), 20, WHITE, (60, 60))
                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][6]), 20, WHITE, (60, 240))
                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][6]), 20, WHITE, (60, 270))
                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][6]), 20, WHITE, (60, 300))
                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][6]), 20, WHITE, (60, 330))
                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][6]), 20, WHITE, (60, 360))
                    afficher("The................................ {} euros".format(Inventaire["The"][6]), 20, ORANGE, (60, 390))
                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][6]), 20, WHITE, (60, 420))
                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][6]), 20, WHITE, (60, 450))
                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][6]), 20, WHITE, (60, 480))
                    afficher("PC.................................. {} euros".format(Inventaire["PC"][6]), 20, WHITE, (60, 510))
                #Stylo et feuilles
                elif choix == 7:
                    afficher("Equipement | PRD & DSC + {}% | Possede : {}".format(ceil(Inventaire["Stylo et feuilles"][3]*100), Inventaire["Stylo et feuilles"][0] ), 20, WHITE, (60, 60))
                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][6]), 20, WHITE, (60, 240))
                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][6]), 20, WHITE, (60, 270))
                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][6]), 20, WHITE, (60, 300))
                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][6]), 20, WHITE, (60, 330))
                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][6]), 20, WHITE, (60, 360))
                    afficher("The................................ {} euros".format(Inventaire["The"][6]), 20, WHITE, (60, 390))
                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][6]), 20, ORANGE, (60, 420))
                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][6]), 20, WHITE, (60, 450))
                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][6]), 20, WHITE, (60, 480))
                    afficher("PC.................................. {} euros".format(Inventaire["PC"][6]), 20, WHITE, (60, 510))
                #Cahier
                elif choix == 8:
                    afficher("Equipement | PRD & DSC + {}% | Possede : {}".format(ceil(Inventaire["Cahier"][3]*100), Inventaire["Cahier"][0] ), 20, WHITE, (60, 60))
                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][6]), 20, WHITE, (60, 240))
                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][6]), 20, WHITE, (60, 270))
                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][6]), 20, WHITE, (60, 300))
                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][6]), 20, WHITE, (60, 330))
                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][6]), 20, WHITE, (60, 360))
                    afficher("The................................ {} euros".format(Inventaire["The"][6]), 20, WHITE, (60, 390))
                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][6]), 20, WHITE, (60, 420))
                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][6]), 20, ORANGE, (60, 450))
                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][6]), 20, WHITE, (60, 480))
                    afficher("PC.................................. {} euros".format(Inventaire["PC"][6]), 20, WHITE, (60, 510))
                #Tablette
                elif choix == 9:
                    afficher("Equipement | PRD + {}% | Possede : {}".format(ceil(Inventaire["Tablette"][3]*100), Inventaire["Tablette"][0] ), 20, WHITE, (60, 60))
                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][6]), 20, WHITE, (60, 240))
                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][6]), 20, WHITE, (60, 270))
                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][6]), 20, WHITE, (60, 300))
                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][6]), 20, WHITE, (60, 330))
                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][6]), 20, WHITE, (60, 360))
                    afficher("The................................ {} euros".format(Inventaire["The"][6]), 20, WHITE, (60, 390))
                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][6]), 20, WHITE, (60, 420))
                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][6]), 20, WHITE, (60, 450))
                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][6]), 20, ORANGE, (60, 480))
                    afficher("PC.................................. {} euros".format(Inventaire["PC"][6]), 20, WHITE, (60, 510))
                #PC
                elif choix == 10:
                    afficher("Equipement | PRD + {}% | Possede : {}".format(ceil(Inventaire["PC"][3]*100), Inventaire["PC"][0] ), 20, WHITE, (60, 60))
                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][6]), 20, WHITE, (60, 240))
                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][6]), 20, WHITE, (60, 270))
                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][6]), 20, WHITE, (60, 300))
                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][6]), 20, WHITE, (60, 330))
                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][6]), 20, WHITE, (60, 360))
                    afficher("The................................ {} euros".format(Inventaire["The"][6]), 20, WHITE, (60, 390))
                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][6]), 20, WHITE, (60, 420))
                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][6]), 20, WHITE, (60, 450))
                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][6]), 20, WHITE, (60, 480))
                    afficher("PC.................................. {} euros".format(Inventaire["PC"][6]), 20, ORANGE, (60, 510))
                
                #Gere les inputs
                for event in pygame.event.get():
                    #Fermer la fenetre du jeu
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    # Si une touche est pressee, on se deplace dans le menu
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            choix -= 1
                            SFX("navigate")
                        if event.key == pygame.K_DOWN:
                            choix += 1
                            SFX("navigate")
                        if event.key == pygame.K_RIGHT:
                            SFX("navigate")
                            return 3, PARGENT
                        if event.key == pygame.K_LEFT:
                            SFX("navigate")
                            return 1, PARGENT

                        #Si on achete ou essaie d'acheter un objet
                        if event.key == pygame.K_SPACE:

                            #Boisson Energisante
                            if choix == 1:
                                if Inventaire["Boisson Energisante"][0] < 1:
                                    SFX("badnote")
                                    load_page()
                                    afficher("Vous n'en possedez plus.", 20, WHITE, (60, 60))
                                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][6]), 20, ORANGE, (60, 240))
                                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][6]), 20, WHITE, (60, 270))
                                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][6]), 20, WHITE, (60, 300))
                                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][6]), 20, WHITE, (60, 330))
                                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][6]), 20, WHITE, (60, 360))
                                    afficher("The................................ {} euros".format(Inventaire["The"][6]), 20, WHITE, (60, 390))
                                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][6]), 20, WHITE, (60, 420))
                                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][6]), 20, WHITE, (60, 450))
                                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][6]), 20, WHITE, (60, 480))
                                    afficher("PC.................................. {} euros".format(Inventaire["PC"][6]), 20, WHITE, (60, 510))
                                    pygame.display.update() #Update l'ecran
                                    valider()
                                else:
                                    SFX("buy")
                                    PARGENT = PARGENT + Inventaire["Boisson Energisante"][6]
                                    Inventaire["Boisson Energisante"][0] -= 1
                            #Burger
                            elif choix == 2:
                                if Inventaire["Burger"][0] < 1:
                                    SFX("badnote")
                                    load_page()
                                    afficher("Vous n'en possedez plus.", 20, WHITE, (60, 60))
                                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][6]), 20, WHITE, (60, 240))
                                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][6]), 20, ORANGE, (60, 270))
                                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][6]), 20, WHITE, (60, 300))
                                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][6]), 20, WHITE, (60, 330))
                                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][6]), 20, WHITE, (60, 360))
                                    afficher("The................................ {} euros".format(Inventaire["The"][6]), 20, WHITE, (60, 390))
                                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][6]), 20, WHITE, (60, 420))
                                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][6]), 20, WHITE, (60, 450))
                                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][6]), 20, WHITE, (60, 480))
                                    afficher("PC.................................. {} euros".format(Inventaire["PC"][6]), 20, WHITE, (60, 510))
                                    pygame.display.update() #Update l'ecran
                                    valider()
                                else:
                                    SFX("buy")
                                    PARGENT = PARGENT + Inventaire["Burger"][6]
                                    Inventaire["Burger"][0] -= 1
                            #Bubble Tea
                            elif choix == 3:
                                if Inventaire["Bubble Tea"][0] < 1:
                                    SFX("badnote")
                                    load_page()
                                    afficher("Vous n'en possedez plus.", 20, WHITE, (60, 60))
                                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][6]), 20, WHITE, (60, 240))
                                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][6]), 20, WHITE, (60, 270))
                                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][6]), 20, ORANGE, (60, 300))
                                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][6]), 20, WHITE, (60, 330))
                                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][6]), 20, WHITE, (60, 360))
                                    afficher("The................................ {} euros".format(Inventaire["The"][6]), 20, WHITE, (60, 390))
                                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][6]), 20, WHITE, (60, 420))
                                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][6]), 20, WHITE, (60, 450))
                                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][6]), 20, WHITE, (60, 480))
                                    afficher("PC.................................. {} euros".format(Inventaire["PC"][6]), 20, WHITE, (60, 510))
                                    pygame.display.update() #Update l'ecran
                                    valider()
                                else:
                                    SFX("buy")
                                    PARGENT = PARGENT + Inventaire["Bubble Tea"][6]
                                    Inventaire["Bubble Tea"][0] -= 1
                            #Dessert au Chocolat
                            elif choix == 4:
                                if Inventaire["Dessert au Chocolat"][0] < 1:
                                    SFX("badnote")
                                    load_page()
                                    afficher("Vous n'en possedez plus.", 20, WHITE, (60, 60))
                                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][6]), 20, WHITE, (60, 240))
                                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][6]), 20, WHITE, (60, 270))
                                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][6]), 20, WHITE, (60, 300))
                                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][6]), 20, ORANGE, (60, 330))
                                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][6]), 20, WHITE, (60, 360))
                                    afficher("The................................ {} euros".format(Inventaire["The"][6]), 20, WHITE, (60, 390))
                                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][6]), 20, WHITE, (60, 420))
                                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][6]), 20, WHITE, (60, 450))
                                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][6]), 20, WHITE, (60, 480))
                                    afficher("PC.................................. {} euros".format(Inventaire["PC"][6]), 20, WHITE, (60, 510))
                                    pygame.display.update() #Update l'ecran
                                    valider()
                                else:
                                    SFX("buy")
                                    PARGENT = PARGENT + Inventaire["Dessert au Chocolat"][6]
                                    Inventaire["Dessert au Chocolat"][0] -= 1
                            #Cafe
                            elif choix == 5:
                                if Inventaire["Cafe"][0] < 1:
                                    SFX("badnote")
                                    load_page()
                                    afficher("Vous n'en possedez plus.", 20, WHITE, (60, 60))
                                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][6]), 20, WHITE, (60, 240))
                                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][6]), 20, WHITE, (60, 270))
                                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][6]), 20, WHITE, (60, 300))
                                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][6]), 20, WHITE, (60, 330))
                                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][6]), 20, ORANGE, (60, 360))
                                    afficher("The................................ {} euros".format(Inventaire["The"][6]), 20, WHITE, (60, 390))
                                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][6]), 20, WHITE, (60, 420))
                                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][6]), 20, WHITE, (60, 450))
                                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][6]), 20, WHITE, (60, 480))
                                    afficher("PC.................................. {} euros".format(Inventaire["PC"][6]), 20, WHITE, (60, 510))
                                    pygame.display.update() #Update l'ecran
                                    valider()
                                else:
                                    SFX("buy")
                                    PARGENT = PARGENT + Inventaire["Cafe"][6]
                                    Inventaire["Cafe"][0] -= 1
                            #The
                            elif choix == 6:
                                if Inventaire["The"][0] < 1:
                                    SFX("badnote")
                                    load_page()
                                    afficher("Vous n'en possedez plus.", 20, WHITE, (60, 60))
                                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][6]), 20, WHITE, (60, 240))
                                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][6]), 20, WHITE, (60, 270))
                                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][6]), 20, WHITE, (60, 300))
                                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][6]), 20, WHITE, (60, 330))
                                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][6]), 20, WHITE, (60, 360))
                                    afficher("The................................ {} euros".format(Inventaire["The"][6]), 20, ORANGE, (60, 390))
                                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][6]), 20, WHITE, (60, 420))
                                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][6]), 20, WHITE, (60, 450))
                                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][6]), 20, WHITE, (60, 480))
                                    afficher("PC.................................. {} euros".format(Inventaire["PC"][6]), 20, WHITE, (60, 510))
                                    pygame.display.update() #Update l'ecran
                                    valider()
                                else:
                                    SFX("buy")
                                    PARGENT = PARGENT + Inventaire["The"][6]
                                    Inventaire["The"][0] -= 1
                            #Stylo et feuilles
                            elif choix == 7:
                                if Inventaire["Stylo et feuilles"][0] < 1:
                                    SFX("badnote")
                                    load_page()
                                    afficher("Vous n'en possedez plus.", 20, WHITE, (60, 60))
                                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][6]), 20, WHITE, (60, 240))
                                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][6]), 20, WHITE, (60, 270))
                                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][6]), 20, WHITE, (60, 300))
                                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][6]), 20, WHITE, (60, 330))
                                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][6]), 20, WHITE, (60, 360))
                                    afficher("The................................ {} euros".format(Inventaire["The"][6]), 20, WHITE, (60, 390))
                                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][6]), 20, ORANGE, (60, 420))
                                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][6]), 20, WHITE, (60, 450))
                                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][6]), 20, WHITE, (60, 480))
                                    afficher("PC.................................. {} euros".format(Inventaire["PC"][6]), 20, WHITE, (60, 510))
                                    pygame.display.update() #Update l'ecran
                                    valider()
                                else:
                                    SFX("buy")
                                    PARGENT = PARGENT + Inventaire["Stylo et feuilles"][6]
                                    Inventaire["Stylo et feuilles"][0] -= 1
                            #Cahier
                            elif choix == 8:
                                if Inventaire["Cahier"][0] < 1:
                                    SFX("badnote")
                                    load_page()
                                    afficher("Vous n'en possedez plus.", 20, WHITE, (60, 60))
                                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][6]), 20, WHITE, (60, 240))
                                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][6]), 20, WHITE, (60, 270))
                                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][6]), 20, WHITE, (60, 300))
                                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][6]), 20, WHITE, (60, 330))
                                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][6]), 20, WHITE, (60, 360))
                                    afficher("The................................ {} euros".format(Inventaire["The"][6]), 20, WHITE, (60, 390))
                                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][6]), 20, WHITE, (60, 420))
                                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][6]), 20, ORANGE, (60, 450))
                                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][6]), 20, WHITE, (60, 480))
                                    afficher("PC.................................. {} euros".format(Inventaire["PC"][6]), 20, WHITE, (60, 510))
                                    pygame.display.update() #Update l'ecran
                                    valider()
                                else:
                                    SFX("buy")
                                    PARGENT = PARGENT + Inventaire["Cahier"][6]
                                    Inventaire["Cahier"][0] -= 1
                            #Tablette
                            elif choix == 9:
                                if Inventaire["Tablette"][0] < 1:
                                    SFX("badnote")
                                    load_page()
                                    afficher("Vous n'en possedez plus.", 20, WHITE, (60, 60))
                                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][6]), 20, WHITE, (60, 240))
                                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][6]), 20, WHITE, (60, 270))
                                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][6]), 20, WHITE, (60, 300))
                                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][6]), 20, WHITE, (60, 330))
                                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][6]), 20, WHITE, (60, 360))
                                    afficher("The................................ {} euros".format(Inventaire["The"][6]), 20, WHITE, (60, 390))
                                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][6]), 20, WHITE, (60, 420))
                                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][6]), 20, WHITE, (60, 450))
                                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][6]), 20, ORANGE, (60, 480))
                                    afficher("PC.................................. {} euros".format(Inventaire["PC"][6]), 20, WHITE, (60, 510))
                                    pygame.display.update() #Update l'ecran
                                    valider()
                                else:
                                    SFX("buy")
                                    PARGENT = PARGENT + Inventaire["Tablette"][6]
                                    Inventaire["Tablette"][0] -= 1
                            #PC
                            elif choix == 10:
                                if Inventaire["PC"][0] < 1:
                                    SFX("badnote")
                                    load_page()
                                    afficher("Vous n'en possedez plus.", 20, WHITE, (60, 60))
                                    afficher("Boisson energisante.... {} euros".format(Inventaire["Boisson Energisante"][6]), 20, WHITE, (60, 240))
                                    afficher("Burger........................... {} euros".format(Inventaire["Burger"][6]), 20, WHITE, (60, 270))
                                    afficher("Bubble tea.................... {} euros".format(Inventaire["Bubble Tea"][6]), 20, WHITE, (60, 300))
                                    afficher("Dessert au chocolat... {} euros".format(Inventaire["Dessert au Chocolat"][6]), 20, WHITE, (60, 330))
                                    afficher("Cafe.............................. {} euros".format(Inventaire["Cafe"][6]), 20, WHITE, (60, 360))
                                    afficher("The................................ {} euros".format(Inventaire["The"][6]), 20, WHITE, (60, 390))
                                    afficher("Stylo et feuilles........ {} euros".format(Inventaire["Stylo et feuilles"][6]), 20, WHITE, (60, 420))
                                    afficher("Cahier........................... {} euros".format(Inventaire["Cahier"][6]), 20, WHITE, (60, 450))
                                    afficher("Tablette....................... {} euros".format(Inventaire["Tablette"][6]), 20, WHITE, (60, 480))
                                    afficher("PC.................................. {} euros".format(Inventaire["PC"][6]), 20, ORANGE, (60, 510))
                                    pygame.display.update() #Update l'ecran
                                    valider()
                                else:
                                    SFX("buy")
                                    PARGENT = PARGENT + Inventaire["PC"][6]
                                    Inventaire["PC"][0] -= 1

                if choix < 1:
                    return 1, PARGENT
                if choix > 10:
                    choix = 10

                pygame.display.update() #Update l'ecran

        Avancee = 0
        choix = 1

        equip = 0

        #Tant que la boucle du magasin tourne
        while Avancee == 0 :

            #Affiche le fond et le rectangle en haut de l'ecran
            Rec_Haut_mag()

            if choix == 1: #Si on se trouve sur le menu "acheter"
                afficher("Acheter un objet.", 20, WHITE, (60, 60))
                window_draw_rect(WHITE, ALPHA, 540, 130, 215, 60)
                window_draw_rect(WHITE, ALPHA, 190, 130, 150, 60)
                window_draw_rect(WHITE, ALPHA, 340, 130, 150, 60)
                window_draw_rect(ORANGE, ALPHA, 40, 130, 150, 60)
                afficher("Acheter", 20, ORANGE, (67, 150))
                afficher("Vendre", 20, WHITE, (217, 150))
                afficher("Quitter", 20, WHITE, (367, 150))
                afficher("Argent : {}".format(PARGENT), 20, WHITE, (560, 150))
            elif choix == 2: #Si on se trouve sur le menu "vendre"
                afficher("Vendre un objet.", 20, WHITE, (60, 60))
                window_draw_rect(WHITE, ALPHA, 540, 130, 215, 60)
                window_draw_rect(WHITE, ALPHA, 340, 130, 150, 60)
                window_draw_rect(WHITE, ALPHA, 40, 130, 150, 60)
                window_draw_rect(ORANGE, ALPHA, 190, 130, 150, 60)
                afficher("Acheter", 20, WHITE, (67, 150))
                afficher("Vendre", 20, ORANGE, (217, 150))
                afficher("Quitter", 20, WHITE, (367, 150))
                afficher("Argent : {}".format(PARGENT), 20, WHITE, (560, 150))
            else: #Si on se trouve sur le menu "Partir"
                afficher("Quitter le magasin et revenir chez soi.", 20, WHITE, (60, 60))
                window_draw_rect(WHITE, ALPHA, 540, 130, 215, 60)
                window_draw_rect(WHITE, ALPHA, 190, 130, 150, 60)
                window_draw_rect(ORANGE, ALPHA, 340, 130, 150, 60)
                window_draw_rect(WHITE, ALPHA, 40, 130, 150, 60)
                afficher("Acheter", 20, WHITE, (67, 150))
                afficher("Vendre", 20, WHITE, (217, 150))
                afficher("Quitter", 20, ORANGE, (367, 150))
                afficher("Argent : {}".format(PARGENT), 20, WHITE, (560, 150))

            #Gere les inputs
            for event in pygame.event.get():
                #Fermer la fenetre du jeu
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # Si une touche est pressee, on se deplace dans le menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        choix -= 1
                        SFX("navigate")
                    if event.key == pygame.K_RIGHT:
                        choix += 1
                        SFX("navigate")
                    #Permet de selectionner quelque chose en appuyant sur espace ou la fleche du bas.
                    if event.key == pygame.K_SPACE or event.key == pygame.K_DOWN:
                        if choix == 1:
                            choix, PARGENT = Acheter(PARGENT)
                            SFX("navigate")
                        elif choix == 2:
                            choix, PARGENT = Vendre(PARGENT)
                            SFX("navigate")
                        elif choix == 3:
                            Music("nav")
                            SFX("select")
                            return 0, PARGENT

            if choix < 1:
                choix = 1
            elif choix > 3:
                choix = 3

            pygame.display.update() #Update l'ecran
    
    def Avancee4():
        """Le bouton "autre". Permet de revenir au menu principal, sauvegarder et visualiser l'aide."""

        #Initialisation des variables
        choix = 1 #Sera utilise pour naviguer dans le bouton et choisir
        
        #Position des rectangles du bas de l'ecran
        X_RecBas = 30
        Y_RecBas = 500

        #Depose les couleurs dans une variable
        WHITE, ORANGE, ALPHA = Couleurs()
        YELLOW = [255,255,85]


        #Boucle qui tourne tant que le joueur se trouve dans le bouton "autre"
        autre_running = True
        while autre_running == True:

            #Permet de dessiner les rectangles en haut de l'ecran
            Rec_Haut()

            #Affiche le grand cadre sur la droite de l'ecran avec les messages a l'interieur
            window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas-384, 550, 348)
            afficher("Productivite (PRD) = Vos degats", 18, WHITE, (X_RecBas+20, Y_RecBas-354))
            afficher("Discipline (DSC) = Votre defense", 18, WHITE, (X_RecBas+20, Y_RecBas-324))
            afficher("Concentration (CON) = Votre sante", 18, WHITE, (X_RecBas+20, Y_RecBas-294))

            afficher("Math/Francais/Anglais : Bonus de degats", 18, WHITE, (X_RecBas+20, Y_RecBas-234))
            afficher("vs. les ennemis de la matiere en question", 18, WHITE, (X_RecBas+20, Y_RecBas-204))
            afficher("selon votre niveau dans la matiere.", 18, WHITE, (X_RecBas+20, Y_RecBas-174))

            afficher("Objectif : Travailler en combattant ses", 18, WHITE, (X_RecBas+20, Y_RecBas-114))
            afficher("distractions pour reussir son annee.", 18, WHITE, (X_RecBas+20, Y_RecBas-84))


            #Rectangle agir
            window_draw_rect(WHITE, ALPHA, X_RecBas, Y_RecBas, 170, 60)
            afficher("Agir", 20, WHITE, (X_RecBas+60, Y_RecBas+20))
            #Rectangle Inventaire
            window_draw_rect(WHITE, ALPHA, X_RecBas+190, Y_RecBas, 170, 60)
            afficher("Inventaire", 20, WHITE, (X_RecBas+209, Y_RecBas+20))
            #Rectangle Shop
            window_draw_rect(WHITE, ALPHA, X_RecBas+380, Y_RecBas, 170, 60)
            afficher("Magasin", 20, WHITE, (X_RecBas+418, Y_RecBas+20))
            #Rectangle Options
            window_draw_rect(ORANGE, ALPHA, X_RecBas+570, Y_RecBas, 170, 60)
            afficher("Autre", 20, ORANGE, (X_RecBas+621, Y_RecBas+20))

            #Sauvegarder
            if choix == 1:
                #Affiche dans le rectangle du haut
                afficher("Ecrase la sauvegarde precedente.", 20, WHITE, (50, 40))
                #Math
                window_draw_rect(YELLOW, ALPHA, X_RecBas+570, Y_RecBas-96, 170, 60)
                afficher("Sauvegarder", 19, YELLOW, (X_RecBas+583, Y_RecBas-76))
                #Francais
                window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas-192, 170, 60)
                afficher("Quitter", 20, WHITE, (X_RecBas+609, Y_RecBas-172))
            #Quitter (revenir au menu principal)
            elif choix == 2:
                #Affiche dans le rectangle du haut
                afficher("Revient au menu principal.", 20, WHITE, (50, 40))
                #Math
                window_draw_rect(WHITE, ALPHA, X_RecBas+570, Y_RecBas-96, 170, 60)
                afficher("Sauvegarder", 19, WHITE, (X_RecBas+583, Y_RecBas-76))
                #Francais
                window_draw_rect(YELLOW, ALPHA, X_RecBas+570, Y_RecBas-192, 170, 60)
                afficher("Quitter", 20, YELLOW, (X_RecBas+609, Y_RecBas-172))

            #Gere les inputs
            for event in pygame.event.get():
                #Fermer la fenetre du jeu
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
               
                # Si une touche est pressee, on se deplace dans le menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        choix -= 1
                        SFX("navigate")
                    if event.key == pygame.K_UP:
                        choix += 1
                        SFX("navigate")
                    if event.key == pygame.K_LEFT:
                        return 0
                    if event.key == pygame.K_SPACE:
                        if choix == 1:
                            Sauvegarde()
                            SFX("save")
                        else:
                            SFX("select")
                            return 6

            if choix > 2:
                choix = 2
            if choix == 0:
                return 0

            pygame.display.update() #Update l'ecran

    menu_nav_run = True
    while menu_nav_run == True :
        #Tant qu'on se trouve dans le menu de navigation et qu'on ne l'a pas quitte
        
        if Avancee == 0: #Menu idle
            Avancee = Avancee0()
        elif Avancee == 1: #Menu agir
            Avancee, PPV_Actuel= Avancee1(PPV_Actuel, PPV)
        elif Avancee == 2: #Menu Inventaire
            Avancee, PPV_Actuel, PATK, PDEF = Avancee2(PPV_Actuel, PPV, PATK, PDEF)
        elif Avancee == 3: #Menu magasin
            Avancee, PARGENT = Avancee3(PARGENT)
        elif Avancee == 4: #Menu autre
            Avancee = Avancee4()
        elif Avancee == 5: #Fermer la fenetre
            pygame.quit()
            exit()
        elif Avancee == 6: #On revient dans le menu principal
            return 0
        elif Avancee == 11 or Avancee == 12 or Avancee == 13 or Avancee == 14: #Conclusion du menu agir
            Player["jour"] += 1
            Enemy_Update()
            Player["stats"][2], Player["stats"][3], Player["stats"][5], Player["stats"][6] = PATK, PDEF, PARGENT, PPV_Actuel
            return 1

def endgame():
    """Permet de lancer le generque de fin"""
    
    # Initialiser les couleurs
    WHITE, ORANGE, ALPHA = Couleurs()
    
    # Initialiser la musique
    Music("end")
    
    # Le fondu au noir
    z = pygame.Surface((800, 600), pygame.SRCALPHA) 
    z.fill((0,0,0,2))      
    
    for ALPHA in range(0,255):
        screen.blit(z, (0,0))
        pygame.display.update()
        pygame.time.wait(6)

        # Fermer le jeu pendant le generique de fin durant le fondu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


    # Le defilement du generique
    h = 680
    while h > -1400:
        
        # Fermer le jeu pendant le generique de fin 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Tant que h (pos verticale du dernier message supérieur à -10)
        screen.fill((0, 0, 0))
        afficher("Studytale", 100, WHITE, (80, h))
        afficher("Equipe", 50, WHITE, (288, h+700))
        afficher("Dany LEGUY", 35, WHITE, (265, h+830))
        afficher("Kelia SIAO", 35, WHITE, (280, h+910))
        afficher("Mathias FERTE", 35, WHITE, (230, h+990))
        afficher("THE END", 100, WHITE, (140, h+1640))
        h -= 1 # A chaque tours de boucle, la position Y diminue de 1
        pygame.display.update()
        pygame.time.wait(6)

    pygame.time.wait(3000)
    # Le deuxieme fondu au noir     
    for ALPHA in range(0,350):
        screen.blit(z, (0,0))
        pygame.display.update()
        pygame.time.wait(4)

        # Fermer le jeu pendant le generique de fin durant le fondu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


#Boucle du jeu
running = True

while running == True:

    #Edicter la conclusion lorsqu'on perd ou gagne
        #Conclu = 0 => On perd et on recommence le jeu
        #Conclu = 1 => On continue a runner le jeu
    Conclu = 1

    #Valeurs RGB de l'ecran
    screen.fill((0 ,0 ,0 ))

    #Le menu principal du jeu, permet de nommer le personnage ou alors de charger une partie sauvegardee
    Player["name"] = MainMenu(PNAME)
    #Les statistiques des ennemis sont remises a jour
    Enemy_Update()
    

    #Permet de lancer le compteur de jour, le jeu se termine au jour 15
    while Player["jour"] < 14 :

        #_____ Le menu de navigation _____
        #Permet de lancer le menu ou on selectionne ce qu'on veut faire, ca gere le deplacement, magasin, gestion du personnage etc.
        Music("nav") #Permet de jouer la musique du menu de navigation
        Conclu = menu_nav(Player["stats"]) #Lance le menu de navigation
        if Conclu == 0: #Si on a selectionne une option pour revenir au menu principal
            break

        #_____ Le combat _____
        #Les controles tous les 7 jours. Vous affrontez un boss en fonction de votre deplacement vers les matieres.
        if Player["jour"] % 7 == 0:
            #Creation d'une liste pour pouvoir dire quelle est la matiere la moins maitrisee par le joueur
            Basse = []
            #On depose dans la liste des nombres correspondant au niveau en math, francais et anglais dans les index
            for key in Player.keys():
                if key == "Math" or key == "Francais" or key == "Anglais":
                    Basse.append(Player[key])

            #Cribblage qui permet de selectionner la matiere avec le moins de points, afin d'affronter un ennemi specifique
            #Si l'index avec la valeur la plus faible de la liste est 0, on affronte le controle de math et ainsi de suite
            if Basse.index(min(Basse)) == 0:
                Conclu = battle(Ennemi["Controle de Math"], Player["stats"])
            elif Basse.index(min(Basse)) == 1:
                Conclu = battle(Ennemi["Controle de Francais"], Player["stats"])
            else:
                Conclu = battle(Ennemi["Controle d'Anglais"], Player["stats"])
            #On reinitialise la liste Basse pour pouvoir la reutiliser la prochaine fois et refaire la meme chose
            for i in range(len(Basse)):
                Basse.pop(0)
            
        #Tous les jours de la semaine, le joueur fait fasse a des distractions differentes.
        else:
            #Cette boucle for permet de passer sur toutes les clefs du dictionnaire ennemi et d'utiliser la valeur de ces clefs pour verifier si l'identifiant de l'ennemi correspond bien au nombre de jour. Ainsi fait, aucun ennemi ne tombe au hasard, a chaque jour on aura un ennemi specifique qui lui sera attribue.
            for key, value in Ennemi.items():
                if Player["jour"] % 7 == value[6]:
                    Conclu = battle(Ennemi[key], Player["stats"])
            
        if Conclu == 0: #Si on perde combat
            break

    #Si le joueur perd un combat ou decide de revenir au menu principal
    if Conclu == 0:
        continue

    Music("nav") #Permet de jouer la musique du menu de navigation
    Conclu = menu_nav(Player["stats"]) #Lance le menu de navigation

    Conclu = battle(Ennemi["Partiels"], Player["stats"])    

    #Si le joueur perd un combat ou decide de revenir au menu principal
    if Conclu == 0:
        continue

    endgame()
    