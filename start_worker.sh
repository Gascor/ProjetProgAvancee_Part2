#!/bin/bash

# Définir le chemin de base où les fichiers WorkerSocket.java sont compilés
BASE_PATH="/path/to/your/project/bin"

# Définir le premier port utilisé
START_PORT=25545

# Vérifier si firewalld est installé et l'installer si nécessaire
if ! command -v firewall-cmd &> /dev/null
then
    echo "firewalld could not be found, installing..."
    sudo apt update
    sudo apt install firewalld
    sudo systemctl start firewalld
    sudo systemctl enable firewalld
fi

# Boucle pour configurer le pare-feu et lancer 12 instances de WorkerSocket
for i in {0..11}
do
    PORT=$(($START_PORT + $i))
    echo "Configuring firewall for port $PORT"
    sudo firewall-cmd --zone=public --add-port=${PORT}/tcp --permanent
    
    echo "Starting WorkerSocket on port $PORT"
    java -cp $BASE_PATH src.WorkerSocket $PORT &> /dev/null &
    echo "WorkerSocket started on port $PORT"
done

# Recharger firewalld pour appliquer les changements
sudo firewall-cmd --reload

echo "All WorkerSockets have been started and firewall configured."
