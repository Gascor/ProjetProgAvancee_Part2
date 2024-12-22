import pandas as pd
import matplotlib.pyplot as plt

# Charger les données à partir des fichiers CSV
cpu_data = pd.read_csv("Data/results_scala_gpu_vs_cpu_CPU.csv", delimiter=';')
gpu_data = pd.read_csv("Data/results_scala_gpu_vs_cpu_GPU.csv", delimiter=';')

# Extraire les colonnes Ntot et TimeDuration(ms)
cpu_times = cpu_data[['Ntot', 'TimeDuration(ms)']]
gpu_times = gpu_data[['Ntot', 'TimeDuration(ms)']]

# Grouper par Ntot et calculer la moyenne du temps pour chaque groupe
cpu_avg_times = cpu_times.groupby('Ntot')['TimeDuration(ms)'].mean()
gpu_avg_times = gpu_times.groupby('Ntot')['TimeDuration(ms)'].mean()

# Création du graphique
plt.figure(figsize=(10, 6))
plt.plot(cpu_avg_times, label='CPU', marker='o')
plt.plot(gpu_avg_times, label='GPU', marker='x')
plt.xlabel('Nombre d\'itérations (Ntot) en milliards')
plt.ylabel('Temps moyen d\'exécution (ms)')
plt.title('Comparaison du temps d\'exécution CPU vs GPU (I9 14900HX 32 Coeurs vs RTX 4090 9742 Coeurs Cuda)')
plt.legend()
plt.grid(True)
plt.yscale('log')  # Échelle logarithmique pour mieux voir les différences
plt.xticks(rotation=45)
plt.tight_layout()

# Sauvegarde du graphique (optionnel)
plt.savefig('doc/Docs/graph/comparison_plot_time_cpu_gpu.png')

# Afficher le graphique
plt.show()
