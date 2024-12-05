package src;
import java.io.*;
import java.net.*;
import java.text.SimpleDateFormat;
import java.util.Date;

/** Master is a client. It makes requests to numWorkers.
 *   
 */
public class MasterSocket {
    static int maxServer = 32;
    static final int[] tab_port = {25545,25546,25547,25548,25549,25550,25551,25552,25553,25554,25555,25556,25557,25558,25559,25560,25561,25562,25563,25564,25565,25566,25567,25568,25569,25570,25571,25572,25573,25574,25575,25576};
    static String[] tab_total_workers = new String[maxServer];
    static final String ip = "127.0.0.1";
    static BufferedReader[] reader = new BufferedReader[maxServer];
    static PrintWriter[] writer = new PrintWriter[maxServer];
    static Socket[] sockets = new Socket[maxServer];
    
    
    public static void main(String[] args) throws Exception {

	// MC parameters
	int totalCount = 666667; // total number of throws on a Worker
	int total = 0; // total number of throws inside quarter of disk
	double pi; 

	int numWorkers = maxServer;
	BufferedReader bufferRead = new BufferedReader(new InputStreamReader(System.in));
	String s; // for bufferRead

	System.out.println("#########################################");
	System.out.println("# Computation of PI by MC method        #");
	System.out.println("#########################################");
	
	System.out.println("\n How many workers for computing PI (< maxServer): ");
	try{
	    s = bufferRead.readLine();
	    numWorkers = Integer.parseInt(s);
	    System.out.println(numWorkers);
	}
	catch(IOException ioE){
	   ioE.printStackTrace();
	}
	
	for (int i=0; i<numWorkers; i++){
	    System.out.println("Enter worker"+ i +" port : ");
	    try{
		s = bufferRead.readLine();
		System.out.println("You select " + s);
	    }
	    catch(IOException ioE){
		ioE.printStackTrace();
	    }
	}

       //create worker's socket
       for(int i = 0 ; i < numWorkers ; i++) {
	   sockets[i] = new Socket(ip, tab_port[i]);
	   System.out.println("SOCKET = " + sockets[i]);
	   
	   reader[i] = new BufferedReader( new InputStreamReader(sockets[i].getInputStream()));
	   writer[i] = new PrintWriter(new BufferedWriter(new OutputStreamWriter(sockets[i].getOutputStream())),true);
       }

       String message_to_send;
       message_to_send = String.valueOf(totalCount);

       String message_repeat = "y";

       long stopTime, startTime;

       while (message_repeat.equals("y")){

	   startTime = System.currentTimeMillis();
	   // initialize workers
	   for(int i = 0 ; i < numWorkers ; i++) {
	       writer[i].println(message_to_send);          // envoi d'un message a chaque worker
	   }
	   
	   //listen to workers's message 
	   for(int i = 0 ; i < numWorkers ; i++) {
	       tab_total_workers[i] = reader[i].readLine();      // reception de la reponse de chaque worker
	       System.out.println("Client sent: " + tab_total_workers[i]);
	   }
	   total = 0;
	   // compute PI with the result of each workers
	   for(int i = 0 ; i < numWorkers ; i++) {
	       total += Integer.parseInt(tab_total_workers[i]);
	   }
	   pi = 4.0 * total / totalCount / numWorkers;

	   stopTime = System.currentTimeMillis();

	   System.out.println("\nPi : " + pi );
	   System.out.println("Error: " + (Math.abs((pi - Math.PI)) / Math.PI) +"\n");
	   
	   System.out.println("Ntot: " + totalCount*numWorkers);
	   System.out.println("Available processors: " + numWorkers);
	   System.out.println("Time Duration (ms): " + (stopTime - startTime) + "\n");
	   
	   System.out.println( (Math.abs((pi - Math.PI)) / Math.PI) +" "+ totalCount*numWorkers +" "+ numWorkers +" "+ (stopTime - startTime));
	   
	   saveResultsToCSV(numWorkers, totalCount * numWorkers, pi, Math.abs((pi - Math.PI)) / Math.PI, stopTime - startTime);
	   System.out.println("\n Repeat computation (y/N): ");
	   try{
	       message_repeat = bufferRead.readLine();
	       System.out.println(message_repeat);
	   }
	   catch(IOException ioE){
	       ioE.printStackTrace();
	   }
       }
       
       for(int i = 0 ; i < numWorkers ; i++) {
	   System.out.println("END");     // Send ending message
	   writer[i].println("END") ;
	   reader[i].close();
	   writer[i].close();
	   sockets[i].close();
       }
   	}
   	/**
	 * Save execution results to a CSV file.
	 */
	public static void saveResultsToCSV(int numWorkers, int totalThrows, double pi, double error, long duration) {
		String fileName = "results.csv";
		File file = new File(fileName);

		try (PrintWriter writer = new PrintWriter(new FileWriter(file, true))) {
			if (file.length() == 0) {
				writer.println("Date;Number of Workers;Total Throws;Estimated Pi;Error;Execution Time (ms)");
			}
			
			String date = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());
			writer.printf("%s;%d;%d;%.8f;%.8e;%d%n", date, numWorkers, totalThrows, pi, error, duration);
			
			System.out.println("Results saved to file: " + fileName);
		} catch (IOException e) {
			System.err.println("Error writing results to CSV file: " + e.getMessage());
		}
	}

}