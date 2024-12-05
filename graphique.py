import pandas as pd
import matplotlib.pyplot as plt

# Charger le fichier CSV
file_path = "results.csv"  # Remplacez par le chemin de votre fichier CSV
data = pd.read_csv(file_path, delimiter=';')

# Convertir les colonnes nécessaires en numérique (remplacer les virgules par des points)
data["Estimated Pi"] = data["Estimated Pi"].str.replace(',', '.').astype(float)
data["Error"] = data["Error"].str.replace(',', '.').astype(float)
data["Execution Time (ms)"] = data["Execution Time (ms)"].astype(float)
data["Total Throws"] = data["Total Throws"].astype(float)

# Vérifier les données
print(data.head())

# Regrouper les données par "Number of Workers"
grouped = data.groupby("Number of Workers").mean()

# SCALABILITÉ FORTE : Temps d'exécution pour une charge fixe
# Filtrer les cas où la charge (Total Throws) reste constante
fixed_load = grouped[grouped["Total Throws"] == grouped["Total Throws"].iloc[0]]

plt.figure(figsize=(10, 6))
plt.plot(fixed_load.index, fixed_load["Execution Time (ms)"], marker='o')
plt.title("Scalabilité Forte (Charge Fixe)")
plt.xlabel("Nombre de Workers")
plt.ylabel("Temps d'exécution (ms)")
plt.grid(True)
plt.savefig("scalabilite_forte.jpg", format='jpg')  # Sauvegarde en JPG
plt.show()

# SCALABILITÉ FAIBLE : Temps d'exécution pour une charge proportionnelle
# Filtrer les cas où la charge est proportionnelle au nombre de workers
proportional_load = grouped[grouped["Total Throws"] / grouped.index == grouped["Total Throws"].iloc[0] / grouped.index[0]]

plt.figure(figsize=(10, 6))
plt.plot(proportional_load.index, proportional_load["Execution Time (ms)"], marker='o')
plt.title("Scalabilité Faible (Charge Proportionnelle)")
plt.xlabel("Nombre de Workers")
plt.ylabel("Temps d'exécution (ms)")
plt.grid(True)
plt.savefig("scalabilite_faible.jpg", format='jpg')  # Sauvegarde en JPG
plt.show()
