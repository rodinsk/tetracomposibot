import matplotlib.pyplot as plt
import resultat_test

def read_data(filename):
    iterations = []
    best_scores = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.split(',')
            if len(parts) == 3:
                iterations.append(int(parts[0]))
                best_scores.append(float(parts[2])) 
    return iterations, best_scores


iter_rand, score_rand = read_data("resultat_test/resultat_random_1.txt") 
iter_gen, score_gen = read_data("resultat_test/resultat_algo_1.txt")

plt.plot(iter_rand, score_rand, label="Recherche Aléatoire", color="blue")
plt.plot(iter_gen, score_gen, label="Algorithme Génétique", color="red")


plt.title("Comparaison : Hasard vs Génétique")
plt.xlabel("Nombre d'évaluations")
plt.ylabel("Meilleur Score Trouvé")
plt.legend()
plt.grid()
plt.show()