
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
    max_strategies = 500;

    old_log_sum_of_translation = 0
    old_log_sum_of_rotation = 0
    score = 0
    total_score = 0

    bestScore = -100000 ; # ex1
    orientations = []

    subTrial = 0

    parentParam = []
    parentScore = -100000

    is_first_generation = True

    generation = 0
    max_generation = 500

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a",evaluations=0,it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        self.x_0 = x_0
        self.y_0 = y_0
        self.orientations = [0,120,240]
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
                
 
                self.total_score += self.score
                self.subTrial += 1
                

                #CAS1 S'il y a d'autres orientations à tester 
                if self.subTrial < len(self.orientations):
                    self.theta_0 = self.orientations[self.subTrial]

                    self.score = 0
                    self.old_log_sum_of_rotation = 0
                    self.old_log_sum_of_translation = 0
                    self.iteration =0
                    return 0, 0, True
                else :

                    #Premier parent
                    if self.is_first_generation:
                        # Premier essai, on initialise le parent
                        self.parentParam = self.param[:]
                        self.parentScore = self.total_score
                        self.is_first_generation = False
                    else:
                        # Comparaison avec parent
                        if self.total_score > self.parentScore:
                            # Nouveau parent
                            self.parentParam = self.param[:]
                            self.parentScore = self.total_score
                    
                    print(f"{self.generation},{self.total_score:.2f},{self.parentScore:.2f}")

                    if self.generation < self.max_generation:
                        #Prochaine génération
                        self.param = self.parentParam[:]  
                        ind = random.randint(0,7)
                        values = [-1,0,1]
                        values.remove(self.param[ind]) 
                        # Forcement du changement
                        self.param[ind] = random.choice(values)
                        self.generation += 1

    
                    else:
                        
                        #Avec le meilleur individu
                        self.param = self.parentParam[:]
                        self.it_per_evaluation = 1000  # On passe à 1000 itérations
                    
                    #Reset
                    self.subTrial = 0
                    self.theta_0 = self.orientations[0]
                    self.total_score = 0
                    self.score = 0
                    self.old_log_sum_of_rotation = 0
                    self.old_log_sum_of_translation = 0
                    self.iteration =0
                    return 0, 0, True

        # fonction de contrôle (qui dépend des entrées sensorielles, et des paramètres)
        translation = math.tanh ( self.param[0] + self.param[1] * sensors[sensor_front_left] + self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right] )
        rotation = math.tanh ( self.param[4] + self.param[5] * sensors[sensor_front_left] + self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right] )

        self.iteration = self.iteration + 1
        return translation, rotation, False #Reset
        
                
        

      