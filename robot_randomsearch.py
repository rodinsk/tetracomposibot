
from robot import * 
import math

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "Optimizer"
    robot_id = -1
    iteration = 0

    param = []
    bestParam = []
    it_per_evaluation = 400
    trial = 0

    bestScore = -100000 ; # ex1

    x_0 = 0
    y_0 = 0
    theta_0 = 0 # in [0,360]

   

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a",evaluations=0,it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        self.param = [random.randint(-1, 1) for i in range(8)]
        self.it_per_evaluation = it_per_evaluation

        #ex1
        self.score = 0
        self.old_x = x_0
        self.old_y = y_0
        self.old_theta = theta_0

        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        # ex1 
        self.score = 0
        self.old_x = self.x
        self.old_y = self.y
        self.old_theta = self.theta
        super().reset()

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        # cet exemple montre comment générer au hasard, et évaluer, des stratégies comportementales
        # Remarques:
        # - la liste "param", définie ci-dessus, permet de stocker les paramètres de la fonction de contrôle
        # - la fonction de controle est une combinaison linéaire des senseurs, pondérés par les paramètres (c'est un "Perceptron")

        # toutes les X itérations: le robot est remis à sa position initiale de l'arène avec une orientation aléatoire

        # Translation effective 
        dist_translation = math.sqrt((self.x - self.old_x)**2 + (self.y - self.old_y)**2)
        # Rotation effective
        dist_rotation = abs(self.theta - self.old_theta)
        #score
        self.score += dist_translation * (1 - dist_rotation)
        #mise à jour
        self.old_x = self.x
        self.old_y = self.y
        self.old_theta = self.theta

        if self.iteration % self.it_per_evaluation == 0:
                if self.iteration > 0:
                    print ("\tparameters           =",self.param)
                    print ("\ttranslations         =",self.log_sum_of_translation,"; rotations =",self.log_sum_of_rotation) # *effective* translation/rotation (ie. measured from displacement)
                    print ("\tdistance from origin =",math.sqrt((self.x-self.x_0)**2+(self.y-self.y_0)**2))
                    #ex1
                    print ("\tscore                =",self.score)
                    if self.score > self.bestScore:
                        self.bestScore = self.score
                        self.bestParam = self.param[:] 
                        self.bestTrial = self.trial   
                        print ("\t>>> New best score! (Trial "+str(self.trial)+") <<<")

                if self.trial < 500:
                    # CAS 1 : On cherche encore (Essais 0 à 499)
                    self.param = [random.randint(-1, 1) for i in range(8)]
                    print ("Starting trial no.", self.trial + 1)
                
                else:
                    # CAS 2 : On a fini les 500 essais -> On joue le meilleur
                    print ("xxx REPLAY BEST STRATEGY (found at trial", self.bestTrial, ") xxx")
                    print ("xxx Best Score was:", self.bestScore)
                    print ("xxx Best Params:", self.bestParam)
                    
                    self.param = self.bestParam[:] # On remet les paramètres du champion
                    self.it_per_evaluation = 1000  # On passe à 1000 itérations comme demandé
                
                self.trial = self.trial + 1
                self.iteration = self.iteration + 1
                return 0, 0, True # ask for reset
        
                
                #self.param = [random.randint(-1, 1) for i in range(8)]
                #self.trial = self.trial + 1
                #print ("Trying strategy no.",self.trial)
                #self.iteration = self.iteration + 1
                #return 0, 0, True # ask for reset

        # fonction de contrôle (qui dépend des entrées sensorielles, et des paramètres)
        translation = math.tanh ( self.param[0] + self.param[1] * sensors[sensor_front_left] + self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right] )
        rotation = math.tanh ( self.param[4] + self.param[5] * sensors[sensor_front_left] + self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right] )

        if debug == True:
            if self.iteration % 100 == 0:
                print ("Robot",self.robot_id," (team "+str(self.team_name)+")","at step",self.iteration,":")
                print ("\tsensors (distance, max is 1.0)  =",sensors)
                print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
                print ("\trobot's name (if relevant)      =",sensor_robot)
                print ("\trobot's team (if relevant)      =",sensor_team)

        self.iteration = self.iteration + 1        
        
        return translation, rotation, False
