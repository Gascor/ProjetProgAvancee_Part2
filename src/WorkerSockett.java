package src;

import java.io.*;
import java.net.*;

public class WorkerSockett {
    private static int port = 25545; // Port par défaut
    private static boolean isRunning = true;

    public static void main(String[] args) throws Exception {
        if (args.length > 0) {
            port = Integer.parseInt(args[0]);  // Configurer le port via l'argument
        }

        ServerSocket serverSocket = new ServerSocket(port);
        System.out.println("Worker démarré sur le port : " + port);

        while (isRunning) {
            Socket socket = serverSocket.accept(); // Accepter une connexion du Master
            handleMaster(socket);
        }
        serverSocket.close();
    }

    private static void handleMaster(Socket socket) {
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             PrintWriter writer = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true)) {

            String str;
            while ((str = reader.readLine()) != null && !str.equals("END")) {
                long totalThrows = Long.parseLong(str);
                long totalInside = computeMonteCarlo((int) totalThrows);
                writer.println(totalInside);
            }

            if (str.equals("END")) {
                socket.close();
            }
        } catch (IOException e) {
            System.out.println("Erreur : " + e.getMessage());
        }
    }

    private static long computeMonteCarlo(int totalThrows) {
        long countInside = 0;
        for (int i = 0; i < totalThrows; i++) {
            double x = Math.random(); // Coordonnée x aléatoire entre 0 et 1
            double y = Math.random(); // Coordonnée y aléatoire entre 0 et 1
            if (x * x + y * y <= 1.0) { // Vérifier si le point est dans le quart de disque
                countInside++;
            }
        }
        return countInside;
    }
}
