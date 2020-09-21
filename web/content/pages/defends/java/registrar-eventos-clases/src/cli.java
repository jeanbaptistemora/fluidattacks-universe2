import java.util.logging.Level;
import java.util.logging.Logger;

class CLI {
  public static void main(String argv[]) throws Exception {
    Logger logger = Logger.getLogger("");
    logger.info("Procesing...");
    try {
      throw(new Exception());
    }
    catch (Exception e) {
      logger.log(Level.WARNING, "Hello... we've got a problem", e);
    }
    logger.fine("Done!");
  }
}
