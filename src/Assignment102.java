package src;

public class Assignment102 {
    public static void main(String[] args) {
        if (args.length < 3) {
            System.out.println("Usage: java Assignment102 <total_points> <num_threads> <output_csv>");
            return;
        }

        int totalPoints = Integer.parseInt(args[0]);
        int numThreads = Integer.parseInt(args[1]);
        String outputCsv = args[2];

        PiMonteCarlo piVal = new PiMonteCarlo(totalPoints, numThreads);

        long startTime = System.currentTimeMillis();
        double value = piVal.getPi();
        long stopTime = System.currentTimeMillis();

        System.out.println("\nPi: " + value);
        System.out.println("Difference to exact value of pi: " + (value - Math.PI));
        System.out.println("Error: " + (Math.abs((value - Math.PI)) / Math.PI) + "\n");
        System.out.println("Ntot: " + totalPoints);
        System.out.println("Time Duration (ms): " + (stopTime - startTime));

        CsvWriter writer = new CsvWriter(outputCsv);
        writer.saveResults(value, value - Math.PI, (Math.abs((value - Math.PI)) / Math.PI), totalPoints, numThreads, (stopTime - startTime));
    }
}
