# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : _________
#  Prénom Nom No_étudiant/e : _________
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

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



        for i in range (0,8):
            if  sensor_view[i] == 1:
                sensor_to_wall.append( sensors[i] )
                sensor_to_robot.append(1.0)
                sensor_to_team.append(1.0)
            elif  sensor_view[i] == 2:
                sensor_to_wall.append( 1.0 )
                sensor_to_robot.append( sensors[i])
                if sensor_team[i] == self.team_name:
                    sensor_to_team.append(sensors[i])
                else:
                    sensor_to_team.append(1.0)
            else:
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)
                sensor_to_team.append(1.0)

        wall = sensor_to_wall[sensor_front] * sensor_to_wall[sensor_front_left] * sensor_to_wall[sensor_front_right]
        robot = sensor_to_robot[sensor_front] * sensor_to_robot[sensor_front_left] * sensor_to_robot[sensor_front_right]
        team = sensor_to_team[sensor_front] * sensor_to_team[sensor_front_left] * sensor_to_team[sensor_front_right]

        
        print("\tIDDD : ", self.robot_id)
        print("Team : ", team)
        print("Robot : ", robot)

        # Robot qui fait tout (pour l'instant)
        if(self.robot_id == 0):
            if wall  < 0.15:
                translation = -0.7
                rotation = random.random() * 2.0 - 1.0 

            if wall < 0.5 :
                translation = sensor_to_wall[sensor_front]*0.5
                rotation = (1-sensor_to_wall[sensor_front])*random.random()+(1-sensor_to_wall[sensor_front_right]) - (1-sensor_to_wall[sensor_front_left])
        
            elif team < 0.9:
                translation = (sensor_to_robot[sensor_front] * sensor_to_robot[sensor_front_left] * sensor_to_robot[sensor_front_right]) *0.7
                rotation = (sensor_to_robot[sensor_front_left] - sensor_to_robot[sensor_front_right])*2.0 + (sensor_to_robot[sensor_front] == 1.0) * -0.25

            elif robot < 0.9:
                translation = (sensor_to_robot[sensor_front] * sensor_to_robot[sensor_front_left] * sensor_to_robot[sensor_front_right]) 
                rotation = ((sensor_to_robot[sensor_front_right] - (sensor_to_robot[sensor_front_left]))) * 2.0 
            else:
                translation = 0.9
                rotation = 0.0 + random.random()* 1.1 - random.random() * 1.1
        #Robot qui évite tout
        elif self.robot_id == 1:
            if wall < 0.5 :
                translation = sensor_to_wall[sensor_front]*0.4 
                rotation = ((random.random() * 2.0 - 1 )*(1-sensors[sensor_front]) * 0.7 - (sensors[sensor_front_right]) *0.6 + (sensors[sensor_front_left]) *0.6  + (sensors[sensor_left]) * 0.5 - (sensors[sensor_right]) * 0.5 + (sensors[sensor_rear_left]) * 0.5 - (sensors[sensor_rear_right]) * 0.5 ) * 0.3
            elif robot < 0.9:
                translation = (sensor_to_robot[sensor_front] * sensor_to_robot[sensor_front_left] * sensor_to_robot[sensor_front_right]) *0.7
                rotation = (sensor_to_robot[sensor_front_left] - sensor_to_robot[sensor_front_right])*2.0 + (sensor_to_robot[sensor_front] == 1.0) * -0.25
            else:
                translation = 1
                rotation = (random.random() * 2.0 - 1 )*(1-sensors[sensor_front]) * 0.8 - (sensors[sensor_front_right]) *0.6 + (sensors[sensor_front_left]) *0.6  + (sensors[sensor_left]) * 0.5 - (sensors[sensor_right]) * 0.5
        # Robot qui suit les ennemis
        elif self.robot_id == 2:
            if wall  < 0.15:
                translation = -0.7
                rotation = random.random() * 2.0 - 1.0 

            if wall < 0.5 :
                translation = sensor_to_wall[sensor_front]*0.5
                rotation = (1-sensor_to_wall[sensor_front])*random.random()+(1-sensor_to_wall[sensor_front_right]) - (1-sensor_to_wall[sensor_front_left])
            else:
                translation = 0.9
                rotation = 0.0 + random.random()* 1.1 - random.random() * 1.1
        elif self.robot_id == 3:
            translation = 0.9
            rotation = 0.0 + random.random()* 1.1 - random.random() * 1.1

        return translation, rotation, False

