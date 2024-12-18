package src;

import java.io.*;
import java.net.*;

public class MasterSockett {
    static final int MAXSERVER = 128;
    // Tableau des ports configurés en dur pour chaque worker
    static final int[] tab_port = {25545, 25546, 25547, 25548};
    // Tableau des adresses IP configurées en dur pour chaque worker
    static String[] workerIPs = {"192.168.1.100", "192.168.1.101", "192.168.1.102", "192.168.1.103"};
    static BufferedReader[] reader = new BufferedReader[MAXSERVER];
    static PrintWriter[] writer = new PrintWriter[MAXSERVER];
    static Socket[] sockets = new Socket[MAXSERVER];

    public static void main(String[] args) throws Exception {
        long totalCount = 800000; // Total number of throws per Worker
        double pi;

        int numWorkers = workerIPs.length;  // Utiliser la taille du tableau workerIPs

        // Configuration et connexion des sockets pour chaque worker
        for (int i = 0; i < numWorkers; i++) {
            sockets[i] = new Socket(workerIPs[i], tab_port[i]);
            reader[i] = new BufferedReader(new InputStreamReader(sockets[i].getInputStream()));
            writer[i] = new PrintWriter(new BufferedWriter(new OutputStreamWriter(sockets[i].getOutputStream())), true);
        }

        distributeAndCollectResults(numWorkers, totalCount);
    }

    private static void distributeAndCollectResults(int numWorkers, long totalCount) throws IOException {
        long total = 0;
        long startTime = System.currentTimeMillis();

        // Envoyer le total de lancers à chaque Worker
        for (int i = 0; i < numWorkers; i++) {
            writer[i].println(totalCount);
        }

        // Collecter les résultats des Workers
        for (int i = 0; i < numWorkers; i++) {
            long partialResult = Long.parseLong(reader[i].readLine());
            total += partialResult;
        }

        double pi = 4.0 * total / (totalCount * numWorkers);  // Calculer PI
        long stopTime = System.currentTimeMillis();

        displayResults(pi, totalCount * numWorkers, numWorkers, stopTime - startTime);
        closeConnections(numWorkers);
    }

    private static void displayResults(double pi, long ntot, int numWorkers, long timeDuration) {
        System.out.println("Pi : " + pi);
        System.out.println("Total simulations: " + ntot);
        System.out.println("Number of Workers: " + numWorkers);
        System.out.println("Duration (ms): " + timeDuration);
    }

    private static void closeConnections(int numWorkers) throws IOException {
        // Fermer les connexions avec les Workers
        for (int i = 0; i < numWorkers; i++) {
            writer[i].println("END");  // Signal de fin aux Workers
            reader[i].close();
            writer[i].close();
            sockets[i].close();
        }
    }
}
