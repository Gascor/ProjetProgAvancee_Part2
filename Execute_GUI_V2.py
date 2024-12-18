import subprocess
from datetime import datetime
import tkinter as tk

def run_java_program(points, threads, output_file_base, java_class):
    """
    Exécute un programme Java pour le calcul avec les paramètres spécifiés et écrit les résultats dans un fichier CSV.
    """
    date = datetime.now().strftime("%Y%m%d")
    output_file = f"{output_file_base}_{date}.csv"
    command = f"java .\src\{java_class}.java {points} {threads} {output_file}"
    try:
        process = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(process.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande Java: {e}")

def gui():
    """
    Construit et affiche l'interface graphique pour la configuration des calculs.
    """
    window = tk.Tk()
    window.title("Configuration des Calculs")

    # Définition des variables
    points_strong = tk.StringVar(value='1600000,16000000,160000000')
    points_weak = tk.StringVar(value='100000,1000000,10000000')
    thread_counts = tk.StringVar(value='1,2,4,8,16,32')
    repeat_count = tk.IntVar(value=5)
    pi_strong_enabled = tk.BooleanVar(value=True)
    assignment_strong_enabled = tk.BooleanVar(value=True)
    pi_weak_enabled = tk.BooleanVar(value=True)
    assignment_weak_enabled = tk.BooleanVar(value=True)

    def start_calculations():
        """
        Démarre les calculs en fonction des paramètres de l'interface utilisateur.
        """
        points_list_strong = [int(p) for p in points_strong.get().split(',')]
        points_list_weak = [int(p) for p in points_weak.get().split(',')]
        threads = [int(t) for t in thread_counts.get().split(',')]
        repeats = repeat_count.get()

        for points in points_list_strong:
            for thread in threads:
                for _ in range(repeats):
                    if pi_strong_enabled.get():
                        run_java_program(points // thread, thread, "results_pi_strong", "Pi")
                    if assignment_strong_enabled.get():
                        run_java_program(points // thread, thread, "results_assignment_strong", "Assignment102")

        for points in points_list_weak:
            for thread in threads:
                for _ in range(repeats):
                    if pi_weak_enabled.get():
                        run_java_program(points, thread, "results_pi_weak", "Pi")
                    if assignment_weak_enabled.get():
                        run_java_program(points, thread, "results_assignment_weak", "Assignment102")

        print("Calculs terminés.")

    # Configuration des widgets de l'interface
    tk.Label(window, text="Points pour scalabilité forte:").pack()
    tk.Entry(window, textvariable=points_strong).pack()

    tk.Label(window, text="Points pour scalabilité faible:").pack()
    tk.Entry(window, textvariable=points_weak).pack()

    tk.Label(window, text="Nombre de threads:").pack()
    tk.Entry(window, textvariable=thread_counts).pack()

    tk.Label(window, text="Nombre de répétitions:").pack()
    tk.Entry(window, textvariable=repeat_count).pack()

    tk.Checkbutton(window, text="Activer Pi pour scalabilité forte", variable=pi_strong_enabled).pack()
    tk.Checkbutton(window, text="Activer Assignment102 pour scalabilité forte", variable=assignment_strong_enabled).pack()
    tk.Checkbutton(window, text="Activer Pi pour scalabilité faible", variable=pi_weak_enabled).pack()
    tk.Checkbutton(window, text="Activer Assignment102 pour scalabilité faible", variable=assignment_weak_enabled).pack()

    tk.Button(window, text="Démarrer les calculs", command=start_calculations).pack()
    window.mainloop()

if __name__ == "__main__":
    gui()
