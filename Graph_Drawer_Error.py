import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Définir les chemins des fichiers et les labels associés
files = [
    "Data/results_assignment_weak_MSIVECTOR.csv",
    "Data/results_pi_weak_MSIVECTOR.csv",
    "Data/results_mw-local_weak_MSIVECTOR.csv",
]
labels = ['Assignment', 'Pi Calculation', 'Master Worker Partagé']

# Préparer la figure
plt.figure(figsize=(12, 8))

colors = ['blue', 'green', 'red']  # Couleurs pour distinguer les différents algorithmes

# Boucle pour traiter chaque fichier
for file, label, color in zip(files, labels, colors):
    df = pd.read_csv(file, delimiter=';', decimal='.', skipinitialspace=True, header=0)
    grouped = df.groupby('Ntot')
    
    # Calcul de la médiane et de la moyenne
    median_errors = grouped['Error'].median().reset_index()
    mean_errors = grouped['Error'].mean().reset_index()
    
    # Tracer la médiane des erreurs
    plt.plot(median_errors['Ntot'], median_errors['Error'], 
             marker='o', linestyle='-', color=color, label=f'{label} - Médiane')
    
    # Tracer la moyenne des erreurs
    plt.plot(mean_errors['Ntot'], mean_errors['Error'], 
             marker='x', linestyle='-', color=color, label=f'{label} - Moyenne', alpha=0.5)

# Configurer le graphique
plt.title("Comparaison de l'Erreur entre Trois Algorithmes sur MSI VECTOR")
plt.xlabel("Nombre d'itérations (Ntot)")
plt.ylabel("Erreur")
plt.xscale('log')  # Échelle logarithmique pour Ntot
plt.yscale('log')  # Échelle logarithmique pour l'Erreur
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.legend()

# Sauvegarder le graphique
output_file = "doc/Docs/graph/comparison_median_mean_error_by_algorithm.png"
plt.savefig(output_file, dpi=300)

# Afficher le graphique
plt.show()
