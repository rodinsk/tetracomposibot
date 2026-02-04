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


iter_rand1, score_rand1= read_data("resultat_test/resultat_random_1.txt")
iter_rand2, score_rand2 = read_data("resultat_test/resultat_random_2.txt")
iter_rand3, score_rand3 = read_data("resultat_test/resultat_random_3.txt")
iter_rand4, score_rand4 = read_data("resultat_test/resultat_random_4.txt")
iter_rand5, score_rand5 = read_data("resultat_test/resultat_random_5.txt")
iter_gen, score_gen = read_data("resultat_test/resultat_algo_1.txt")
iter_gen2, score_gen2 = read_data("resultat_test/resultat_algo_2.txt")
iter_gen3, score_gen3 = read_data("resultat_test/resultat_algo_3.txt")
iter_gen4, score_gen4 = read_data("resultat_test/resultat_algo_4.txt")
iter_gen5, score_gen5 = read_data("resultat_test/resultat_algo_5.txt")

plt.plot(iter_rand1, score_rand1, label="Recherche Aléatoire ", color="orange")
plt.plot(iter_rand2, score_rand2, color="orange")
plt.plot(iter_rand3, score_rand3, color="orange")
plt.plot(iter_rand4, score_rand4, color="orange")
plt.plot(iter_rand5, score_rand5, color="orange")

plt.plot(iter_gen, score_gen, label="Algorithme Génétique ", color="purple")
plt.plot(iter_gen2, score_gen2, color="purple")
plt.plot(iter_gen3, score_gen3, color="purple")
plt.plot(iter_gen4, score_gen4, color="purple")
plt.plot(iter_gen5, score_gen5, color="purple")



plt.title("Comparaison : Hasard vs Génétique")
plt.xlabel("Nombre d'évaluations")
plt.ylabel("Meilleur Score Trouvé")
plt.legend()
plt.grid()
plt.show()