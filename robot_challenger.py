# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : NSIKU TOMONO Rodi 21302437
#  Prénom Nom No_étudiant/e : HUANG Hongshuo    21304319
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

        
        wall = sensor_to_wall[sensor_front] * sensor_to_wall[sensor_front_left] * sensor_to_wall[sensor_front_right] * sensor_to_wall[sensor_left] * sensor_to_wall[sensor_right]
        robot = sensor_to_robot[sensor_front] * sensor_to_robot[sensor_front_left] * sensor_to_robot[sensor_front_right] *sensor_to_robot[sensor_left] * sensor_to_robot[sensor_right] * sensor_to_robot[sensor_rear_left] * sensor_to_robot[sensor_rear_right]
        team = sensor_to_team[sensor_front] * sensor_to_team[sensor_front_left] * sensor_to_team[sensor_front_right]

        
        #Robot champion amélioré
        if self.robot_id == 0:
            if random.random() < 0.005 and abs(self.memory - sensors[sensor_front]) < 0.05 and abs(self.memory - 1.0)  > 0.05:
                translation = -0.5
                rotation = random.random() * 2.0 - 1
            else: 
                translation = sensors[sensor_front]*0.1+0.7
                rotation = 0.2 * sensors[sensor_left] + 0.2 * sensors[sensor_front_left] - 0.2 * sensors[sensor_right] - 0.2 * sensors[sensor_front_right] + (random.random()-0.5)*1. #+ sensors[sensor_front] * 0.1
        #Robot qui évite tout
        elif self.robot_id == 1:
            if random.random() < 0.1 and ( abs(self.memory - sensors[sensor_front]) < 0.05 or wall < 0.1 ) :
                translation = -0.25
                rotation = random.choice([-0.5, 0, 0.5])
            
            elif robot < 0.9:
                translation = (sensor_to_robot[sensor_front] * sensor_to_robot[sensor_front_left] * sensor_to_robot[sensor_front_right]) *0.8 + 0.5
                rotation = (sensor_to_robot[sensor_front_left] - sensor_to_robot[sensor_front_right] + sensor_to_robot[sensor_right] + sensor_to_robot[sensor_left])*2.0 + (sensor_to_robot[sensor_front] != 1.0) * 0.4 + (random.random() * 2.0 -1) * 0.5
            
            elif wall < 0.5 :
                translation = (sensor_to_wall[sensor_front] * 0.9) 
                rotation = ( (1-sensors[sensor_front]) * 0.7 - (sensors[sensor_front_right]) *0.5 + (sensors[sensor_front_left]) *0.5  + (sensors[sensor_left]) * 0.5 - (sensors[sensor_right]) * 0.5 + (sensors[sensor_rear_left]) * 0.5 - (sensors[sensor_rear_right]) * 0.5 ) * 0.15 + random.random() * 0.8 -0.4
                
            else:
                translation = 1
                rotation = (random.random() * 2.0 - 1 )*(1-sensors[sensor_front]) * 0.8 - (sensors[sensor_front_right]) *0.6 + (sensors[sensor_front_left]) *0.6  + (sensors[sensor_left]) * 0.5 - (sensors[sensor_right]) * 0.5

        # Robot qui suit les ennemis
        elif self.robot_id == 2:
            #print(self.memory - sensors[sensor_front])
            if random.random() < 0.15 and abs(self.memory - sensors[sensor_front]) < 0.1 and abs(self.memory - 1.0)  > 0.05 :
                translation = -1
                rotation = random.random() * 2.0 -1
            elif team < 0.9 : 
                translation = (sensor_to_robot[sensor_front] * sensor_to_robot[sensor_front_left] * sensor_to_robot[sensor_front_right]) *0.7
                rotation = rotation = 0.2 * sensor_to_robot[sensor_left] + 0.2 * sensor_to_robot[sensor_front_left] - 0.2 * sensor_to_robot[sensor_right] - 0.2 * sensor_to_robot[sensor_front_right] + (random.random()-0.5)*1
            
            elif wall < 0.5:
                translation = sensor_to_wall[sensor_front]*0.5
                rotation = (1-sensor_to_wall[sensor_front])*random.random()+(1-sensor_to_wall[sensor_front_right]) - (1-sensor_to_wall[sensor_front_left])
        
            elif robot < 1.0 :
                translation = 1.0
                rotation = ((sensor_to_robot[sensor_front_right] - (sensor_to_robot[sensor_front_left]))) * 2.0
            else:
                translation = 1.0
                rotation =  (random.random()-0.5)*0.5

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

