package src;

import java.io.*;
import java.net.*;

public class MasterSockett {
    static final int MAXSERVER = 24; // Total de 24 workers (12 par machine)
    static final int[] tab_port = new int[MAXSERVER];
    static String[] workerIPs = new String[MAXSERVER];
    static BufferedReader[] reader = new BufferedReader[MAXSERVER];
    static PrintWriter[] writer = new PrintWriter[MAXSERVER];
    static Socket[] sockets = new Socket[MAXSERVER];

    public static void main(String[] args) throws Exception {
        long totalCount = 800000; // Total number of throws per Worker
        double pi;

        // Initialisation des ports et IPs pour chaque worker
        for (int i = 0; i < 12; i++) {
            tab_port[i] = 25545 + i; // Workers sur la première machine
            workerIPs[i] = "192.168.24.60";  // IP de la première machine worker
            tab_port[i + 12] = 25545 + i; // Workers sur la deuxième machine
            workerIPs[i + 12] = "192.168.24.175"; // IP de la deuxième machine worker
        }

        // Connexion aux workers
        for (int i = 0; i < MAXSERVER; i++) {
            sockets[i] = new Socket(workerIPs[i], tab_port[i]);
            reader[i] = new BufferedReader(new InputStreamReader(sockets[i].getInputStream()));
            writer[i] = new PrintWriter(new BufferedWriter(new OutputStreamWriter(sockets[i].getOutputStream())), true);
            System.out.println("Connected to worker at " + workerIPs[i] + " on port " + tab_port[i]);
        }

        distributeAndCollectResults(MAXSERVER, totalCount);
    }

    private static void distributeAndCollectResults(int numWorkers, long totalCount) throws IOException {
        long total = 0, startTime = System.currentTimeMillis(), stopTime;

        // Envoyer les instructions aux workers
        for (int i = 0; i < numWorkers; i++) {
            writer[i].println(totalCount);
        }

        // Collecter les résultats des workers
        for (int i = 0; i < numWorkers; i++) {
            long partialResult = Long.parseLong(reader[i].readLine());
            total += partialResult;
        }

        double pi = 4.0 * total / (totalCount * numWorkers);
        stopTime = System.currentTimeMillis();

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
        for (int i = 0; i < numWorkers; i++) {
            writer[i].println("END");
            reader[i].close();
            writer[i].close();
            sockets[i].close();
        }
    }
}
