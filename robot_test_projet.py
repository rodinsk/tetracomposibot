from robot import * 
import random

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "Dumb" # Assure-toi que c'est le même nom dans le fichier config !
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def behavior_hateWall(self, sensor_to_wall):
        # CORRECTION 3 : On enlève le Random qui fait trembler le robot
        translation = max(0.3, sensor_to_wall[sensor_front]*0.5)
        # On tourne simplement à l'opposé du mur (Gauche - Droite)
        rotation = (sensor_to_wall[sensor_front_left] - sensor_to_wall[sensor_front_right]) * 2.5
        return translation, rotation
    
    def behavior_loveBot(self, sensor_to_robot):
        # On fonce (vitesse 1.0)
        translation = 1.0
        # On tourne VERS l'ennemi (Droite - Gauche)
        rotation = (sensor_to_robot[sensor_front_right] - sensor_to_robot[sensor_front_left]) * 2.5 
        return translation, rotation 
    
    def behavior_hateBot(self, sensor_to_robot):
        # CORRECTION 2 : L'ANTI-BLOCAGE (Pair/Impair)
        # C'est vital. Si tu ne mets pas ça, tes robots vont rester collés.
        
        dist_front = sensor_to_robot[sensor_front]
        
        # Si on est collé (< 0.5), on recule
        if dist_front < 0.5:
             translation = -1.0 # Marche arrière
             
             # Règle Pair/Impair pour casser la symétrie
             # Le robot Pair tourne à GAUCHE, l'Impair à DROITE
             if self.robot_id % 2 == 0:
                 rotation = 1.0 
             else:
                 rotation = -1.0
        else:
             # Evitement doux si on n'est pas encore collé
             translation = 0.6
             rotation = (sensor_to_robot[sensor_front_left] - sensor_to_robot[sensor_front_right]) * 2.0
             
        return translation, rotation
    
    def behavior_cruise(self):
        translation = 1.0
        rotation = (random.random()-0.5)*0.2
        return translation , rotation 

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        sensor_to_wall = []
        sensor_to_team = []
        sensor_to_ennemi = []

        # 1. TRI DES CAPTEURS
        for i in range (0,8):
            obj_type = sensor_view[i]
            dist = sensors[i]
            
            # Valeurs par défaut (1.0 = rien)
            w, t, e = 1.0, 1.0, 1.0

            if obj_type == 1: # MUR
                w = dist
            elif obj_type == 2: # ROBOT
                if sensor_team[i] == self.team_name:
                    t = dist
                else:
                    e = dist
            
            sensor_to_wall.append(w)
            sensor_to_team.append(t)
            sensor_to_ennemi.append(e)

        # 2. CALCUL DES DISTANCES (PRODUIT)
        wall = sensor_to_wall[sensor_front] * sensor_to_wall[sensor_front_left] * sensor_to_wall[sensor_front_right]
        # Ici, 'team' représente la proximité de ton équipe
        team = sensor_to_team[sensor_front] * sensor_to_team[sensor_front_left] * sensor_to_team[sensor_front_right]
        ennemi = sensor_to_ennemi[sensor_front] * sensor_to_ennemi[sensor_front_left] * sensor_to_ennemi[sensor_front_right]

        # 3. LOGIQUE DE DECISION
        
        # Priorité 1 : Mur
        if wall < 0.5:
            translation, rotation = self.behavior_hateWall(sensor_to_wall)
         
        # Priorité 2 : Equipe (CORRECTION 1 : LE BUG DU "A")
        # On utilise simplement la variable 'team' calculée au-dessus.
        # Si team < 0.8, ça veut dire qu'un ami est proche.
        elif team < 0.8:
            translation, rotation = self.behavior_hateBot(sensor_to_team)
       
        # Priorité 3 : Ennemi
        elif ennemi < 1.0 :
            translation, rotation = self.behavior_loveBot(sensor_to_ennemi)
            
        # Priorité 4 : Rien
        else:
            translation, rotation = self.behavior_cruise()
    
        self.iteration = self.iteration + 1        
        return translation, rotation, False