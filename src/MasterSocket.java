package src;

import java.io.*;
import java.net.*;

/**
 * MasterSocket : Coordonne les Workers pour calculer Pi via des sockets.
 */
public class MasterSocket {
	static final int MAXSERVER = 128;
	static final int[] tab_port = {25545, 25546, 25547, 25548, 25549, 25550, 25551, 25552, 25553, 25554, 25555, 25556, 25557, 25558, 25559, 25560, 25561, 25562, 25563, 25564, 25565, 25566, 25567, 25568, 25569, 25570, 25571, 25572, 25573, 25574, 25575, 25576, 25577, 25578, 25579, 25580, 25581, 25582, 25583, 25584, 25585, 25586, 25587, 25588, 25589, 25590, 25591, 25592, 25593, 25594, 25595, 25596, 25597, 25598, 25599, 25600, 25601, 25602, 25603, 25604, 25605, 25606, 25607, 25608, 25609, 25610, 25611, 25612, 25613, 25614, 25615, 25616, 25617, 25618, 25619, 25620, 25621, 25622, 25623, 25624, 25625, 25626, 25627, 25628, 25629, 25630, 25631, 25632, 25633, 25634, 25635, 25636, 25637, 25638, 25639, 25640, 25641, 25642, 25643, 25644, 25645, 25646, 25647, 25648, 25649, 25650, 25651, 25652, 25653, 25654, 25655, 25656, 25657, 25658, 25659, 25660, 25661, 25662, 25663, 25664, 25665, 25666, 25667, 25668, 25669, 25670, 25671, 25672};
	static String[] tab_total_workers = new String[MAXSERVER];
	static final String ip = "127.0.0.1";
	static BufferedReader[] reader = new BufferedReader[MAXSERVER];
	static PrintWriter[] writer = new PrintWriter[MAXSERVER];
	static Socket[] sockets = new Socket[MAXSERVER];

	public static void main(String[] args) throws Exception {
		long totalCount = 50000; // total number of throws on a Worker
		int total = 0; // total number of throws inside quarter of disk
		double pi;

		int numWorkers = 32;
		BufferedReader bufferRead = new BufferedReader(new InputStreamReader(System.in));
		String s;

		System.out.println("#########################################");
		System.out.println("# Computation of PI by MC method        #");
		System.out.println("#########################################");



		// Create worker sockets
		for (int i = 0; i < numWorkers; i++) {
			sockets[i] = new Socket(ip, tab_port[i]);
			System.out.println("SOCKET = " + sockets[i]);

			reader[i] = new BufferedReader(new InputStreamReader(sockets[i].getInputStream()));
			writer[i] = new PrintWriter(new BufferedWriter(new OutputStreamWriter(sockets[i].getOutputStream())), true);
		}

		String message_to_send = String.valueOf(totalCount);
		String message_repeat = "y";

		long stopTime, startTime;

		while (message_repeat.equals("y")) {
			startTime = System.currentTimeMillis();

			// Initialize workers
			for (int i = 0; i < numWorkers; i++) {
				writer[i].println(message_to_send); // Send a message to each worker
			}

			// Listen to workers' messages
			for (int i = 0; i < numWorkers; i++) {
				tab_total_workers[i] = reader[i].readLine(); // Read message from server
				System.out.println("Client sent: " + tab_total_workers[i]);
			}
			total = 0;
			// Compute PI with the result of each worker
			for (int i = 0; i < numWorkers; i++) {
				total += Integer.parseInt(tab_total_workers[i]);
			}
			pi = 4.0 * total / totalCount / numWorkers;

			stopTime = System.currentTimeMillis();
			long timeDuration = stopTime - startTime;

			long ntot = totalCount * numWorkers;
			double difference = pi - Math.PI;
			double error = Math.abs(difference) / Math.PI;

			// Display results
			System.out.println("\nPi : " + pi);
			System.out.println("Error: " + error + "\n");

			System.out.println("Ntot: " + ntot);
			System.out.println("Available processors: " + numWorkers);
			System.out.println("Time Duration (ms): " + timeDuration + "\n");

			// Save results to CSV
			saveResultsToCsv("results.csv", pi, difference, error, ntot, numWorkers, timeDuration);

			// Repeat computation prompt
			System.out.println("\nRepeat computation (y/N): ");
			try {
				message_repeat = bufferRead.readLine();
				System.out.println(message_repeat);
			} catch (IOException ioE) {
				ioE.printStackTrace();
			}
		}

		// Close connections
		for (int i = 0; i < numWorkers; i++) {
			System.out.println("END"); // Send ending message
			writer[i].println("END");
			reader[i].close();
			writer[i].close();
			sockets[i].close();
		}
	}

	/**
	 * Saves the results to a CSV file.
	 */
	private static void saveResultsToCsv(String fileName, double pi, double difference, double error, long ntot, int processors, long timeDuration) {
		File file = new File(fileName);
		boolean isNewFile = !file.exists();

		try (FileWriter fw = new FileWriter(file, true); BufferedWriter bw = new BufferedWriter(fw); PrintWriter writer = new PrintWriter(bw)) {
			if (isNewFile) {
				// Write header if file is new
				writer.println("PI,Difference,Error,Ntot,AvailableProcessors,TimeDuration(ms)");
			}
			// Add results to file
			writer.printf("%f;%f;%f;%d;%d;%d;%n", pi, difference, error, ntot, processors, timeDuration);
			System.out.println("Results saved to file: " + fileName);
		} catch (IOException e) {
			System.err.println("Error writing to CSV file: " + e.getMessage());
		}
	}
}
