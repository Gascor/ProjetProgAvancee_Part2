import pandas as pd
import matplotlib.pyplot as plt

# Charger les données à partir d'un fichier CSV
data_file = "Data/results_mw-dist_weak_G24.csv"  # Remplacez par le chemin complet
df = pd.read_csv(data_file, delimiter=';', decimal='.', skipinitialspace=True, header=0)

# Créer un graphique combiné
plt.figure(figsize=(12, 7))  # Ajustez la taille du graphique si nécessaire

# Groupement par nombre de processeurs et calcul du speed-up moyen
grouped = df.groupby('AvailableProcessors')
speedup_means = []
processor_counts = []

for name, group in grouped:
    subset_1_processor = df[df['AvailableProcessors'] == 1]
    if not subset_1_processor.empty:
        time_on_1_processor = subset_1_processor["TimeDuration(ms)"].mean()
        average_time = group["TimeDuration(ms)"].mean()
        speedup = time_on_1_processor / average_time
        speedup_means.append(speedup)
        processor_counts.append(name)

plt.plot(processor_counts, speedup_means, marker="o", linestyle='-', label="Moyenne du Speed-up")
plt.axhline(y=1, color="red", linestyle="--", label="Speed-up idéal")

# Ajuster les limites des axes pour mieux "dézoomer"
plt.xlim(0.5, max(processor_counts) * 1.5)  # Assurez-vous que 'max(processor_counts)' est votre valeur maximale
plt.ylim(min(speedup_means) * 0.8, 1.1)  # Ajuste ymin pour être un peu en dessous du minimum de vos speed-up

plt.title("""Moyenne du Graphique de Scalabilité Faible (Speed-up) | Calculs Master Worker Distribué
(Sur Ordinateur Salle G24 cf: Rapport section Architecture materielles)""")
plt.xlabel("Nombre de processeurs")
plt.ylabel("Moyenne du Speed-up")
plt.xscale("log", base=2)
plt.yscale("linear")  # Utilisez 'linear' si cela fonctionne mieux pour vos données
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.legend()

# Sauvegarder et afficher le graphique
plt.savefig("doc/Docs/graph/mw-dist_weak_mean_speedup_G24.png", dpi=300)