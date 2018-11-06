import java.util.logging.ConsoleHandler;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Config {
  public Config() {
    System.out.println("Configuring...");
    Logger logger = Logger.getLogger("");
    ConsoleHandler ch = new ConsoleHandler();
    ch.setLevel(Level.INFO);
    logger.addHandler(ch);
    logger.setLevel(Level.ALL);
  }
}
