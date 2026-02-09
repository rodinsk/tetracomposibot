import math
from robot import * 
import random

nb_robots = 0

class Robot_player(Robot):
    
    # Nom d'équipe
    team_name = "Fraise framboise myrtille"
    robot_id = -1
    
    # Contrainte respectée : memory est initialisé à 0 (int)
    # Nous allons l'utiliser comme un COMPTEUR pour la marche arrière.
    memory = 0 

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)
        
        # Paramètres génétiques (définis une seule fois ici pour le Robot 3)
        if self.robot_id == 3:
            self.genetic_params = [-1, -1, 1, -1, 0, 1, 1, 0]

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        
        # 1. Gestion du déblocage (Unstuck logic) avec un entier
        # Si memory > 0, cela veut dire qu'on est en train de reculer
        if self.memory > 0:
            self.memory -= 1 # On décrémente le compteur
            # Marche arrière et rotation aléatoire pour se dégager
            return -0.7, random.choice([-1.0, 1.0])

        # 2. Analyse des capteurs
        sensor_to_wall = []
        sensor_to_team = []   # Amis
        sensor_to_ennemi = [] # Ennemis

        for i in range(8):
            dist = sensors[i]
            view = sensor_view[i]
            
            # Initialisation par défaut (1.0 = loin / rien)
            w, t, e = 1.0, 1.0, 1.0

            if view == 1: # Mur
                w = dist
            elif view == 2: # Robot
                if sensor_team[i] == self.team_name:
                    t = dist # C'est un ami
                else:
                    e = dist # C'est un ennemi
            
            sensor_to_wall.append(w)
            sensor_to_team.append(t)
            sensor_to_ennemi.append(e)

        # Calcul des produits frontaux (Cone de vision devant le robot)
        # Plus la valeur est petite, plus l'obstacle est proche
        wall_front = sensor_to_wall[sensor_front] * sensor_to_wall[sensor_front_left] * sensor_to_wall[sensor_front_right]
        team_front = sensor_to_team[sensor_front] * sensor_to_team[sensor_front_left] * sensor_to_team[sensor_front_right]
        ennemi_front = sensor_to_ennemi[sensor_front] * sensor_to_ennemi[sensor_front_left] * sensor_to_ennemi[sensor_front_right]

        # Déclenchement du mécanisme de déblocage (Si trop près d'un mur)
        if sensors[sensor_front] < 0.15 or sensors[sensor_front_left] < 0.1 or sensors[sensor_front_right] < 0.1:
            # Si on est collé, on initialise le compteur à 10 tours de marche arrière
            # (Sauf pour le robot chasseur qui peut vouloir coller un ennemi)
            if not (self.robot_id == 2 and ennemi_front < 0.5):
                self.memory = 10 
                return 0, 0 # On s'arrête ce tour-ci, au prochain on recule

        translation = 0
        rotation = 0

        # --- COMPORTEMENTS SPÉCIFIQUES ---

        # Robot 0 : Champion Amélioré (Explorateur)
        if self.robot_id == 0:
            translation = 1.0 # Toujours à fond
            # Braitenberg simple : évite les obstacles (murs et amis)
            # On combine les capteurs murs et amis pour l'évitement
            left_obstacle = min(sensor_to_wall[sensor_front_left], sensor_to_team[sensor_front_left])
            right_obstacle = min(sensor_to_wall[sensor_front_right], sensor_to_team[sensor_front_right])
            
            # Si obstacle à gauche, tourne à droite, et inversement
            rotation = (left_obstacle - right_obstacle) * 1.5
            # Ajout d'un bruit aléatoire pour l'exploration
            rotation += (random.random() - 0.5) * 0.2

        # Robot 1 : L'éviteur (Peureux)
        elif self.robot_id == 1:
            # Très sensible aux murs et aux autres robots
            if wall_front < 0.6 or team_front < 0.8:
                translation = 0.4
                # Tourne à l'opposé de l'obstacle
                rotation = (sensor_to_wall[sensor_front_left] - sensor_to_wall[sensor_front_right]) * 2.0
            else:
                translation = 0.8
                # Oscille légèrement pour couvrir de la surface
                rotation = math.cos(nb_robots) * 0.5 # Juste pour varier

        # Robot 2 : Le Chasseur (Hunter)
        elif self.robot_id == 2:
            # 1. Éviter les murs (Priorité absolue)
            if wall_front < 0.4:
                translation = 0.2
                rotation = (sensor_to_wall[sensor_front_left] - sensor_to_wall[sensor_front_right]) * 3.0
            
            # 2. Éviter les amis (Pour ne pas se bloquer mutuellement)
            elif team_front < 0.6:
                translation = 0.0
                rotation = 1.0 # Tourne sur place
            
            # 3. Chasser l'ennemi
            elif ennemi_front < 1.0:
                translation = 1.0 # Fonce
                # Braitenberg "Love" : on va VERS la cible.
                # Si ennemi à gauche (valeur faible), on veut tourner à gauche (rotation positive)
                # Formule : (Droite - Gauche)
                rotation = (sensor_to_ennemi[sensor_front_right] - sensor_to_ennemi[sensor_front_left]) * 2.5
            
            # 4. Rien en vue : Patrouille
            else:
                translation = 1.0
                rotation = (random.random() - 0.5) * 0.5

        # Robot 3 : Génétique (Optimisé)
        elif self.robot_id == 3:
            p = self.genetic_params
            # Utilisation de tanh pour normaliser entre -1 et 1
            translation = math.tanh(p[0] + p[1] * sensors[sensor_front_left] + p[2] * sensors[sensor_front] + p[3] * sensors[sensor_front_right])
            rotation = math.tanh(p[4] + p[5] * sensors[sensor_front_left] + p[6] * sensors[sensor_front] + p[7] * sensors[sensor_front_right])

        return translation, rotation, False