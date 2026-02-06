


from robot import * 
import random


nb_robots = 0
debug =  False

class Robot_player(Robot):

    team_name = "Dumb"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

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
        
        wall = sensor_to_wall[sensor_front] * sensor_to_wall[sensor_front_left] * sensor_to_wall[sensor_front_right] * sensor_to_wall[sensor_left] * sensor_to_wall[sensor_right]
        robot = sensor_to_robot[sensor_front] * sensor_to_robot[sensor_front_left] * sensor_to_robot[sensor_front_right]
        team = sensor_to_team[sensor_front] * sensor_to_team[sensor_front_left] * sensor_to_team[sensor_front_right]

        
        
        translation = ((sensors[sensor_front] * 1.4) - 0.1) * 0.4
        #rotation = (random.random() * 2.0 - 1 )*(1-sensors[sensor_front]) * 0.8 - (sensors[sensor_front_right]) *0.6 + (sensors[sensor_front_left]) *0.6  + (sensors[sensor_left]) * 0.5 - (sensors[sensor_right]) * 0.5
        rotation = (random.random() * 2.0 - 1 )*(1-sensors[sensor_front]) * 0.8 - (sensors[sensor_front_right]) *0.6 + (sensors[sensor_front_left]) *0.6  + (sensors[sensor_left]) * 0.5 - (sensors[sensor_right]) * 0.5

     
        if wall < 0.5 :
            translation = sensor_to_wall[sensor_front]*0.4 
            rotation = ((random.random() * 2.0 - 1 )*(1-sensors[sensor_front]) * 0.7 - (sensors[sensor_front_right]) *0.6 + (sensors[sensor_front_left]) *0.6  + (sensors[sensor_left]) * 0.5 - (sensors[sensor_right]) * 0.5 + (sensors[sensor_rear_left]) * 0.5 - (sensors[sensor_rear_right]) * 0.5 ) * 0.3
        elif robot < 0.9:
                translation = (sensor_to_robot[sensor_front] * sensor_to_robot[sensor_front_left] * sensor_to_robot[sensor_front_right]) *0.7
                rotation = (sensor_to_robot[sensor_front_left] - sensor_to_robot[sensor_front_right])*2.0 + (sensor_to_robot[sensor_front] == 1.0) * -0.25 
        else:
            translation = 1
            rotation = (random.random() * 2.0 - 1 )*(1-sensors[sensor_front]) * 0.8 - (sensors[sensor_front_right]) *0.6 + (sensors[sensor_front_left]) *0.6  + (sensors[sensor_left]) * 0.5 - (sensors[sensor_right]) * 0.5



        if debug == True:
            if self.iteration % 100 == 0:
                print ("Robot",self.robot_id," (team "+str(self.team_name)+")","at step",self.iteration,":")
                print ("\tsensors (distance, max is 1.0)  =",sensors)
                print ("\t\tsensors to wall  =",sensor_to_wall)
                print ("\t\tsensors to robot =",sensor_to_robot)
                print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
                print ("\trobot's name (if relevant)      =",sensor_robot)
                print ("\trobot's team (if relevant)      =",sensor_team)
                print ("\t rotation   =" , rotation)
                print ("\t translation =", translation)
        
        self.iteration = self.iteration + 1        
        return translation, rotation, False
