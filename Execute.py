import subprocess
import sys
from datetime import datetime
import argparse

# Fonction pour exécuter les programmes Java et écrire les résultats dans un fichier CSV unique
def run_java_program(points, threads, output_file_base, java_class):
    date = datetime.now().strftime("%Y%m%d")
    output_file = f"{output_file_base}_{date}.csv"
    command = f"java .\src\{java_class}.java {points} {threads} {output_file}"
    try:
        process = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(process.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande Java: {e}")

def main():
    parser = argparse.ArgumentParser(description="Exécute des programmes Java pour des calculs de scalabilité.")
    parser.add_argument("--points_strong", type=str, default="1600000,16000000,160000000",
                        help="Points pour scalabilité forte, séparés par des virgules.")
    parser.add_argument("--points_weak", type=str, default="100000,1000000,10000000",
                        help="Points pour scalabilité faible, séparés par des virgules.")
    parser.add_argument("--thread_counts", type=str, default="1,2,4,8,16,32",
                        help="Nombre de threads, séparés par des virgules.")
    parser.add_argument("--repeat_count", type=int, default=5,
                        help="Nombre de répétitions pour chaque configuration.")

    args = parser.parse_args()

    points_list_strong = [int(p) for p in args.points_strong.split(',')]
    points_list_weak = [int(p) for p in args.points_weak.split(',')]
    threads = [int(t) for t in args.thread_counts.split(',')]
    repeats = args.repeat_count

    for points in points_list_strong:
        for thread in threads:
            for _ in range(repeats):
                points_per_thread = int(points / thread)
                run_java_program(points_per_thread, thread, "results_pi_strong", "Pi")

    for points in points_list_strong:
        for thread in threads:
            for _ in range(repeats):
                points_per_thread = int(points / thread)
                run_java_program(points_per_thread, thread, "results_assignment_strong", "Assignment102")

    for points in points_list_weak:
        for thread in threads:
            for _ in range(repeats):
                run_java_program(points, thread, "results_pi_weak", "Pi")

    for points in points_list_weak:
        for thread in threads:
            for _ in range(repeats):
                run_java_program(points, thread, "results_assignment_weak", "Assignment102")

    print("Calculs terminés.")

if __name__ == "__main__":
    main()
