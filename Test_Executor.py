import pandas as pd
import matplotlib.pyplot as plt

# Charger les données à partir d'un fichier CSV
data_file = "Data/results_assignment_strong_G24.csv"  # Utilisez le chemin complet ici
df = pd.read_csv(data_file, delimiter=';', decimal='.', skipinitialspace=True, header=0)

# Vérifier les premières lignes pour examiner les données
print("Premières lignes du fichier :")
print(df.head())

# Vérifier les types de données après la lecture
print("Types de colonnes après lecture :")
print(df.dtypes)

# Vérifier les valeurs uniques de AvailableProcessors
print("Valeurs uniques de AvailableProcessors :")
print(df["AvailableProcessors"].unique())

# Créer un graphique combiné
plt.figure(figsize=(10, 6))

# Groupement par nombre de processeurs
grouped = df.groupby('AvailableProcessors')

# Tracer la moyenne du Speed-up pour chaque nombre de processeurs
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
plt.plot(processor_counts, processor_counts, linestyle="--", color="red", label="Speed-up idéal")


# Ajuster les limites des axes
plt.xlim(0.8, max(processor_counts) * 2)  # Élargissement de l'axe des X
plt.ylim(min(speedup_means) * 0.8, 80)  # Augmenter la limite supérieure pour mieux centrer la ligne rouge


# Configurer le graphique combiné
plt.title("""Moyenne du Graphique de Scalabilité Forte (Speed-up) | Calculs sur Assignment102.java
(Sur Ordinateur Salle G24 cf: Rapport section Architecture materielles)""")
plt.xlabel("Nombre de processeurs")
plt.ylabel("Moyenne du Speed-up")
plt.xscale("log", base=2)
plt.yscale("log", base=2)
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.legend()

# Sauvegarder le graphique
combined_output_file = "doc/Docs/pi_scalabilite_forte_moyenne_speedup.png"  # Utilisez le chemin complet ici
plt.savefig(combined_output_file, dpi=300)

# Afficher le graphique (facultatif en mode batch)
# plt.show()
