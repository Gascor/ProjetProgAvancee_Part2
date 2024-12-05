import os
import subprocess
import csv
from math import ceil

# Configuration des tests
points_totaux = [1600000, 16000000, 160000000]  # Points totaux à tester
workers = [1, 2, 4, 8, 16, 20, 24, 32]  # Nombre de workers
output_csv = "scalabilite_forte_results.csv"  # Fichier CSV de sortie

# Commande Java (adapter si nécessaire)
java_command = "java -cp bin src.Assignment102"

# Préparer le fichier CSV de sortie
with open(output_csv, mode="w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Total Points", "Workers", "Estimated Pi", "Error", "Relative Error", "Execution Time (ms)"])

# Exécuter les tests
for points in points_totaux:
    for num_workers in workers:
        for i in range(10):  # Boucle pour répéter 10 fois chaque test
            points_per_worker = ceil(points / num_workers)
            command = f"{java_command} {points_per_worker} {num_workers} temp_results.csv"

            print(f"Exécution : {command}")
            try:

                # Lancer le programme Java
                result = subprocess.run(command, shell=True, capture_output=True, text=True)

                # Afficher les sorties pour debug
                print("Sortie standard :")
                print(result.stdout)
                print("Erreur standard :")
                print(result.stderr)

                # Vérifiez si le fichier temporaire existe
                if not os.path.exists("temp_results.csv"):
                    print(f"Fichier temporaire 'temp_results.csv' introuvable après exécution de : {command}")
                    continue

                # Lire les résultats dans le fichier temporaire
                with open("temp_results.csv", mode="r") as temp_csv:
                    temp_reader = csv.reader(temp_csv)
                    for row in temp_reader:
                        if len(row) == 6:  # Vérifie que c'est une ligne de données
                            with open(output_csv, mode="a", newline="") as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow([points, num_workers] + row[1:])

            except Exception as e:
                print(f"Erreur inattendue : {e}")

print(f"Tests terminés. Résultats sauvegardés dans {output_csv}.")
