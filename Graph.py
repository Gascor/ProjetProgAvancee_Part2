import pandas as pd
import matplotlib.pyplot as plt

# Charger les données à partir d'un fichier CSV
data_file = "assigment102.csv"  # Remplace par le chemin de ton fichier CSV
df = pd.read_csv(data_file, delimiter=';', skipinitialspace=True)

# Remplacer les virgules par des points et convertir les colonnes en numériques
df["PI"] = df["PI"].str.replace(',', '.').astype(float)
df["Difference"] = df["Difference"].str.replace(',', '.').astype(float)
df["Error"] = df["Error"].str.replace(',', '.').astype(float)
df["Ntot"] = df["Ntot"].str.replace(',', '.').astype(float)
df["AvailableProcessors"] = df["AvailableProcessors"].str.replace(',', '.').astype(float)
df["TimeDuration(ms)"] = df["TimeDuration(ms)"].str.replace(',', '.').astype(float)

# Calculer le ratio Ntot / AvailableProcessors
df["Ratio"] = df["Ntot"] / df["AvailableProcessors"]

# Vérifier les valeurs uniques de ce ratio
unique_ratios = sorted(df["Ratio"].unique())

# Créer un graphique combiné
plt.figure(figsize=(12, 8))

# Définir une tolérance pour comparer AvailableProcessors à 1
tolerance = 1e-6

for ratio in unique_ratios:
    subset = df[df["Ratio"] == ratio]

    # Trouver les données pour 1 processeur (si elles existent)
    subset_1_processor = subset[abs(subset["AvailableProcessors"] - 1) < tolerance]

    # Vérifier si des données existent pour 1 processeur
    if not subset_1_processor.empty:
        time_on_1_processor = subset_1_processor["TimeDuration(ms)"].values[0]
    else:
        print(f"Aucune donnée pour AvailableProcessors=1 avec Ratio={ratio}")
        continue  # Passer au ratio suivant si aucune donnée n'est disponible

    # Calcul du Speed-up
    subset = subset.copy()
    subset["Speed-up"] = time_on_1_processor / subset["TimeDuration(ms)"]

    # Tracer les points de Speed-up
    plt.plot(
        subset["AvailableProcessors"],
        subset["Speed-up"],
        marker="o",
        label=f" Speedup de Ntot/Processors = {ratio:.1e}"
    )

# Ajouter la courbe idéale (Speed-up constant = 1)
ideal_processors = sorted(df["AvailableProcessors"].unique())
ideal_speedup = [1] * len(ideal_processors)  # Scalabilité faible idéale : Speed-up = nb processeurs
plt.plot(
    ideal_processors,
    ideal_speedup,
    linestyle="--",
    color="red",
    label="Speed-up idéal (constant)"
)

# Configurer le graphique
plt.title("Graphe de Scalabilité Faible (Speed-up)", fontsize=16)
plt.xlabel("Nombre de processeurs", fontsize=14)
plt.ylabel("Speed-up", fontsize=14)
plt.xscale("log", base=2)
plt.yscale("log", base=2)
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

# Ajouter la légende
plt.legend(fontsize=12)

# Sauvegarder et afficher le graphique
combined_output_file = "scalabilite_faible_ratio_based.png"
plt.savefig(combined_output_file, dpi=300)
plt.show()