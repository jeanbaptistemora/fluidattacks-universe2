import java.util.logging.FileHandler;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;

class CLI
{
  public static void main(String argv[]) throws Exception
  {
    Logger logger = Logger.getLogger(“”);
    FileHandler fh = new FileHandler("CLI.log");
    fh.setFormatter(new MyFormatter());
    logger.setLevel(Level.ALL);
    logger.addHandler(fh);
    logger.info("procesando...");
    try
    {
      throw(new Exception());
    }
    catch (Exception e)
    {
      logger.log(Level.WARNING, "houston... we've got a problem", e);
    }
    logger.fine("hecho!");
  }
}
