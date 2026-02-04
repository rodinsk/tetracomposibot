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

    old_log_sum_of_translation = 0
    old_log_sum_of_rotation = 0
    score = 0

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
        self.old_log_sum_of_translation = 0
        self.old_log_sum_of_rotation = 0
        self.score = 0

        #ex2
        self.final_score = 0          # Score final
        self.sub_evaluation = 0       # 0 à 2
        self.cumulated_score = 0      # Somme des scores
        self.nb_repeats = 3           # Nombre de répétitions

        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        
        #ex1
        self.score = 0
        self.log_sum_of_translation = 0
        self.log_sum_of_rotation = 0
        self.old_log_sum_of_translation = 0
        self.old_log_sum_of_rotation = 0
        #ex2
        self.theta0 = random.randint(0, 360)
        self.theta = self.theta0
        self.x = self.x_0
        self.y = self.y_0
        print ("[RESET] theta =",self.theta0)
        super().reset()

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        # cet exemple montre comment générer au hasard, et évaluer, des stratégies comportementales
        # Remarques:
        # - la liste "param", définie ci-dessus, permet de stocker les paramètres de la fonction de contrôle
        # - la fonction de controle est une combinaison linéaire des senseurs, pondérés par les paramètres (c'est un "Perceptron")

        # toutes les X itérations: le robot est remis à sa position initiale de l'arène avec une orientation aléatoire
        
        delta_translation = self.log_sum_of_translation - self.old_log_sum_of_translation
        delta_rotation = abs(self.log_sum_of_rotation - self.old_log_sum_of_rotation)

        self.score += delta_translation * (1 - delta_rotation)

        self.old_log_sum_of_translation = self.log_sum_of_translation
        self.old_log_sum_of_rotation = self.log_sum_of_rotation
    
        if self.iteration % self.it_per_evaluation == 0:
                
                #ex2
                self.cumulated_score += self.score # Somme des scores
                self.sub_evaluation += 1 # Nombre de répétitions
                print ("score = " + str(self.score))
                print ("tour " + str(self.sub_evaluation) + ": cumulated_score = " + str(self.cumulated_score))

                if self.sub_evaluation < self.nb_repeats and self.trial < 500:
                    #
                    pass

                else:
                    
                    #ex2
                    self.final_score = self.cumulated_score

                    if self.trial < 500:
                        print ("\tparameters           =",self.param)
                        print ("\ttranslations         =",self.log_sum_of_translation,"; rotations =",self.log_sum_of_rotation) # *effective* translation/rotation (ie. measured from displacement)
                        print ("\tdistance from origin =",math.sqrt((self.x-self.x_0)**2+(self.y-self.y_0)**2))
                        #ex1
                        print ("\tscore                =",self.final_score)
                        if self.final_score > self.bestScore:
                            self.bestScore = self.final_score
                            self.bestParam = self.param[:] 
                            self.bestTrial = self.trial   
                            print ("\t>>> New best score! (Trial "+str(self.trial)+") <<<")

                        self.trial = self.trial + 1
                        
                        self.param = [random.randint(-1, 1) for i in range(8)] 
                        print ("Starting trial no.", self.trial + 1)
                        #ex2
                        self.sub_evaluation = 0 
                        self.cumulated_score = 0
                        self.final_score = 0
                    
                    else:
                        #si plus que 500 essais, on rejoue la meilleure stratégie
                        print ("\n" )
                        print ("xxx REPLAY BEST STRATEGY (found at trial", self.bestTrial, ") xxx")
                        print ("xxx Best Score was:", self.bestScore)
                        print ("xxx Best Params:", self.bestParam)
                    
                        self.param = self.bestParam[:] # On remet les paramètres du champion
                        self.it_per_evaluation = 1000  # On passe à 1000 itérations comme demandé

                        #ex2
                        self.sub_evaluation = 0 
                        self.cumulated_score = 0
                        self.final_score = 0
                
                self.score = 0
                self.iteration = self.iteration + 1
                return 0, 0, True 

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