package src;

// Estimate the value of Pi using Monte-Carlo Method, using parallel program
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;

class PiMonteCarlo {
    long nThrows;
    AtomicInteger nSuccess;
    double value;
    int nThreads; // Nombre de threads à utiliser

    public PiMonteCarlo(long throwsCount, int nThreads) {
        this.nThrows = throwsCount;
        this.nSuccess = new AtomicInteger(0);
        this.value = 0;
        this.nThreads = nThreads;
    }

    public double getPi() {
        ExecutorService executor = Executors.newFixedThreadPool(nThreads);
        long chunkSize = nThrows / nThreads;

        for (int j = 0; j < nThreads; j++) {
            final long start = j * chunkSize;
            final long end = (j == nThreads - 1) ? nThrows : start + chunkSize;
            executor.submit(() -> {
                for (long i = start; i < end; i++) {
                    double x = Math.random();
                    double y = Math.random();
                    if (x * x + y * y <= 1)
                        nSuccess.incrementAndGet();
                }
            });
        }

        executor.shutdown();
        while (!executor.isTerminated()) {
            // attendre que tous les threads soient terminés
        }

        value = 4.0 * nSuccess.get() / nThrows;
        return value;
    }
}
