package src;

public class Assignment102 {
    public static void main(String[] args) {
        // Vérifier que les arguments sont fournis
        if (args.length < 3) {
            System.out.println("Usage: java Assignment102 <total_points> <num_threads> <output_csv>");
            return;
        }

        // Récupérer les arguments
        int pointsPerWorker = Integer.parseInt(args[0]);  // Total de points par travailleur
        int numThreads = Integer.parseInt(args[1]);  // Nombre de threads (processeurs)
        String outputCsv = args[2];  // Nom du fichier CSV de sortie

        // Calculer Ntot correctement
        int totalPoints = pointsPerWorker * numThreads;

        // Créer une instance de PiMonteCarlo avec les paramètres
        PiMonteCarlo PiVal = new PiMonteCarlo(pointsPerWorker, numThreads);

        // Démarrer le chronomètre
        long startTime = System.currentTimeMillis();
        double value = PiVal.getPi();
        long stopTime = System.currentTimeMillis();

        // Afficher les résultats dans la console
        System.out.println("\nPi: " + value);
        System.out.println("Difference to exact value of pi: " + (value - Math.PI));
        System.out.println("Error: " + (Math.abs((value - Math.PI)) / Math.PI) + "\n");
        System.out.println("Ntot: " + totalPoints);  // Afficher Ntot correct
        System.out.println("Available processors: " + numThreads);
        System.out.println("Time Duration (ms): " + (stopTime - startTime));

        // Créer un objet CsvWriter et enregistrer les résultats dans le fichier CSV
        CsvWriter writer = new CsvWriter(outputCsv);
        writer.saveResults(value, value - Math.PI, (Math.abs((value - Math.PI)) / Math.PI), totalPoints, numThreads, (stopTime - startTime)*numThreads);
    }
}
