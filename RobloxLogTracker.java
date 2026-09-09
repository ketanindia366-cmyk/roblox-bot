import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class RobloxLogTracker {
    public static void main(String[] args) {
        // Ensure the arguments are completely provided by the Python runtime handler
        if (args.length < 3) {
            System.out.println("❌ Error: Missing configuration parameters from Python interface wrapper.");
            System.exit(1);
        }

        String userId = args[0];
        String actionType = args[1].toUpperCase();
        String rankId = args[2];

        // Format a localized current timestamp
        LocalDateTime now = LocalDateTime.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        String formattedTime = now.format(formatter);

        // Define our destination file track configuration
        String fileName = "java_audit_ledger.txt";

        try (FileWriter fw = new FileWriter(fileName, true);
             PrintWriter pw = new PrintWriter(fw)) {
            
            // Build the entry layout parameters cleanly
            String logEntry = String.format("[%s] [JAVA STORAGE CORE] Action: %s | Target User ID: %s | Applied Rank ID: %s", 
                    formattedTime, actionType, userId, rankId);
            
            pw.println(logEntry);
            
            // Return text string directly back into the Python app console pipeline
            System.out.println("Committed tracking parameters successfully to: " + fileName);

        } catch (IOException e) {
            System.out.println("❌ Java Critical Error writing to ledger: " + e.getMessage());
        }
    }
}
