import subprocess
import sys
from datetime import datetime
import tkinter as tk

# Fonction pour exécuter les programmes Java et écrire les résultats dans un fichier CSV unique
def run_java_program(points, threads, output_file_base, java_class):
    # Format du nom de fichier avec la date du jour pour éviter la surcharge des données
    date = datetime.now().strftime("%Y%m%d")
    output_file = f"{output_file_base}_{date}.csv"
    command = f"java .\src\{java_class}.java {points} {threads} {output_file}"
    try:
        # Exécute la commande Java
        process = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(process.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande Java: {e}")

# Interface graphique avec Tkinter
def gui():
    window = tk.Tk()
    window.title("Configuration des Calculs")

    # Variables pour stocker les entrées utilisateur
    points_strong = tk.StringVar(value='1600000,16000000,160000000')
    points_weak = tk.StringVar(value='100000,1000000,10000000')
    thread_counts = tk.StringVar(value='1,2,4,8,16,32')
    repeat_count = tk.IntVar(value=5)

    # Fonction pour lancer les calculs
    def start_calculations():
        points_list_strong = [int(p) for p in points_strong.get().split(',')]
        points_list_weak = [int(p) for p in points_weak.get().split(',')]
        threads = [int(t) for t in thread_counts.get().split(',')]
        repeats = repeat_count.get()
        
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

    # Création des widgets
    tk.Label(window, text="Points pour scalabilité forte:").pack()
    tk.Entry(window, textvariable=points_strong).pack()
    
    tk.Label(window, text="Points pour scalabilité faible:").pack()
    tk.Entry(window, textvariable=points_weak).pack()

    tk.Label(window, text="Nombre de threads:").pack()
    tk.Entry(window, textvariable=thread_counts).pack()

    tk.Label(window, text="Nombre de répétitions:").pack()
    tk.Entry(window, textvariable=repeat_count).pack()

    tk.Button(window, text="Démarrer les calculs", command=start_calculations).pack()

    window.mainloop()

# Lancer l'interface graphique
if __name__ == "__main__":
    gui()
