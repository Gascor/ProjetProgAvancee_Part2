import os
import subprocess
import csv
from math import ceil
import time
from datetime import datetime

# Configuration des tests
points_totaux = [1600000, 16000000, 160000000]  # Points totaux à tester
workers = [1, 2, 4, 8, 16, 32, 64, 128]  # Nombre de workers
Script_visee = "Assignment102"
output_csv = f"temp_results_{Script_visee}.csv"  # Fichier CSV de sortie

# Commande Java (adapter si nécessaire)
java_command = f"java -cp bin src.{Script_visee}"

# Préparer le fichier CSV de sortie
with open(output_csv, mode="w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=";")  # Utiliser ; comme séparateur
    writer.writerow(["PI", "Difference", "Error", "Ntot", "AvailableProcessors", "TimeDuration(ms)"])

# Fonction pour extraire les résultats depuis la sortie Java
def parse_java_output(output, points, workers):
    try:
        # Séparer la sortie en lignes
        lines = output.splitlines()
        # Vérifiez le nombre de lignes attendu pour éviter les erreurs
        if len(lines) < 6:
            raise ValueError(f"Sortie inattendue : pas assez de lignes.\nSortie complète :\n{output}")

        # Extraire les valeurs nécessaires avec une validation
        pi_line = lines[0]
        diff_line = lines[1]
        error_line = lines[2]
        ntot_line = f"Ntot: {points * workers}"
        available_processors = f"Available processors: {workers}"
        time_line = lines[5]

        if "Pi:" not in pi_line or "Difference" not in diff_line or "Error" not in error_line or "Time Duration" not in time_line:
            raise ValueError(f"Format inattendu dans la sortie Java.\nSortie complète :\n{output}")

        pi = float(pi_line.split(":")[1].strip())
        difference = float(diff_line.split(":")[1].strip())
        error = float(error_line.split(":")[1].strip())
        ntot = points * workers
        execution_time = int(time_line.split(":")[1].strip())

        return pi, difference, error, ntot, workers, execution_time

    except Exception as e:
        # Afficher une erreur claire et détaillée si l'analyse échoue
        print(f"Erreur lors de l'analyse de la sortie Java : {e}")
        print(f"Sortie complète :\n{output}")
        return None, None, None, None, None, None


# Exécuter les tests
for points in points_totaux:
    for num_workers in workers:
        for i in range(10):  # Boucle pour répéter 10 fois chaque test
            points_per_worker = ceil(points / num_workers)
            command = f"{java_command} {points_per_worker} {num_workers} {output_csv}"

            print(f"Exécution : {command}")
            try:
                # Lancer le programme Java avec un timeout
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=120)

                # Afficher les sorties pour debug
                print("Sortie standard :")
                print(result.stdout)
                print("Erreur standard :")
                print(result.stderr)

                # Analyser la sortie standard pour extraire les résultats
                pi, difference, error, ntot, available_processors, execution_time = parse_java_output(
                    result.stdout, points, num_workers
                )

                # Vérifiez si les données ont été extraites correctement
                if pi is not None:
                    with open(output_csv, mode="a", newline="") as csvfile:
                        writer = csv.writer(csvfile, delimiter=";")  # Utiliser ; comme séparateur
                        writer.writerow([pi, difference, error, ntot, available_processors, execution_time])

            except subprocess.TimeoutExpired:
                print(f"Le processus a dépassé le temps limite (timeout) pour la commande : {command}")
            except Exception as e:
                print(f"Erreur inattendue : {e}")

print(f"Tests terminés. Résultats sauvegardés dans {output_csv}.")
