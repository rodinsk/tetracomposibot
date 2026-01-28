# Configuration file.

import arenas

# general -- first three parameters can be overwritten with command-line arguments (cf. "python tetracomposibot.py --help")

display_mode = 0
arena = 2
position = False 
max_iterations = 2000 #401*500
max_iterations = 2001 #401*500

# affichage

display_welcome_message = False
verbose_minimal_progress = True # display iterations
display_robot_stats = False
display_team_stats = False
display_tournament_results = False
display_time_stats = True

# initialization : create and place robots at initial positions (returns a list containing the robots)

import robot_dumb
import robot_braitenberg_avoider as robotavoider
import robot_braitenberg_loveWall as robotlovewall
import robot_braitenberg_avoider
import robot_braitenberg_hateWall
import robot_braitenberg_loveBot

def initialize_robots(arena_size=-1, particle_box=-1): # particle_box: size of the robot enclosed in a square
    #x_center = arena_size // 2 - particle_box / 2
    y_center = arena_size // 2 - particle_box / 2
    robots = []
<<<<<<< HEAD
    robots.append(robot_braitenberg_avoider.Robot_player(4, y_center, 0, name="My Robot", team="A"))
    robots.append(robot_braitenberg_loveBot.Robot_player(93, y_center, 90, name="My Robot", team="A"))
=======
    robots.append(robotavoider.Robot_player(4, y_center, 0, name="Avoider", team="A"))
    robots.append(robotlovewall.Robot_player(80, y_center, 0, name="LoverWall", team="A"))
    robots.append(robot_braitenberg_hateWall.Robot_player(4, y_center, 0, name="My Robot", team="A"))
    robots.append(robot_braitenberg_hateWall.Robot_player(93, y_center, 90, name="My Robot", team="A"))
>>>>>>> 3200ede506f345855c4adc0357a9d92e71b02402
    return robots
