import java.util.logging.Logger;
import java.util.logging.Level;

public class Main
{
  private final static Logger logger = Logger.getLogger(Main.class.getName());
  public static void main(String argv[])
  {
    logger.setLevel(Level.WARNING);
    logger.warning("Comenzando el main");
    try
    {
      System.out.println("Hola");
      int i = 0/0;
    }
    catch (Exception e)
    {
      logger.severe("Problemas dentro del main");
    }
    logger.info("No se mostrará por no tener nivel
      WARNING o superior: Finalizando el main");
  }
}
