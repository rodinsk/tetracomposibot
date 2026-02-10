# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : _________
#  Prénom Nom No_étudiant/e : _________
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

import math
from robot import * 
import random

nb_robots = 0

class Robot_player(Robot):

    team_name = "Fraise framboise myrtille"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0                # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        translation = sensors[sensor_front]
        rotation = 1.0 * sensors[sensor_front_left] - 1.0 * sensors[sensor_front_right] + (random.random()-0.5)*0.1
       
        sensor_to_wall = []
        sensor_to_robot = []
        sensor_to_team = []
        sensor_to_ennemi = []



        for i in range (0,8):
            if  sensor_view[i] == 1:
                sensor_to_wall.append( sensors[i] )
                sensor_to_robot.append(1.0)
                sensor_to_team.append(1.0)

                sensor_to_ennemi.append(1.0)
            elif  sensor_view[i] == 2:
                sensor_to_wall.append( 1.0 )
                sensor_to_robot.append( sensors[i])
                if sensor_team[i] == self.team_name:
                    sensor_to_team.append(sensors[i])
                    sensor_to_ennemi.append(1.0)
                else:
                    sensor_to_team.append(1.0)
                    sensor_to_ennemi.append(sensors[i])
            else:
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)
                sensor_to_team.append(1.0)
                sensor_to_ennemi.append(1.0)

        
        wall = sensor_to_wall[sensor_front] * sensor_to_wall[sensor_front_left] * sensor_to_wall[sensor_front_right]
        robot = sensor_to_robot[sensor_front] * sensor_to_robot[sensor_front_left] * sensor_to_robot[sensor_front_right]
        team = sensor_to_team[sensor_front] * sensor_to_team[sensor_front_left] * sensor_to_team[sensor_front_right]
        ennemi = sensor_to_ennemi[sensor_front] * sensor_to_ennemi[sensor_front_left] * sensor_to_ennemi[sensor_front_right]

        #print("team : ", self.team , "team name :", self.team_name, "Robot : " + sensor_team[sensor_front])

        """
        # Robot qui fait tout (pour l'instant) ( Cham)
        if(self.robot_id == 3):
            if team < 0.9:
                translation = (sensor_to_robot[sensor_front] * sensor_to_robot[sensor_front_left] * sensor_to_robot[sensor_front_right]) *0.7
                rotation = (sensor_to_robot[sensor_front_left] - sensor_to_robot[sensor_front_right])*2.0 + (sensor_to_robot[sensor_front] == 1.0) * -0.25
            elif wall < 0.5 :
                translation = sensor_to_wall[sensor_front]*0.5
                rotation = (1-sensor_to_wall[sensor_front])*random.random()+(1-sensor_to_wall[sensor_front_right]) - (1-sensor_to_wall[sensor_front_left])
            

            elif robot < 0.9:
                translation = (sensor_to_robot[sensor_front] * sensor_to_robot[sensor_front_left] * sensor_to_robot[sensor_front_right]) 
                rotation = ((sensor_to_robot[sensor_front_right] - (sensor_to_robot[sensor_front_left]))) * 2.0 
            else:
                translation = 0.9
                rotation = 0.0 + random.random()* 1.1 - random.random() * 1.1
        """
        #Robot champion amélioré
        if self.robot_id == 0:
            if random.random() < 0.005 and abs(self.memory - sensors[sensor_front]) < 0.05 and  self.memory!= 0:
                translation = -0.7
                rotation = random.random() * 2.0 - 1
            else: 
                translation = 1.0
                rotation = 0.2 * sensors[sensor_left] + 0.2 * sensors[sensor_front_left] - 0.2 * sensors[sensor_right] - 0.2 * sensors[sensor_front_right] + (random.random()-0.5)*1. #+ sensors[sensor_front] * 0.1
        #Robot qui évite tout
        # === ROBOT 1 : LE FANTÔME (Vitesse Max + Évitement Total) ===
        elif self.robot_id == 1:
            
            if random.random() < 0.1 and abs(self.memory - sensors[sensor_front]) < 0.05 and self.memory != 0:
                translation = -1.0 # Recule à fond (-0.7 -> -1.0)
                rotation = random.random() * 2.0 - 1
            
            # Évitement Robot
            elif robot < 0.9:
                # Vitesse augmentée (* 0.7 -> * 1.0)
                translation = (sensor_to_robot[sensor_front] * sensor_to_robot[sensor_front_left] * sensor_to_robot[sensor_front_right]) * 1.0
                # Rotation plus forte (* 2.0 -> * 3.0)
                rotation = (sensor_to_robot[sensor_front_left] - sensor_to_robot[sensor_front_right]) * 3.0 + (sensor_to_robot[sensor_front] == 1.0) * -0.5
            
            # Évitement Mur
            elif wall < 0.5 :
                # Vitesse augmentée (* 0.4 -> * 1.0)
                translation = sensor_to_wall[sensor_front] * 1.0 
                # J'ai gardé ta longue formule mais changé le multiplicateur final (* 0.3 -> * 1.5)
                # C'est ça qui l'empêchait de tourner assez vite !
                rotation = ((random.random() * 2.0 - 1 )*(1-sensors[sensor_front]) * 0.5 - (sensors[sensor_front_right]) * 0.9 + (sensors[sensor_front_left]) * 0.9  + (sensors[sensor_left]) * 0.8 - (sensors[sensor_right]) * 0.8 + (sensors[sensor_rear_left]) * 0.2 - (sensors[sensor_rear_right]) * 0.2 ) * 1.5
            
            # Croisière (Pas d'obstacle)
            else:
                translation = 1.0 # Vitesse max (0.7 -> 1.0)
                # Rotation plus stable pour aller tout droit mais éviter les bords
                rotation = (random.random() * 2.0 - 1 )*(1-sensors[sensor_front]) * 0.5 - (sensors[sensor_front_right]) * 0.8 + (sensors[sensor_front_left]) * 0.8  + (sensors[sensor_left]) * 0.5 - (sensors[sensor_right]) * 0.5
        # Robot qui suit les ennemis
        elif self.robot_id == 2:
            print(self.memory - sensors[sensor_front])
            if random.random() < 0.005 and abs(self.memory - sensors[sensor_front]) < 0.05:
                translation = -0.8
                rotation = random.random() * 2.0 - 1
            
            if sensors[sensor_front] < 0.15 or sensors[sensor_front_left] < 0.15 or sensors[sensor_front_right] < 0.15:
                self.memory = 10 # On va reculer pendant 10 steps
                return 0, 0, False

            translation = 1.0
            rotation = 0
            # Si on voit un robot (View == 2) et que ce n'est pas mon équipe
            for i in range(8):
                if sensor_view[i] == 2 and sensor_team[i] != self.team_name:
                    # On fonce dessus (simple Braitenberg Love)
                    # Si c'est à droite (i > 3), on tourne à droite
                    if i > 3: rotation = 1.0
                    else: rotation = -1.0
                    break
        #Algo génétique
        elif self.robot_id == 3:
            if random.random() < 0.05 and abs(self.memory - sensors[sensor_front]) < 0.05 and abs(self.memory - 1.0)  > 0.05:
                translation = -1
                rotation = random.random() * 2.0 - 1
            elif robot < 0.9:
                translation = (sensor_to_robot[sensor_front] * sensor_to_robot[sensor_front_left] * sensor_to_robot[sensor_front_right]) *0.8
                rotation = (sensor_to_robot[sensor_front_left] - sensor_to_robot[sensor_front_right])*2.0 + (sensor_to_robot[sensor_front] == 1.0) * -0.25
            elif random.random() < 0.1:
                translation = 1
                rotation = random.random() * 2.0 - 1
            else:
                self.param= [1, 0, 1, 1, 1, 1, -1, -1]
                translation = math.tanh ( self.param[0] + self.param[1] * sensors[sensor_front_left] + self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right] )
                rotation = math.tanh ( self.param[4] + self.param[5] * sensors[sensor_front_left] + self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right] )
        self.memory = sensors[sensor_front]

        return translation, rotation, False

