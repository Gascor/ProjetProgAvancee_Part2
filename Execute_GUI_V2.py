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
    masterworker_enabled = tk.BooleanVar(value=False)
    masterworker_points = tk.StringVar(value='1600000')
    masterworker_workers = tk.IntVar(value=4)

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
                    run_java_program(points // thread, thread, "results_pi_strong", "Pi")
                    run_java_program(points // thread, thread, "results_assignment_strong", "Assignment102")

        for points in points_list_weak:
            for thread in threads:
                for _ in range(repeats):
                    run_java_program(points, thread, "results_pi_weak", "Pi")
                    run_java_program(points, thread, "results_assignment_weak", "Assignment102")

        if masterworker_enabled.get():
            total_points = int(masterworker_points.get())
            workers = masterworker_workers.get()
            for _ in range(repeats):
                run_java_program(total_points, workers, "results_masterworker_strong", "MasterWorker")
                run_java_program(total_points * workers, workers, "results_masterworker_weak", "MasterWorker")

        print("Calculs terminés.")

    def toggle_masterworker():
        """
        Active ou désactive les entrées pour le test MasterWorker en fonction de l'état du bouton à cocher.
        """
        state = 'normal' if masterworker_enabled.get() else 'disabled'
        points_masterworker_entry.config(state=state)
        workers_masterworker_entry.config(state=state)

    # Configuration des widgets de l'interface
    tk.Label(window, text="Points pour scalabilité forte:").pack()
    tk.Entry(window, textvariable=points_strong).pack()

    tk.Label(window, text="Points pour scalabilité faible:").pack()
    tk.Entry(window, textvariable=points_weak).pack()

    tk.Label(window, text="Nombre de threads:").pack()
    tk.Entry(window, textvariable=thread_counts).pack()

    tk.Label(window, text="Nombre de répétitions:").pack()
    tk.Entry(window, textvariable=repeat_count).pack()

    masterworker_checkbox = tk.Checkbutton(window, text="Activer le test MasterWorker", variable=masterworker_enabled, command=toggle_masterworker)
    masterworker_checkbox.pack()

    tk.Label(window, text="Nombre de points pour MasterWorker:").pack()
    points_masterworker_entry = tk.Entry(window, textvariable=masterworker_points, state='disabled')
    points_masterworker_entry.pack()

    tk.Label(window, text="Nombre de workers pour MasterWorker:").pack()
    workers_masterworker_entry = tk.Entry(window, textvariable=masterworker_workers, state='disabled')
    workers_masterworker_entry.pack()

    tk.Button(window, text="Démarrer les calculs", command=start_calculations).pack()
    window.mainloop()

if __name__ == "__main__":
    gui()
