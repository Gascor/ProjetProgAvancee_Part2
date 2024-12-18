import pandas as pd
import matplotlib.pyplot as plt

# Charger les données à partir d'un fichier CSV
data_file = "Data.csv"  # Remplacez par le chemin complet
df = pd.read_csv(data_file, delimiter=';', decimal='.', skipinitialspace=True, header=0)

# Créer un graphique combiné
plt.figure(figsize=(12, 7))

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

# Ajuster les limites des axes
plt.xlim(0.8, max(processor_counts) * 2)  # Élargissement de l'axe des X
plt.ylim(min(speedup_means) * -4.5, 4.5)  # Augmenter la limite supérieure pour mieux centrer la ligne rouge

plt.title("Moyenne du Graphique de Scalabilité Forte (Speed-up)")
plt.xlabel("Nombre de processeurs")
plt.ylabel("Moyenne du Speed-up")
plt.xscale("log", base=2)
plt.yscale("linear")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.legend()

# Sauvegarder et afficher le graphique
plt.savefig("doc/Docs/pi_scalabilite_forte_moyenne_speedup.png", dpi=300)
plt.show()
