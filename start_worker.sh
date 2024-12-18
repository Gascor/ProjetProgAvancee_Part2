#!/bin/bash

# Définir le chemin de base où les fichiers WorkerSocket.java sont compilés
BASE_PATH="/bin"

# Définir le premier port utilisé
START_PORT=25545

# Boucle pour ouvrir les ports et lancer 12 instances de WorkerSocket
for i in {0..11}
do
    PORT=$(($START_PORT + $i))
    echo "Configuring firewall for port $PORT"
    # Ajouter une règle pour permettre le trafic sur le port actuel
    sudo iptables -A INPUT -p tcp --dport $PORT -j ACCEPT
    sudo iptables -A OUTPUT -p tcp --sport $PORT -j ACCEPT
    
    echo "Starting WorkerSocket on port $PORT"
    java -cp $BASE_PATH src.WorkerSocket $PORT &> /dev/null &
    echo "WorkerSocket started on port $PORT"
done

echo "All WorkerSockets have been started."
