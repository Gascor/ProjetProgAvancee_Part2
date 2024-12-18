import pandas as pd
import subprocess
import sys

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Essayer d'importer tabulate, l'installer si non présent
try:
    from tabulate import tabulate
except ImportError:
    print("Le module 'tabulate' n'est pas installé. Il va être installé.")
    install_package('tabulate')
    from tabulate import tabulate  # Réessayer l'importation après l'installation
# Charger les données à partir d'un fichier CSV
file_path = 'Data/results_pi_strong_MSIVECTOR.csv'  # Remplacez par le chemin de votre fichier
data = pd.read_csv(file_path, delimiter=';')

# Fonction pour convertir les données en Markdown
def to_markdown(df, title):
    print(f"### {title}")
    print(df.to_markdown(index=True) + "\n")

# Calcul des moyennes par groupe de threads
mean_by_processors = data.groupby('AvailableProcessors').mean()
to_markdown(mean_by_processors, "Moyennes par nombre de threads (Tous les Ntot)")

# Calcul des moyennes par groupe de threads pour chaque Ntot unique
for ntot in data['Ntot'].unique():
    filtered_data = data[data['Ntot'] == ntot]
    mean_by_processors_ntot = filtered_data.groupby('AvailableProcessors').mean()
    to_markdown(mean_by_processors_ntot, f"Moyennes par nombre de threads pour Ntot = {ntot}")

# Calcul des moyennes pour chaque Ntot
mean_by_ntot = data.groupby('Ntot').mean()
to_markdown(mean_by_ntot, "Moyennes globales pour chaque Ntot")

# Calcul des moyennes par AvailableProcessors pour chaque Ntot unique
for ntot in data['Ntot'].unique():
    filtered_data = data[data['Ntot'] == ntot]
    mean_by_ntot_specific = filtered_data.mean().to_frame().T
    to_markdown(mean_by_ntot_specific, f"Moyennes pour Ntot = {ntot}")
