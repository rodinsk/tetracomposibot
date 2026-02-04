from robot import * 
import random
import math
nb_robots = 0
debug = True


class Robot_player(Robot):

    team_name = "Dumb"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        if self.robot_id % 4 == 0:
            self.cruise_bias = 0.2   # Tourne gauche (Cercle)
        elif self.robot_id % 4 == 1:
            self.cruise_bias = -0.2  # Tourne droite (Cercle inverse)
        elif self.robot_id % 4 == 2:
            self.cruise_bias = 0.05 
        else:
            self.cruise_bias = -0.05

        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def behavior_hateWall(self,sensor_to_wall):
        translation = sensor_to_wall[sensor_front]*0.5
        rotation = (1-sensor_to_wall[sensor_front])*random.random()+(1-sensor_to_wall[sensor_front_right]) - (1-sensor_to_wall[sensor_front_left])
        return translation, rotation
    
    def behavior_loveBot(self,sensor_to_robot):
        
        translation = 1.0
        #translation = (sensor_to_robot[sensor_front] * sensor_to_robot[sensor_front_left] * sensor_to_robot[sensor_front_right]) 
        rotation = ((sensor_to_robot[sensor_front_right] - (sensor_to_robot[sensor_front_left]))) * 2.0 
        return translation, rotation 
    
    def behavior_hateBot(self,  sensor_to_robot):
            
        #translation = -1.0  
        
        #if self.robot_id % 2 == 0:
            #rotation = 1.0 
        #else:
            #rotation = -1.0 
        translation = (sensor_to_robot[sensor_front] * sensor_to_robot[sensor_front_left] * sensor_to_robot[sensor_front_right]) *0.7
        rotation = (sensor_to_robot[sensor_front_left] - sensor_to_robot[sensor_front_right])*2.0 + (sensor_to_robot[sensor_front] == 1.0) * -0.25
        #rotation = (sensor_to_robot[sensor_front_left] - sensor_to_robot[sensor_front_right]) * 3.0 + 0.2
        return translation, rotation
    
    def behavior_cruise(self):
        
        translation = 1.0
        #rotation = (random.random()-0.5)*0.5
        rotation = self.cruise_bias + (random.random()-0.5)*0.5
        return translation , rotation 
    
    def behavior_champion(self,sensors):
        translation = sensors[sensor_front]*0.1+0.2
        rotation = 0.2 * sensors[sensor_left] + 0.2 * sensors[sensor_front_left] - 0.2 * sensors[sensor_right] - 0.2 * sensors[sensor_front_right] + (random.random()-0.5)*1. #+ sensors[sensor_front] * 0.1
        return translation, rotation

    def behavior_avoider(self,sensors):
        translation = sensors[sensor_front]*0.7
        rotation = (1-sensors[sensor_front])-(sensors[sensor_front_right]) + (sensors[sensor_front_left])
        return translation, rotation
    
    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):


        sensor_to_wall = []
        sensor_to_team = []
        sensor_to_ennemi = []
        sensor_to_robot = []

        for i in range (0,8):
            if  sensor_view[i] == 1:
                sensor_to_wall.append( sensors[i] )
                sensor_to_team.append(1.0)
                sensor_to_ennemi.append(1.0)
                sensor_to_robot.append(1.0)
            elif  sensor_view[i] == 2:
                sensor_to_wall.append( 1.0 )
                sensor_to_robot.append( sensors[i] )
                if sensor_team[i] == self.team_name:
                    sensor_to_team.append( sensors[i] )
                    sensor_to_ennemi.append(1.0)
                else:
                    sensor_to_team.append( 1.0 )
                    sensor_to_ennemi.append( sensors[i] )
            else:
                sensor_to_wall.append(1.0)
                sensor_to_team.append(1.0)
                sensor_to_ennemi.append(1.0)
                sensor_to_robot.append(1.0)

        if debug == True:
            if self.iteration % 100 == 0:
                print ("Robot",self.robot_id," (team "+str(self.team_name)+")","at step",self.iteration,":")
                print ("\tsensors (distance, max is 1.0)  =",sensors)
                print ("\t\tsensors to wall  =",sensor_to_wall)
                #print ("\t\tsensors to robot =",sensor_to_robot)
                print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
                print ("\trobot's name (if relevant)      =",sensor_robot)
                print ("\trobot's team (if relevant)      =",sensor_team)

        wall = sensor_to_wall[sensor_front] * sensor_to_wall[sensor_front_left] * sensor_to_wall[sensor_front_right]
        ennemi = sensor_to_ennemi[sensor_front] * sensor_to_ennemi[sensor_front_left] * sensor_to_ennemi[sensor_front_right]
        robot = sensor_to_robot[sensor_front] * sensor_to_robot[sensor_front_left] * sensor_to_robot[sensor_front_right]
        team = sensor_to_team[sensor_front] * sensor_to_team[sensor_front_left] * sensor_to_team[sensor_front_right]

        
        
        if wall < 0.5:
            translation, rotation = self.behavior_hateWall(sensor_to_wall)
         
        elif sensor_team[sensor_front] == "A" or sensor_team[sensor_left] == "A" or sensor_team[sensor_front_left] == "A" or sensor_team[sensor_right] == "A" or sensor_team[sensor_front_right] == "A" or sensor_team[sensor_rear] == "A" or sensor_team[sensor_rear_left] == "A" or sensor_team[sensor_rear_right] == "A" and robot < 0.8 :
            translation, rotation = self.behavior_hateBot(sensor_to_team)
       
        elif ennemi < 1.0 :
            translation, rotation = self.behavior_loveBot(sensor_to_ennemi)
        else:
            translation, rotation = self.behavior_cruise()
    

        self.iteration = self.iteration + 1        
        return translation, rotation, False
