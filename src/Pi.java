package src;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

/**
 * Approximates PI using the Monte Carlo method.  Demonstrates
 * use of Callables, Futures, and thread pools.
 */
public class Pi 
{
    public static void main(String[] args) throws Exception 
    {
	long total=0;
	total = new Master().doRun(50000, 10);
	System.out.println("total from Master = " + total);
    }
}

/**
 * Creates workers to run the Monte Carlo simulation
 * and aggregates the results.
 */
class Master {
	private final String csvFile = "execution_history_PI_Script.csv";
    public long doRun(int totalCount, int numWorkers) throws InterruptedException, ExecutionException, IOException
    {

	long startTime = System.currentTimeMillis();

	// Create a collection of tasks
	List<Callable<Long>> tasks = new ArrayList<Callable<Long>>();
	for (int i = 0; i < numWorkers; ++i) 
	    {
		tasks.add(new Worker(totalCount));
	    }
    
	// Run them and receive a collection of Futures
	ExecutorService exec = Executors.newFixedThreadPool(numWorkers);
	List<Future<Long>> results = exec.invokeAll(tasks);
	long total = 0;
    
	// Assemble the results.
	for (Future<Long> f : results) {
		// Call to get() is an implicit barrier. This will block
		// until result from corresponding worker is ready.
		total += f.get();
	}
	double pi = 4.0 * total / totalCount / numWorkers;

	long stopTime = System.currentTimeMillis();
	long duration = stopTime - startTime;

	double error = Math.abs((pi - Math.PI)) / Math.PI;

	// Affichage des résultats
	System.out.println("\nPi : " + pi);
	System.out.println("Error: " + error + "\n");
	System.out.println("Ntot: " + totalCount * numWorkers);
	System.out.println("Available processors: " + numWorkers);
	System.out.println("Time Duration (ms): " + duration + "\n");

	// Write to CSV
	writeToCSV(totalCount * numWorkers, numWorkers, duration, pi, error);

	exec.shutdown();
	return total;
    }
	private void writeToCSV(int totalIterations, int numWorkers, long duration, double pi, double error)
            throws IOException {
        try (FileWriter writer = new FileWriter(csvFile, true)) {
            // Write header if file is empty
            if (new java.io.File(csvFile).length() == 0) {
                writer.write("TotalIterations,NumWorkers,DurationMs,CalculatedPi,Error\n");
            }
            // Write execution data
            writer.write(totalIterations + "," + numWorkers + "," + duration + "," + pi + "," + error + "\n");
        }
    }
}

/**
 * Task for running the Monte Carlo simulation.
 */
class Worker implements Callable<Long> 
{   
    private int numIterations;
    public Worker(int num) 
	{ 
	    this.numIterations = num; 
	}

  @Override
      public Long call() 
      {
	  long circleCount = 0;
	  Random prng = new Random ();
	  for (int j = 0; j < numIterations; j++) 
	      {
		  double x = prng.nextDouble();
		  double y = prng.nextDouble();
		  if ((x * x + y * y) < 1)  ++circleCount;
	      }
	  return circleCount;
      }
}
