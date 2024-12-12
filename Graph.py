import pandas as pd
import matplotlib.pyplot as plt

# Charger les données à partir d'un fichier CSV
data_file = "temp_results_Assignment102.csv"  # Remplace par le chemin de ton fichier CSV
df = pd.read_csv(data_file, delimiter=';', skipinitialspace=True)

# Vérifier les premières lignes pour examiner les données
print("Premières lignes du fichier :")
print(df.head())

# Identifier les colonnes de type 'object' pour appliquer les remplacements
columns_to_convert = ["PI", "Difference", "Error", "Ntot", "AvailableProcessors", "TimeDuration(ms)"]

for col in columns_to_convert:
    if df[col].dtype == 'object':  # Vérifie si la colonne est de type 'object'
        df[col] = df[col].str.replace(',', '.').astype(float)

# Vérifier les types après la conversion
print("Types de colonnes après conversion :")
print(df.dtypes)

# Vérifier les valeurs uniques de AvailableProcessors
print("Valeurs uniques de AvailableProcessors :")
print(df["AvailableProcessors"].unique())

# Filtrer les données pour chaque Ntot unique
unique_Ntot = df["Ntot"].unique()

# Créer un graphique combiné
plt.figure(figsize=(10, 6))

# Définir une tolérance pour la comparaison de la valeur de AvailableProcessors
tolerance = 1e-6

for ntot in unique_Ntot:
    subset = df[df["Ntot"] == ntot]

    # Comparer AvailableProcessors avec 1, en tenant compte de la tolérance
    subset_1_processor = subset[abs(subset["AvailableProcessors"] - 1) < tolerance]

    # Vérifier si des données existent pour 1 processeur
    if not subset_1_processor.empty:
        time_on_1_processor = subset_1_processor["TimeDuration(ms)"].values[0]
    else:
        print(f"Aucune donnée pour AvailableProcessors=1 avec Ntot={ntot}")
        continue  # Si aucune donnée n'est trouvée, on passe au suivant

    # Calcul du Speed-up
    subset = subset.copy()
    subset["Speed-up"] = time_on_1_processor / subset["TimeDuration(ms)"]

    # Graphe individuel
    plt.plot(subset["AvailableProcessors"], subset["Speed-up"], marker="o", label=f"Ntot={ntot:.0e}")

    # Ajouter la courbe idéale
    ideal_speedup = subset["AvailableProcessors"]  # Droite idéale
    plt.plot(subset["AvailableProcessors"], ideal_speedup, linestyle="--", color="red",
             label=f"Speed-up idéal (Ntot={ntot:.0e})")

# Configurer le graphique combiné
plt.title("Graphe de Scalabilité Forte (Speed-up)")
plt.xlabel("Nombre de processeurs")
plt.ylabel("Speed-up")
plt.xscale("log", base=2)
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.legend()

# Sauvegarder le graphique combiné
combined_output_file = "assignment102_scalabilite_forte_combined.png"
plt.savefig(combined_output_file, dpi=300)
plt.show()
