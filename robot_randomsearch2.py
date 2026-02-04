
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

    

    x_0 = 0
    y_0 = 0
    theta_0 = 0 # in [0,360]

    # Nouvelles variables
    max_strategies = 500

    old_log_sum_of_translation = 0
    old_log_sum_of_rotation = 0
    score = 0
    total_score = 0

    bestScore = -100000 ; # ex1
    orientations = []

    subTrial = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a",evaluations=0,it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        self.x_0 = x_0
        self.y_0 = y_0
        self.orientations = [0, 90, 360]
        self.theta_0 = self.orientations[0];
        self.param = [random.randint(-1, 1) for i in range(8)]
        self.it_per_evaluation = it_per_evaluation
        self.old_log_sum_of_translation = 0
        self.old_log_sum_of_rotation = 0
        self.score = 0
        self.total_score = 0

        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
     
        super().reset()

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        #Calcul score
       
        
    
        effective_translation = self.log_sum_of_translation - self.old_log_sum_of_translation
        effective_rotation = self.log_sum_of_rotation - self.old_log_sum_of_rotation

        self.score += effective_translation * (1 - abs(effective_rotation))

        self.old_log_sum_of_translation = self.log_sum_of_translation
        self.old_log_sum_of_rotation = self.log_sum_of_rotation


        #Fin évaluation 
        if self.iteration % self.it_per_evaluation == 0 and self.iteration > 0:
                print ("Starting sub trial  / ", (self.subTrial) % len(self.orientations) + 1, " with orientation ", self.theta_0)
                print ("\tparameters           =",self.param)
                print ("\ttranslations         =",self.log_sum_of_translation,"; rotations =",self.log_sum_of_rotation) # *effective* translation/rotation (ie. measured from displacement)
                print ("\tdistance from origin =",math.sqrt((self.x-self.x_0)**2+(self.y-self.y_0)**2))
                print ("\tscore                =",self.score)

                
                
                self.total_score += self.score

                self.subTrial += 1
                

                #CAS1 On va tester d'autres conditions
                if self.subTrial < len(self.orientations):
                    self.theta_0 = self.orientations[self.subTrial]
                else :
                    print("Total score for trial ", self.trial, " : ", self.total_score)
                    # CAS 2 Fin stratégie
                    if self.total_score > self.bestScore:
                        self.bestScore = self.total_score
                        self.bestParam = self.param[:] 
                        self.bestTrial = self.trial  
                        print ("\t>>> New best score! : ", self.total_score, " <<<")

                    #Vérification prochaine essai ou replay
                    if self.trial < self.max_strategies:
                        # CAS 1 
                        self.param = [random.randint(-1, 1) for i in range(8)]
                        
                        self.trial = self.trial + 1
                    else:
                        # CAS 2 
                        print ("||| Playing best trial : ", self.bestTrial, ") |||")
                        print ("Best score :", self.bestScore)
                        print ("Best parameters:", self.bestParam)
                        
                        self.param = self.bestParam[:] # On remet les paramètres du champion sans copie de tableau
                        self.it_per_evaluation = 1000  # On passe à 1000 itérations 

                    self.subTrial = 0
                    self.theta_0 = self.orientations[0]
                    self.total_score = 0
                
                self.score = 0
                self.iteration = 0
                self.old_log_sum_of_translation = 0
                self.old_log_sum_of_rotation = 0

                return 0, 0, True #Reset

        # fonction de contrôle (qui dépend des entrées sensorielles, et des paramètres)
        translation = math.tanh ( self.param[0] + self.param[1] * sensors[sensor_front_left] + self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right] )
        rotation = math.tanh ( self.param[4] + self.param[5] * sensors[sensor_front_left] + self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right] )

        self.iteration = self.iteration + 1
        return translation, rotation, False #Reset
        
                
        

      